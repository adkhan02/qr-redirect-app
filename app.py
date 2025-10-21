from flask import Flask, render_template, request
import qrcode
import os
import uuid

app = Flask(__name__)
QR_FOLDER = 'static/qr'
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_filename = None
    if request.method == 'POST':
        real_link = request.form.get('share_link')
        if real_link:
            qr = qrcode.make(real_link)
            qr_filename = f"{uuid.uuid4().hex[:8]}.png"
            qr_path = os.path.join(QR_FOLDER, qr_filename)
            qr.save(qr_path)

    return render_template('index.html', qr_filename=qr_filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
