import os
from flask import Flask, redirect, request, render_template_string
from urllib.parse import quote

app = Flask(__name__)
DEST_HOST = os.environ.get("DEST_HOST", "https://destino.com")

WAIT_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="10;url={{ dest }}">
  <title>Redirecionando...</title>
</head>
<body>
  <p>Redirecionando em 10 segundos...</p>
  <p><a href="{{ dest }}">Clique aqui se não for redirecionado</a></p>
</body>
</html>
"""

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def redirect_preserve(path):
    dest = f"{DEST_HOST.rstrip('/')}/{path}"
    if request.query_string:
        dest += "?" + request.query_string.decode()
    return render_template_string(WAIT_HTML, dest=dest)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)