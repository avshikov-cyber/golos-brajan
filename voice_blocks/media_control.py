import pyautogui
import time

def media_play_pause():
    """Воспроизвести/приостановить"""
    pyautogui.press('playpause')
    time.sleep(0.1)
    print("⏯️ Play/Pause")

def media_next():
    """Следующий трек"""
    pyautogui.press('nexttrack')
    time.sleep(0.1)
    print("⏭️ Следующий")

def media_prev():
    """Предыдущий трек"""
    pyautogui.press('prevtrack')
    time.sleep(0.1)
    print("⏮️ Предыдущий")

def media_stop():
    """Остановить воспроизведение"""
    pyautogui.press('stop')
    time.sleep(0.1)
    print("⏹️ Стоп")