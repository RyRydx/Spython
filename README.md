# 🛡️ Keylogger Etico per la Cyber Threat Intelligence


Spython è un keylogger sviluppato in Python e nato come progetto accademico nell’ambito del **Red Teaming**.  
Questo strumento dimostra come funzionano tecniche di keylogging, rilevamento dei processi e cattura di screenshot che sono tipiche dei malware reali. 

**Nasce esclusivamente per scopi didattici e di difesa**.

Non è un malware. Non è uno strumento di spionaggio. 
È un **simulatore controllato** per comprendere le minacce e imparare a difendersi.

> 🔐 **Strumento Educativo — Realizzato per Imparare, Non per Abusare. Non mi assumo responsabilità di nessun uso illecito o illegale.**

---

## 🧩 Funzionalità Implementate

🔹 **Cattura keystrokes in tempo reale**: caratteri alfanumerici e tasti speciali come `[enter]`, `[space]`, `[backspace]`, `[ctrl]`
🔹 **Rilevamento del processo attivo**: identifica l’applicazione in uso (es. `chrome.exe`, `steam.exe`, `notepad.exe`) tramite API Windows e `psutil`
🔹 **Screenshot automatici**: viene catturato uno screenshot ogni volta che viene premuto il tasto `Invio`
🔹 **Invio dati su Telegram**: testo formattato in Markdown + screenshot inviati via API del bot
🔹 **Pulizia automatica dei file temporanei**: gli screenshot vengono cancellati immediatamente dopo l’invio
🔹 **Compilazione in .exe autonomo**: grazie a Nuitka, il programma può essere eseguito su qualsiasi PC Windows senza Python installato
🔹 **Modalità silenziosa**: nessuna finestra di comando visibile (`--windows-disable-console`)

---

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
