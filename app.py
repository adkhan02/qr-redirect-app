from flask import Flask, render_template, request, redirect
import qrcode
import os
import uuid

app = Flask(__name__)
QR_FOLDER = 'static/qr'
os.makedirs(QR_FOLDER, exist_ok=True)

redirect_map = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_filename = None
    if request.method == 'POST':
        real_link = request.form.get('share_link')
        if real_link:
            short_id = str(uuid.uuid4())[:8]
            redirect_map[short_id] = real_link

            qr_url = request.host_url + 'go/' + short_id
            qr = qrcode.make(qr_url)
            qr_filename = f"{short_id}.png"
            qr.save(os.path.join(QR_FOLDER, qr_filename))

    return render_template('index.html', qr_filename=qr_filename)

@app.route('/go/<short_id>')
def go(short_id):
    if short_id in redirect_map:
        return redirect(redirect_map[short_id], code=302)
    return "Invalid or expired link", 404

# ✅ This line starts the Flask server
if __name__ == '__main__':
    app.run(debug=True)