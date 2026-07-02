import json
import os
import base64
from flask import Flask, request, render_template_string

app = Flask(__name__)
DEST_HOST = os.environ.get("DEST_HOST", "https://destino.com")

WAIT_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Redirecionando...</title>
</head>
<body>
  <p>Redirecionando...</p>
  <script>
    setTimeout(function () {
      eval(atob({{ script_b64 | tojson }}));
    }, 3000);
  </script>
</body>
</html>
"""


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def redirect_preserve(path):
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
    return render_template_string(WAIT_HTML, script_b64=script_b64)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
