import window_control as wc
import time
import subprocess

print("🐋 Тест управления окнами (БЕЗОПАСНЫЙ)")
print("=" * 40)
print("Сейчас будет открыт Блокнот, а затем он закроется через 5 секунд.")

# Открываем Блокнот
subprocess.Popen("notepad.exe")
time.sleep(2)

# Закрываем Блокнот через 5 секунд
print("⏳ Закрываем Блокнот через 5 секунд...")
time.sleep(5)
wc.close_active_window()
print("✅ Тест управления окнами завершён!")