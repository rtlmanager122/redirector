import json
import os
import base64
from flask import Flask, request, render_template_string, url_for

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
  <script src="{{ loader_url }}" defer data-payload="{{ script_b64 }}"></script>
</body>
</html>
"""


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def redirect_preserve(path):
    if path.startswith("static/"):
        return app.send_static_file(path[len("static/"):])

    dest = f"{DEST_HOST.rstrip('/')}/{path}"
    if request.query_string:
        dest += "?" + request.query_string.decode()

    dest_b64 = base64.b64encode(dest.encode("utf-8")).decode("ascii")
    redirect_js = f"""(function () {{
  var dest = atob({json.dumps(dest_b64)});
  setTimeout(function () {{
    window.location.replace(dest);
  }}, 5000);
}})();"""
    script_b64 = base64.b64encode(redirect_js.encode("utf-8")).decode("ascii")
    loader_url = url_for("static", filename="redirect-loader.js")
    return render_template_string(
        WAIT_HTML, script_b64=script_b64, loader_url=loader_url
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
