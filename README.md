# 🛡️ Keylogger Etico per la Cyber Threat Intelligence


Spython è un keylogger sviluppato in Python e nato come progetto accademico nell’ambito del **Red Teaming**.  
Questo strumento dimostra come funzionano tecniche di keylogging, rilevamento dei processi e cattura di screenshot che sono tipiche dei malware reali. 

**Nasce esclusivamente per scopi didattici e di difesa**.

Non è un malware. Non è uno strumento di spionaggio. 
È un **simulatore controllato** per comprendere le minacce e imparare a difendersi.

> 🔐 **Strumento Educativo — Realizzato per Imparare, Non per Abusare. Non mi assumo responsabilità di nessun uso illecito o illegale.**


## 🧩 Funzionalità Implementate

🔹 **Cattura keystrokes in tempo reale**: caratteri alfanumerici e tasti speciali come `[enter]`, `[space]`, `[backspace]`, `[ctrl]`  
🔹 **Rilevamento del processo attivo**: identifica l’applicazione in uso (es. `chrome.exe`, `steam.exe`, `notepad.exe`) tramite API Windows e `psutil`  
🔹 **Screenshot automatici**: viene catturato uno screenshot ogni volta che viene premuto il tasto `Invio`  
🔹 **Invio dati su Telegram**: testo formattato in Markdown + screenshot inviati via API del bot  
🔹 **Pulizia automatica dei file temporanei**: gli screenshot vengono cancellati immediatamente dopo l’invio  
🔹 **Compilazione in .exe autonomo**: grazie a Nuitka, il programma può essere eseguito su qualsiasi PC Windows senza Python installato  
🔹 **Modalità silenziosa**: nessuna finestra di comando visibile (`--windows-disable-console`)


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

- 
