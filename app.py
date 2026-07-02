import os
from flask import Flask, redirect, request
from urllib.parse import urljoin
app = Flask(__name__)
DEST_HOST = os.environ.get("DEST_HOST", "https://destino.com")
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def redirect_preserve(path):
    # Monta: https://destino.com/safra/auth?tenant=xxx
    dest = f"{DEST_HOST.rstrip('/')}/{path}"
    if request.query_string:
        dest += "?" + request.query_string.decode()
    return redirect(dest, code=302)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)