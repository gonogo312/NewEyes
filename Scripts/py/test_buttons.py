import webbrowser
import pyautogui

url = 'www.google.com'
chrome_path = 'chromium.exe www.google.com --incognito'

webbrowser.open(chrome_path)

pyautogui.keyDown("ctrl")
pyautogui.keyDown("shift")
pyautogui.press("n")

pyautogui.keyUp("ctrl")
pyautogui.keyUp("shift")