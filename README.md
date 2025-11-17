# 🛡️ Keylogger Etico - Red Teaming Project

Spython è un keylogger sviluppato in Python e nato come progetto accademico nell’ambito del **Red Teaming**.  
Questo strumento dimostra come funzionano tecniche di keylogging, rilevamento dei processi e cattura di screenshot che sono tipiche dei malware reali. 

**Nasce esclusivamente per scopi didattici e di difesa**.

Non è un malware. Non è uno strumento di spionaggio. 
È un **simulatore controllato** per comprendere le minacce e imparare a difendersi.

> 🔐 **Strumento Educativo — Realizzato per Imparare, Non per Abusare. Non mi assumo responsabilità di nessun uso illecito o illegale. Anche se il programma è educativo, molti antivirus (es. Windows Defender) lo rileveranno come malware, perché le sue funzionalità (keylogging, screenshot, invio dati) sono tipiche di software malevoli. È normale che venga bloccato o cancellato.**


## 🧩 Funzionalità Implementate

🔹 **Cattura keystrokes in tempo reale**: caratteri alfanumerici e tasti speciali come `[enter]`, `[space]`, `[backspace]`, `[ctrl]`  
🔹 **Rilevamento del processo attivo**: identifica l’applicazione in uso (es. `chrome.exe`, `steam.exe`, `notepad.exe`) tramite API Windows e `psutil`  
🔹 **Screenshot automatici**: viene catturato uno screenshot ogni volta che viene premuto il tasto `Invio`  
🔹 **Invio dati su Telegram**: testo formattato in Markdown + screenshot inviati via API del bot  
🔹 **Pulizia automatica dei file temporanei**: gli screenshot vengono cancellati immediatamente dopo l’invio  
🔹 **Compilazione in .exe autonomo**: grazie a Nuitka, il programma può essere eseguito su qualsiasi PC Windows senza Python installato  
🔹 **Modalità silenziosa**: nessuna finestra di comando visibile (`--windows-disable-console`)
🔹 **Cattura informazioni Sistema operativo**: Cattura delle informazioni del sistema operativo del dispositivo.
🔹 **Wi-Fi passowrd scraper**: cattura della password del Wi-Fi attualmente connesso alla macchina.




## 🛠️ Dipendenze e Installazione

### Requisiti

- Python 3.10 o superiore
- Sistema operativo: **Windows 10/11**
- Un bot Telegram (creato tramite `@BotFather`)

### Installazione delle librerie

Apri un terminale (PowerShell o CMD) e esegui:
```bash
pip install -r requirements.txt
```


# 🤖 Configurazione del Bot Telegram

Per ricevere i dati raccolti dal keylogger, devi creare un bot Telegram personale e ottenere due informazioni importanti:

- **Bot Token** (fornito da `@BotFather`)
- **User ID** (il tuo ID univoco su Telegram)


## 🔧 Passaggi per configurare il bot

### 1. Crea un nuovo bot su Telegram
- Apri Telegram e cerca **@BotFather**
- Invia il comando `/newbot` e segui le istruzioni
- Scegli un nome per il tuo bot (es. *KeyloggerBot*)
- Scegli un username (es. `mio_keylogger_bot`)
- Riceverai un token simile a questo:
```bash
123456789:ABCdefGhIJKlmnoPqrStUvwxYz123456789
```
### 2. Salva il token
- Copia il token appena ricevuto  
- Apri il file `keylogger.py`  
- Incolla il token al posto di `BOT_API_TOKEN`:
```python
BOT_API_TOKEN = "IL_TUO_TOKEN_AQUI"
```
### 3. Ottieni il tuo User ID
- Invia un messaggio al tuo nuovo bot (es. `/start`)
- Apri questo link nel browser (sostituisci `IL_TUO_TOKEN_QUI`):
```bash
https://api.telegram.org/botIL_TUO_TOKEN_AQUI/getUpdates
```
- Cerca nel testo una riga come questa:
```bash
"from":{"id":123456789,"is_bot":false,"first_name":"Mario","username":"mario123",...}
```
- Il numero dopo `"id":` è il tuo User ID (es. `123456789`)
- Apri il file keylogger.py
- Incolla il tuo `ID` al posto di `USER_ID`:
```bash
USER_ID = "IL_TUO_USER_ID_QUI"
```
Ora puoi eseguire il programma e ricevere i dati su Telegram.

# 🫣 Trasformare il file in .exe
- Possiamo trasformare il nostro file .py in un eseguibile `.exe` tramite **Nuitka**:
- Come primo passo dobbiamo installare l'apposita liberia:
```bash
py -m pip install nuitka
```
- Una volta installatele librerie possiamo compilare il file .py:
```bash
py -m nuitka --standalone --onefile --windows-disable-console keylogger.py                       
```
# 🥇 Dimostrazione - basic version:
![asmsasa](https://github.com/user-attachments/assets/c6e1e541-85bc-4fce-a26e-b7cc2f7225e0)
## 🥇 Dimostrazione - advanced version:
![IMG_3684](https://github.com/user-attachments/assets/1f261ebb-35ac-401f-9b4d-de04af366436)


**Nota:** Non mi assumo responsabilità di utilizzi illegittimi e per scopi illegali. Questo è un progetto scolastico.
