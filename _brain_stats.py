# _brain_stats.py
# Метрики динамики и ошибок Брайана

import json
import os
from datetime import datetime
from collections import Counter

BASE = r"C:\Users\USER\OneDrive\Desktop"
JOURNAL = os.path.join(BASE, "golos_intuition_journal.json")
HISTORY = os.path.join(BASE, "brain_stats_history.json")
ERRORS = os.path.join(BASE, "brain_errors.md")


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("=" * 60)
    print("АНАЛИЗ МОЗГА БРАЙАНА")
    print("=" * 60)

    j = load_json(JOURNAL)
    if not j:
        print("Журнал не найден")
        return

    stats = j.get("stats", {})
    journal = j.get("journal", [])

    total = stats.get("total_cycles", 0)
    matches = stats.get("matches", 0)
    no_matches = stats.get("no_matches", 0)
    no_anticipation = stats.get("no_anticipation", 0)
    hit_rate = stats.get("hit_rate", 0.0)

    # Средний confidence
    confs = []
    for e in journal:
        ant = e.get("anticipation")
        if ant and "confidence" in ant:
            confs.append(ant["confidence"])
    avg_conf = round(sum(confs) / len(confs), 2) if confs else 0.0

    # Топ переходов (based_on -> actual)
    transitions = Counter()
    for e in journal:
        ant = e.get("anticipation")
        per = e.get("perception")
        if ant and per:
            based = ant.get("based_on", "")
            actual = per.get("actual", "")
            if based and actual:
                transitions[(based[:30], actual[:30])] += 1

    # Топ ошибок (expected != actual, verdict NO_MATCH)
    errors = Counter()
    for e in journal:
        if e.get("verdict") == "NO_MATCH":
            ant = e.get("anticipation") or {}
            per = e.get("perception") or {}
            expected = ant.get("expected", "")[:30]
            actual = per.get("actual", "")[:30]
            if expected or actual:
                errors[(expected, actual)] += 1

    # Вывод
    print(f"\nДата: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"\n📊 СТАТИСТИКА")
    print(f"  Всего циклов:      {total}")
    print(f"  MATCH:             {matches}")
    print(f"  NO_MATCH:          {no_matches}")
    print(f"  NO_ANTICIPATION:   {no_anticipation}")
    print(f"  hit_rate:          {hit_rate}")
    print(f"  avg confidence:    {avg_conf}")

    # Динамика
    history = load_json(HISTORY) or {"snapshots": []}
    prev = history["snapshots"][-1] if history["snapshots"] else None

    if prev:
        print(f"\n📈 ДИНАМИКА (с прошлого снимка)")
        d_total = total - prev.get("total", 0)
        d_matches = matches - prev.get("matches", 0)
        d_hit = round(hit_rate - prev.get("hit_rate", 0.0), 3)
        d_conf = round(avg_conf - prev.get("avg_confidence", 0.0), 2)
        print(f"  +{d_total} циклов")
        print(f"  +{d_matches} MATCH")
        print(f"  hit_rate: {d_hit:+}")
        print(f"  confidence: {d_conf:+}")

    # Топ переходов
    print(f"\n🔄 ТОП-10 ПЕРЕХОДОВ")
    for (a, b), c in transitions.most_common(10):
        print(f"  {c}x  {a} → {b}")

    # Топ ошибок
    print(f"\n❌ ТОП-10 ОШИБОК")
    for (exp, act), c in errors.most_common(10):
        print(f"  {c}x  ожидал: {exp} | было: {act}")

    # Сохраняем снимок
    snapshot = {
        "date": datetime.now().isoformat(),
        "total": total,
        "matches": matches,
        "no_matches": no_matches,
        "no_anticipation": no_anticipation,
        "hit_rate": hit_rate,
        "avg_confidence": avg_conf,
        "top_transitions": [{"from": a, "to": b, "count": c} for (a, b), c in transitions.most_common(20)],
        "top_errors": [{"expected": exp, "actual": act, "count": c} for (exp, act), c in errors.most_common(20)]
    }
    history["snapshots"].append(snapshot)
    save_json(HISTORY, history)
    print(f"\n💾 Снимок сохранён: {HISTORY}")

    # Дневник ошибок
    with open(ERRORS, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"- Циклов: {total}, MATCH: {matches}, hit_rate: {hit_rate}\n")
        f.write(f"- Топ ошибок:\n")
        for (exp, act), c in errors.most_common(5):
            f.write(f"  - {c}x ожидал: `{exp}` | было: `{act}`\n")

    print(f"📝 Дневник ошибок: {ERRORS}")
    print("=" * 60)


if __name__ == "__main__":
    main()