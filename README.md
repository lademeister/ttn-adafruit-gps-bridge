# TTN to Adafruit IO Bridge for GPS tracker

Empfängt TTN Webhook Uplinks mit Latitude/Longitude und sendet sie an Adafruit.io Feed.

## Deployment

1. GitHub Repo erstellen und Dateien hochladen (app.py, requirements.txt)
2. Render.com Webservice erstellen mit:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
3. Setze Environment Variables in Render:
   - ADAFRUIT_USER=dein Adafruit IO Benutzername (z.B. Lademeister)
   - ADAFRUIT_KEY=dein Adafruit IO Key
   - ADAFRUIT_FEED=location-ttn
4. TTN Konsole:
   - Application → Integrations → Webhooks → Custom Webhook hinzufügen
   - Base URL: `https://<your-render-service>.onrender.com/ttn`
   - POST-Methode, kein Body-Template
5. Adafruit IO:
   - Feed `location-ttn` anlegen (oder wahlweise anderen Namen, oder bestehender Feed)
   - Map Block im Dashboard anlegen folls noch nciht vorhandne, Feed hinzufügen, Spur aktivieren falls gewünscht

## Hinweis

- Die Payload muss im TTN decoded_payload die Felder `latitude` und `longitude` enthalten.
- Der Service gibt HTTP 200 zurück bei Erfolg.
