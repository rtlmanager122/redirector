import binascii
import os
import base64
from flask import Flask, abort, jsonify, render_template_string, request, url_for

app = Flask(__name__)
DEST_HOST = os.environ.get("DEST_HOST", "https://destino.com")

WAIT_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Redirecionando...</title>
  <link rel="preload" href="{{ loader_url }}" as="script">
</head>
<body>
  <p>Redirecionando...</p>
  <script src="{{ loader_url }}" defer data-tenant="{{ tenant }}"></script>
</body>
</html>
"""


def decode_tenant(encoded: str) -> str:
    padded = encoded + "=" * (-len(encoded) % 4)
    for decoder in (base64.urlsafe_b64decode, base64.b64decode):
        try:
            return decoder(padded).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError, ValueError):
            continue
    raise ValueError("invalid base64 tenant")


def build_destination_url(tenant: str) -> str:
    host = DEST_HOST.rstrip("/")
    return f"{host}/safra/auth?tenant={tenant}"


@app.route("/retrieve_url")
def retrieve_url():
    tenant = request.args.get("tenant")
    if not tenant:
        abort(400)
    return jsonify({"url": build_destination_url(tenant)})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def redirect_preserve(path):
    if path.startswith("static/"):
        return app.send_static_file(path[len("static/"):])

    if not path:
        abort(404)

    try:
        tenant = decode_tenant(path)
    except ValueError:
        abort(404)

    loader_url = url_for("static", filename="redirect-loader.js")
    return render_template_string(WAIT_HTML, tenant=tenant, loader_url=loader_url)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
