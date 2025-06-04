# 🎬 JSD-60 Recovery Script

This Python script is designed to help recover the audio processor (JSD-60) at a movie theater in the event of unexpected input switching or fader level drops mid-show. It automatically checks the system status and uses Selenium to correct the input and volume levels if needed.

---

## ✅ Features

- Connects to the JSD-60's `dynamic.cgi` endpoint
- Ensures the correct input (Button 2 / Digital 8) is selected
- Ensures the fader level is above a minimum threshold (defaults to 38.0)
- Uses Selenium to interact with the JSD-60's web interface if corrections are needed
- Designed for headless operation (no UI popups)

---

## 🧰 Requirements

- Python 3.7+
- Google Chrome (headless)
- ChromeDriver installed and in PATH

### Python dependencies

Install with:
`pip install -r requirements.txt`
