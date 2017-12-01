"Creates blueprints from submodules and create a Flask app."
import flask
import ixstates.ui.index
import ixstates.api.messages
import ixstates.api.user_management
import markdown
from cachetools import func as functools


app = flask.Flask(__name__)  # pylint: disable=invalid-name
app.config['appname'] = "IxStates"
with open("/dev/random", "rb") as f:
    app.secret_key = f.read(24)

app.register_blueprint(ixstates.ui.index.blueprint)

app.register_blueprint(ixstates.api.messages.blueprint, url_prefix="/api")
app.register_blueprint(
    ixstates.api.user_management.blueprint, url_prefix="/api")


@app.template_filter('render_markdown')
@functools.lru_cache(maxsize=32)
def render_markdown(content):
    "Render some Markdown content to HTML."
    return markdown.markdown(content)


@app.before_request
def add_links():
    "Create a response-wide `links` variable for storing Link headers"
    flask.g.links = []


auto_translations = {  # pylint: disable=C0103
    "css": "style",
    "js": "script"
}


@app.template_global('static_link')
def static_link(filename, _as=None):
    "Add a static link and append a header for preloading"
    if _as is None:
        _as = auto_translations[filename.rpartition('.')[2]]
    flask.g.links.append((filename, _as))
    return flask.url_for('static', filename=filename)


@app.after_request
def process_links(response):
    "Create headers for preloading and attach to the response"
    for link in flask.g.links:
        url = flask.url_for('static', filename=link[0])
        _as = link[1]
        if link[1] == "font":
            # Must append crossorigin flag
            header_post = ";crossorigin"
        else:
            header_post = ""
        response.headers.add(
            'Link', "<{}>;rel=preload;as={}".format(url, _as) + header_post)
    return response
