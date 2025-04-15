from flask import Flask, Response, request
import datetime

app = Flask(__name__)

GOOGLE_SHEETS_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxjAi_l-Kpj8rHHvwnIN32DZfgTMaq0_G7vQgiHR4ttlGJZaY_DkNCglRVQmLozL6jpOg/exec"

@app.route('/pixel_log.gif')
def pixel_log():
    # Pixel GIF transparent 1x1 (en bytes)
    pixel_bytes = (
        b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;'
    )
    
    # Exemple : log de certaines infos (optionnel)
    uid = request.args.get('uid', 'inconnu')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    timestamp = datetime.datetime.utcnow()
    print(f"[{timestamp}] Pixel chargé pour UID={uid}, IP={ip}")
    
    return Response(pixel_bytes, mimetype='image/gif')

@app.route('/pixel.gif')
def pixel():
pixel_bytes = (
        b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
        b'\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,\x00\x00'
        b'\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;'
    )

uid = request.args.get('uid', 'inconnu')
ip = request.headers.get('X-Forwarded-For', request.remote_addr)
# Envoie vers Google Sheets
try:
	requests.post(GOOGLE_SHEETS_WEBHOOK_URL, json={
		"uid": uid,
		"ip": ip
	})
except Exception as e:
	print("Erreur envoi Google Sheets:", e)
	
return Response(pixel_bytes, mimetype='image/gif')

@app.route('/')
def home():
    return "Application Flask déployée avec succès !"

if __name__ == '__main__':
    app.run(debug=True)
