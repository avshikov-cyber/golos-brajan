# -*- coding: utf-8 -*-
"""
INTUITION CORE — универсальный мозг предвосхищения.

Три точки:
  1. ПАМЯТЬ (memory)     — что система уже видела
  2. ПРЕДВОСХИЩЕНИЕ (anticipation) — что система ожидает
  3. ВОСПРИЯТИЕ (perception)       — что реально произошло

Четвёртая точка:
  4. CONVERGENCE — встреча ожидания и реальности.
     MATCH / NO_MATCH. Результат пишется обратно в память.

Особенности:
- Fallback: если нет кандидатов, берём самый частый вариант вообще.
- Decay: старые переходы слабеют со временем.
- Контексты: один мозг — много контекстов.
- Универсальность: не знает про "музыку" или "браузер". Работает с
  абстрактными событиями. Адаптация — на стороне пользователя.

Автор: Капитан и Кит. 2026.
"""

import json
import os
import time
from datetime import datetime
from collections import defaultdict, Counter


# ==================== НАСТРОЙКИ ПО УМОЛЧАНИЮ ====================
DEFAULT_DECAY_RATE = 0.01
DEFAULT_MIN_CONFIDENCE = 0.05
DEFAULT_FALLBACK = True


# ==================== ЯДРО ====================
class IntuitionCore:
    """
    Универсальный мозг предвосхищения.
    Не знает ничего о конкретной системе.
    """

    def __init__(
        self,
        decay_rate=DEFAULT_DECAY_RATE,
        min_confidence=DEFAULT_MIN_CONFIDENCE,
        enable_fallback=DEFAULT_FALLBACK,
        journal_file=None,
    ):
        self.decay_rate = decay_rate
        self.min_confidence = min_confidence
        self.enable_fallback = enable_fallback
        self.journal_file = journal_file or "intuition_journal.json"

        # transitions[context][A][B] = вес перехода A -> B
        self.transitions = defaultdict(lambda: defaultdict(Counter))

        # последнее событие в каждом контексте
        self._last_event = {}

        # текущий контекст
        self.current_context = "default"

        # состояние цикла
        self.anticipation = None
        self.perception = None

        # журнал и статистика
        self.journal = []
        self.matches = 0
        self.no_matches = 0
        self.no_anticipation = 0

        # Загружаем сохранённый журнал, если есть
        self.load_journal()

    # ==================== 1. ПАМЯТЬ ====================
    def store(self, event, context=None):
        """Сохраняет событие в память контекста."""
        ctx = context or self.current_context
        prev = self._last_event.get(ctx)

        if prev is not None:
            self.transitions[ctx][prev][event] += 1

        self._last_event[ctx] = event
        return event

    # ==================== 2. ПРЕДВОСХИЩЕНИЕ ====================
    def anticipate(self, context=None):
        """
        Предвосхищает следующее событие на основе памяти.
        Возвращает ожидаемое событие или None.
        """
        ctx = context or self.current_context
        last_event = self._last_event.get(ctx)

        if last_event is None:
            self.anticipation = None
            return None

        candidates = self.transitions[ctx].get(last_event, Counter())

        # Fallback: если нет кандидатов по текущему событию
        if not candidates and self.enable_fallback:
            all_events = Counter()
            for src_counter in self.transitions[ctx].values():
                all_events.update(src_counter)
            if all_events:
                expected, count = all_events.most_common(1)[0]
                self.anticipation = {
                    "time": datetime.now().isoformat(),
                    "context": ctx,
                    "based_on": last_event,
                    "expected": expected,
                    "confidence": count,
                    "fallback": True,
                }
                return expected

        if not candidates:
            self.anticipation = None
            return None

        expected, count = candidates.most_common(1)[0]
        self.anticipation = {
            "time": datetime.now().isoformat(),
            "context": ctx,
            "based_on": last_event,
            "expected": expected,
            "confidence": count,
            "fallback": False,
        }
        return expected

    # ==================== 3. ВОСПРИЯТИЕ ====================
    def perceive(self, real_event):
        """Считывает реальное событие."""
        self.perception = {
            "time": datetime.now().isoformat(),
            "actual": real_event,
        }
        return real_event

    # ==================== 4. CONVERGENCE ====================
    def converge(self, auto_store=True):
        """
        Фиксирует встречу предвосхищения и восприятия.
        Возвращает: "MATCH", "NO_MATCH" или "NO_ANTICIPATION".
        """
        if self.perception is None:
            raise RuntimeError("Сначала вызови perceive(event).")

        if self.anticipation is None:
            verdict = "NO_ANTICIPATION"
            self.no_anticipation += 1
        elif self.anticipation["expected"] == self.perception["actual"]:
            verdict = "MATCH"
            self.matches += 1
        else:
            verdict = "NO_MATCH"
            self.no_matches += 1

        entry = {
            "time": datetime.now().isoformat(),
            "context": self.current_context,
            "anticipation": self.anticipation,
            "perception": self.perception,
            "verdict": verdict,
        }
        self.journal.append(entry)

        if auto_store:
            self.store(self.perception["actual"])

        self.anticipation = None
        self.perception = None
        return verdict

    # ==================== DECAY ====================
    def apply_decay(self, context=None):
        """Гасит все переходы в контексте."""
        ctx = context or self.current_context
        for src in list(self.transitions[ctx].keys()):
            counter = self.transitions[ctx][src]
            for ev in list(counter.keys()):
                counter[ev] *= (1 - self.decay_rate)
                if counter[ev] < self.min_confidence:
                    del counter[ev]
            if not counter:
                del self.transitions[ctx][src]

    # ==================== КОНТЕКСТЫ ====================
    def switch_context(self, context):
        """Переключает текущий контекст."""
        self.current_context = context
        return context

    # ==================== УДОБНЫЙ ЦИКЛ ====================
    def cycle(self, real_event):
        """
        Полный цикл одной командой.
        Возвращает: (expected, verdict, confidence)
        """
        expected = self.anticipate()
        self.perceive(real_event)
        verdict = self.converge()
        confidence = None
        if self.journal:
            last = self.journal[-1]
            if last["anticipation"]:
                confidence = last["anticipation"]["confidence"]
        return expected, verdict, confidence

    # ==================== ЖУРНАЛ ====================

    def load_journal(self, path=None):
        """Загружает журнал с диска и восстанавливает transitions."""
        filepath = path or self.journal_file
        if not os.path.exists(filepath):
            print(f"Журнал не найден: {filepath}")
            return
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки журнала: {e}")
            return

        self.journal = data.get("journal", [])
        stats = data.get("stats", {})
        self.matches = stats.get("matches", 0)
        self.no_matches = stats.get("no_matches", 0)
        self.no_anticipation = stats.get("no_anticipation", 0)

        # Пересчитываем transitions из journal
        self.transitions = defaultdict(lambda: defaultdict(Counter))
        self._last_event = {}
        for entry in self.journal:
            per = entry.get("perception") or {}
            ant = entry.get("anticipation") or {}
            actual = per.get("actual")
            based_on = ant.get("based_on")
            if based_on and actual:
                self.transitions["default"][based_on][actual] += 1
            if actual:
                self._last_event["default"] = actual

        print(f"Журнал загружен: {len(self.journal)} записей")

    def save_journal(self, path=None):
        """Сохраняет журнал в JSON."""
        filepath = path or self.journal_file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "stats": self.get_stats(),
                "journal": self.journal,
            }, f, ensure_ascii=False, indent=2)

    def get_stats(self):
        """Возвращает статистику."""
        total = len(self.journal)
        hit_rate = round(self.matches / total, 3) if total else 0.0
        return {
            "total_cycles": total,
            "matches": self.matches,
            "no_matches": self.no_matches,
            "no_anticipation": self.no_anticipation,
            "hit_rate": hit_rate,
            "contexts": list(self.transitions.keys()),
        }

    def reset(self):
        """Полный сброс."""
        self.transitions = defaultdict(lambda: defaultdict(Counter))
        self._last_event = {}
        self.anticipation = None
        self.perception = None
        self.journal = []
        self.matches = 0
        self.no_matches = 0
        self.no_anticipation = 0


# ==================== ПРИМЕР ИСПОЛЬЗОВАНИЯ ====================
if __name__ == "__main__":
    print("INTUITION CORE — пример работы\n")

    brain = IntuitionCore()

    stream = [
        "привет", "как дела", "нормально", "а у тебя", "тоже",
        "привет", "как дела", "хорошо",
        "привет", "как дела", "нормально", "пока",
    ]

    # Первое событие — только в память
    brain.store(stream[0])

    for event in stream[1:]:
        expected, verdict, confidence = brain.cycle(event)
        mark = "OK" if verdict == "MATCH" else ("MISS" if verdict == "NO_MATCH" else "...")
        print(f"  {mark}  ожидал: {expected} | увидел: {event} | {verdict}")

    print()
    print("Статистика:", brain.get_stats())
    brain.save_journal()
    print("Журнал сохранён: intuition_journal.json")
