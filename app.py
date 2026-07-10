"""Mock realtor sites for RCAI real-estate widget testing.

One Flask app, subdomain routing: <realtor>.readychatai.lat -> that realtor's
branded site (home + listing detail). Each site embeds the RCAI real-estate
chat widget for its business. Unknown/apex host -> realtor index (handy when
hitting the raw Coolify URL before DNS is wired).

Run local:  python app.py   (or gunicorn app:app)
Test a subdomain locally:  curl -H "Host: palmrealty.readychatai.lat" localhost:8000
"""

import os

from flask import Flask, abort, render_template, render_template_string, request

from data import PRESET_FIELDS, REALTORS

app = Flask(__name__)

# Widget api_keys come from the environment (not committed). Empty -> the site
# renders without the widget for that realtor.
for _key, _env in (("palmrealty", "DEV_WIDGET_KEY"), ("harborestates", "QA_WIDGET_KEY")):
    _v = os.environ.get(_env)
    if _v:
        REALTORS[_key]["api_key"] = _v


@app.template_filter("val")
def _val(v):
    return "—" if v is None or v == "" else v


def _realtor_from_host():
    host = request.headers.get("X-Forwarded-Host", request.host).split(":")[0]
    return REALTORS.get(host.split(".")[0].lower())


def _img(seed, w=800, h=560):
    # Deterministic placeholder photo per listing (external, fine on a real host).
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


def _coordline(item, r):
    """Nautical-chart coordinate line (Harbor's signature). Deterministic per
    listing, jittered around the region so each card reads like a real fix."""
    if r["brand"] != "harbor":
        return None
    h = sum(ord(c) for c in item["id"])
    lat = 41.40 + (h % 240) / 1000        # ~41.40–41.64 N (Aquidneck / East Bay)
    lon = 71.20 + ((h * 7) % 260) / 1000  # ~71.20–71.46 W
    return f"{lat:.4f}° N · {lon:.4f}° W"


WIDGET_SNIPPET = """{% if r.api_key %}<!-- ReadyChatAI Widget -->
<script>
  (function(){var s=document.createElement("script");s.src="{{ r.api_url }}/api/widget/js/";
   s.async=true;s.onload=function(){ReadyChatAI.init({apiKey:"{{ r.api_key }}",apiUrl:"{{ r.api_url }}"});};
   document.head.appendChild(s);})();
</script>{% else %}<!-- ReadyChatAI widget not wired: set api_key for "{{ r.key }}" -->{% endif %}"""


def _widget(r):
    return render_template_string(WIDGET_SNIPPET, r=r)


@app.route("/")
def home():
    r = _realtor_from_host()
    if not r:
        return render_template_string(INDEX_HTML, realtors=REALTORS.values())
    return render_template("home.html", r=r, img=_img, widget_snippet=_widget(r))


@app.route("/listing/<listing_id>")
def listing(listing_id):
    r = _realtor_from_host()
    if not r:
        abort(404)
    item = next((x for x in r["listings"] if x["id"] == listing_id), None)
    if not item:
        abort(404)
    return render_template(
        "listing.html", r=r, item=item, img=_img, preset_fields=PRESET_FIELDS,
        coordline=_coordline(item, r), widget_snippet=_widget(r),
    )


@app.route("/healthz")
def healthz():
    return "ok", 200


INDEX_HTML = """<!doctype html><html><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>RCAI Real-Estate Test Sites</title>
<style>body{font:16px system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 20px}
li{margin:8px 0}</style></head><body>
<h1>RCAI real-estate mock sites</h1>
<p>Reach a site by its subdomain (Host header), e.g. <code>palmrealty.readychatai.lat</code>.</p>
<ul>{% for r in realtors %}
<li><strong>{{ r.name }}</strong> — <code>{{ r.key }}.readychatai.lat</code>
    ({{ r.listings|length }} listings, widget: {{ 'wired' if r.api_key else 'not wired' }})</li>
{% endfor %}</ul></body></html>"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
