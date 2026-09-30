# test_blocks.py
import clipboard_control as cb
import window_control as wc
import media_control as mc

print("🐋 Тестирование блоков управления")
print("=" * 40)

# 1. Буфер обмена
print("\n📋 Тест буфера обмена:")
print("Выдели текст в любом окне и нажми Enter")
input()
cb.copy_text()
print(f"Скопировано: {cb.get_clipboard_text()}")
print("Нажми Enter, чтобы вставить текст")
input()
cb.paste_text()

# 2. Управление окнами
print("\n🪟 Тест управления окнами:")
print("Нажми Enter, чтобы закрыть активное окно")
input()
wc.close_active_window()

# 3. Медиа
print("\n🎵 Тест управления медиа:")
print("Нажми Enter, чтобы поставить на паузу/воспроизвести")
input()
mc.media_play_pause()