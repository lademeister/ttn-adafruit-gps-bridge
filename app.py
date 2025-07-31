from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route('/ttn', methods=['POST'])
def ttn_webhook():
    data = request.get_json()
    decoded = data.get("uplink_message", {}).get("decoded_payload", {})

    lat = None
    lon = None

    # Suche nach einem Schlüssel mit Latitude und Longitude
    for key, val in decoded.items():
        if isinstance(val, dict) and "latitude" in val and "longitude" in val:
            lat = val["latitude"]
            lon = val["longitude"]
            break

    if lat is None or lon is None:
        return {"error": "No GPS coordinates found in decoded payload"}, 400

    aio_user = os.getenv("ADAFRUIT_USER")
    aio_key = os.getenv("ADAFRUIT_KEY")
    aio_feed = os.getenv("ADAFRUIT_FEED")

    if not aio_user or not aio_key or not aio_feed:
        return {"error": "Adafruit environment variables not set"}, 500

    url = f"https://io.adafruit.com/api/v2/{aio_user}/feeds/{aio_feed}/data"
    headers = {
        "X-AIO-Key": aio_key,
        "Content-Type": "application/json"
    }
    payload = {
        "lat": lat,
        "lon": lon
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code not in (200, 201):
        return {"error": f"Failed to send to Adafruit, status {r.status_code}"}, 500

    return {"message": "OK"}, 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
