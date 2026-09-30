import pyautogui
import time
import pyperclip

def copy_text():
    """Копирует выделенный текст в буфер обмена"""
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)
    print("📋 Скопировано")

def paste_text():
    """Вставляет текст из буфера обмена"""
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    print("📋 Вставлено")

def cut_text():
    """Вырезает выделенный текст в буфер обмена"""
    pyautogui.hotkey('ctrl', 'x')
    time.sleep(0.1)
    print("✂️ Вырезано")

def get_clipboard_text():
    """Возвращает текст из буфера обмена"""
    return pyperclip.paste()

def set_clipboard_text(text):
    """Записывает текст в буфер обмена"""
    pyperclip.copy(text)
    print(f"📝 В буфер обмена записано: {text[:50]}...")