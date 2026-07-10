"""Mock realtor sites for RCAI real-estate widget testing.

One Flask app, subdomain routing: <realtor>.readychatai.lat -> that realtor's
site (home + listing detail). Each site embeds the RCAI real-estate chat widget
for its business (config in data.py). Unknown/apex host -> realtor index (handy
when hitting the raw Coolify URL before DNS is wired).

Run local:  FLASK_APP=app flask run  (or gunicorn app:app)
Test a subdomain locally:  curl -H "Host: palmrealty.readychatai.lat" localhost:8000
"""

import os

from flask import Flask, abort, render_template_string, request

from data import PRESET_FIELDS, REALTORS

app = Flask(__name__)

# Widget api_keys come from the environment (not committed). Empty -> site
# renders without the widget for that realtor.
for _key, _env in (("palmrealty", "DEV_WIDGET_KEY"), ("harborestates", "QA_WIDGET_KEY")):
    _v = os.environ.get(_env)
    if _v:
        REALTORS[_key]["api_key"] = _v


def _realtor_from_host():
    host = request.headers.get("X-Forwarded-Host", request.host).split(":")[0]
    label = host.split(".")[0].lower()
    return REALTORS.get(label)


def _img(seed, w=800, h=560):
    # Deterministic placeholder photo per listing (external, fine on a real host).
    return f"https://picsum.photos/seed/{seed}/{w}/{h}"


@app.route("/")
def home():
    r = _realtor_from_host()
    if not r:
        return render_template_string(INDEX_HTML, realtors=REALTORS.values())
    return render_template_string(HOME_HTML, r=r, img=_img)


@app.route("/listing/<listing_id>")
def listing(listing_id):
    r = _realtor_from_host()
    if not r:
        abort(404)
    item = next((x for x in r["listings"] if x["id"] == listing_id), None)
    if not item:
        abort(404)
    return render_template_string(
        LISTING_HTML, r=r, item=item, img=_img, preset_fields=PRESET_FIELDS
    )


@app.route("/healthz")
def healthz():
    return "ok", 200


# --- widget embed (rendered only when api_key is set) --------------------------
WIDGET_SNIPPET = """
{% if r.api_key %}
<!-- ReadyChatAI Widget -->
<script>
  (function() {
    var s = document.createElement("script");
    s.src = "{{ r.api_url }}/api/widget/js/";
    s.async = true;
    s.onload = function() {
      ReadyChatAI.init({ apiKey: "{{ r.api_key }}", apiUrl: "{{ r.api_url }}" });
    };
    document.head.appendChild(s);
  })();
</script>
{% else %}
<!-- ReadyChatAI widget not wired: set api_key for "{{ r.key }}" in data.py -->
{% endif %}
"""

BASE_CSS = """
:root{--accent:{{ r.accent }};--accent-dark:{{ r.accent_dark }};}
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1a1a;background:#f7f7f5}
a{color:var(--accent-dark);text-decoration:none}
header{background:var(--accent);color:#fff;padding:20px 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
header .brand{font-size:1.4rem;font-weight:700}
header .tag{opacity:.9;font-size:.9rem}
header .contact{font-size:.85rem;text-align:right;opacity:.95}
header a{color:#fff}
.wrap{max-width:1120px;margin:0 auto;padding:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.card{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08);display:flex;flex-direction:column}
.card img{width:100%;height:190px;object-fit:cover;display:block;background:#e6e6e6}
.card .body{padding:14px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card h3{margin:0;font-size:1.05rem}
.price{color:var(--accent-dark);font-weight:700;font-size:1.1rem}
.meta{color:#555;font-size:.88rem}
.badge{display:inline-block;font-size:.7rem;text-transform:uppercase;letter-spacing:.04em;padding:2px 8px;border-radius:999px;font-weight:700}
.badge.active{background:#e5f6f2;color:var(--accent-dark)}
.badge.pending{background:#fff3cd;color:#8a6d00}
.badge.sold{background:#f2dede;color:#a33}
.badge.rent{background:#e8eef7;color:var(--accent-dark)}
footer{color:#888;font-size:.8rem;text-align:center;padding:32px 16px}
/* listing detail */
.detail{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08)}
.detail img{width:100%;max-height:460px;object-fit:cover}
.detail .pad{padding:24px}
.detail h1{margin:.2em 0}
dl.fields{display:grid;grid-template-columns:auto 1fr;gap:8px 20px;margin:16px 0}
dl.fields dt{color:#666;font-weight:600}
dl.fields dd{margin:0}
.section-title{margin-top:24px;font-size:1rem;text-transform:uppercase;letter-spacing:.05em;color:var(--accent-dark)}
.extra dt{color:#a05a00}
.back{display:inline-block;margin-bottom:14px}
"""

