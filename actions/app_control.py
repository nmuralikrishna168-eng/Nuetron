import subprocess
import time
import urllib.parse
import webbrowser
import pyautogui
import pygetwindow as gw


class AppController:
    """Control and automate Windows applications."""

    @staticmethod
    def open_app_and_type(app_command: str, text: str, delay: float = 1.5):
        try:
            subprocess.Popen(app_command, shell=True)
            time.sleep(delay)
            pyautogui.write(text, interval=0.03)
        except Exception as e:
            print(f"App control error: {e}")

    @staticmethod
    def open_notepad(text: str = ""):
        try:
            subprocess.Popen("notepad.exe")
            time.sleep(1.2)
            if text:
                pyautogui.write(text, interval=0.01)
        except Exception as e:
            print(f"Notepad error: {e}")

    @staticmethod
    def play_youtube_video(query: str):
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            webbrowser.open(url)
            time.sleep(3.5)
            pyautogui.press("tab")
            pyautogui.press("enter")
        except Exception as e:
            print(f"YouTube automation error: {e}")

    @staticmethod
    def open_website(url: str):
        try:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            webbrowser.open(url)
        except Exception as e:
            print(f"Browser error: {e}")

    @staticmethod
    def bring_window_to_front(window_title: str):
        try:
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                windows[0].activate()
        except Exception as e:
            print(f"Window control error: {e}")

    @staticmethod
    def close_application(app_name: str):
        try:
            subprocess.call(f"taskkill /IM {app_name} /F", shell=True)
        except Exception as e:
            print(f"Close app error: {e}")
