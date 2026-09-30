import pyautogui
import pygetwindow as gw
import time

def close_active_window():
    """Закрывает активное окно (Alt+F4)"""
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.2)
    print("❌ Окно закрыто")

def maximize_active_window():
    """Разворачивает активное окно (Win+Up)"""
    pyautogui.hotkey('win', 'up')
    time.sleep(0.2)
    print("⏹️ Окно развернуто")

def minimize_active_window():
    """Сворачивает активное окно (Win+Down)"""
    pyautogui.hotkey('win', 'down')
    time.sleep(0.2)
    print("➖ Окно свернуто")

def switch_to_window(title_part):
    """Переключается на окно, содержащее title_part в заголовке"""
    try:
        windows = gw.getWindowsWithTitle(title_part)
        if windows:
            win = windows[0]
            win.activate()
            time.sleep(0.3)
            print(f"🔄 Переключено на окно: {win.title}")
            return True
    except Exception as e:
        print(f"⚠️ Ошибка переключения: {e}")
    return False

def get_active_window_title():
    """Возвращает заголовок активного окна"""
    try:
        win = gw.getActiveWindow()
        if win:
            return win.title
    except:
        pass
    return None