HEADER_HTML = """
<header>
  <div>
    <div class="brand">{{ r.name }}</div>
    <div class="tag">{{ r.tagline }} · {{ r.city }}</div>
  </div>
  <div class="contact">
    <a href="tel:{{ r.phone }}">{{ r.phone }}</a><br>
    <a href="mailto:{{ r.email }}">{{ r.email }}</a>
  </div>
</header>
"""


def _val(v):
    return "—" if v is None or v == "" else v


app.jinja_env.filters["val"] = _val


HOME_HTML = (
    "<!doctype html><html><head><meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>{{ r.name }} — Listings</title><style>" + BASE_CSS + "</style>"
    + WIDGET_SNIPPET +
    "</head><body>" + HEADER_HTML +
    """
    <div class="wrap">
      <div class="grid">
        {% for it in r.listings %}
        <a class="card" href="/listing/{{ it.id }}">
          <img src="{{ img(it.id) }}" alt="{{ it.title }}">
          <div class="body">
            <div>
              {% set lt = it.fields.get('Listing Type') %}
              {% if it.status == 'sold' %}<span class="badge sold">Sold</span>
              {% elif it.status == 'pending' %}<span class="badge pending">Pending</span>
              {% elif lt == 'For Rent' %}<span class="badge rent">For Rent</span>
              {% else %}<span class="badge active">For Sale</span>{% endif %}
            </div>
            <h3>{{ it.title }}</h3>
            <div class="price">{{ it.price }}</div>
            <div class="meta">
              {{ it.fields.get('Bedrooms')|val }} bd · {{ it.fields.get('Bathrooms')|val }} ba ·
              {{ it.fields.get('Square Footage')|val }} sqft · {{ it.fields.get('Property Type')|val }}
            </div>
            <div class="meta">{{ it.fields.get('Address')|val }}</div>
          </div>
        </a>
        {% endfor %}
      </div>
    </div>
    <footer>Mock site for RCAI widget testing — {{ r.name }}. Not a real brokerage.</footer>
    </body></html>
    """
)


LISTING_HTML = (
    "<!doctype html><html><head><meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>{{ item.title }} — {{ r.name }}</title><style>" + BASE_CSS + "</style>"
    + WIDGET_SNIPPET +
    "</head><body>" + HEADER_HTML +
    """
    <div class="wrap">
      <a class="back" href="/">← All listings</a>
      <div class="detail">
        <img src="{{ img(item.id, 1200, 640) }}" alt="{{ item.title }}">
        <div class="pad">
          <div>
            {% if item.status == 'sold' %}<span class="badge sold">Sold</span>
            {% elif item.status == 'pending' %}<span class="badge pending">Pending</span>
            {% elif item.fields.get('Listing Type') == 'For Rent' %}<span class="badge rent">For Rent</span>
            {% else %}<span class="badge active">For Sale</span>{% endif %}
          </div>
          <h1>{{ item.title }}</h1>
          <div class="price">{{ item.price }}</div>
          <p>{{ item.desc }}</p>

          <div class="section-title">Property details</div>
          <dl class="fields">
            {% for f in preset_fields %}
            <dt>{{ f }}</dt><dd>{{ item.fields.get(f)|val }}</dd>
            {% endfor %}
          </dl>

          {% if item.extra %}
          <div class="section-title">Additional information</div>
          <dl class="fields extra">
            {% for k, v in item.extra.items() %}
            <dt>{{ k }}</dt><dd>{{ v|val }}</dd>
            {% endfor %}
          </dl>
          {% endif %}
        </div>
      </div>
    </div>
    <footer>Mock site for RCAI widget testing — {{ r.name }}. Not a real brokerage.</footer>
    </body></html>
    """
)


INDEX_HTML = """
<!doctype html><html><head><meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>RCAI Real-Estate Test Sites</title>
<style>body{font:16px system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 20px}
li{margin:8px 0}</style></head><body>
<h1>RCAI real-estate mock sites</h1>
<p>Reach a site by its subdomain (Host header), e.g. <code>palmrealty.readychatai.lat</code>.</p>
<ul>
{% for r in realtors %}
<li><strong>{{ r.name }}</strong> — <code>{{ r.key }}.readychatai.lat</code>
    ({{ r.listings|length }} listings, widget: {{ 'wired' if r.api_key else 'not wired' }})</li>
{% endfor %}
</ul></body></html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
