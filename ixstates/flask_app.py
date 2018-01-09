"Creates blueprints from submodules and create a Flask app."
import flask
import ixstates.ui.errors
import ixstates.ui.index
import ixstates.ui.admin
import ixstates.ui.mail
import ixstates.api.admin
import ixstates.api.blog
import ixstates.api.mail
import ixstates.api.messages
import ixstates.api.user_management
import ixstates.api.lorewards
from cachetools import func as functools
import markdown
import markdown.extensions.tables
import gfm


app = flask.Flask(__name__)  # pylint: disable=invalid-name
md = markdown.Markdown(extensions=[  # pylint: disable=invalid-name
    gfm.AutolinkExtension(), gfm.AutomailExtension(),
    gfm.HiddenHiliteExtension(), gfm.SemiSaneListExtension(),
    gfm.SpacedLinkExtension(), gfm.StrikethroughExtension(),
    gfm.TaskListExtension(), markdown.extensions.tables.TableExtension()])
app.config['appname'] = "IxStates"
with open("/dev/random", "rb") as f:
    app.secret_key = f.read(24)

app.register_blueprint(ixstates.ui.index.blueprint)
app.register_blueprint(ixstates.ui.admin.blueprint, url_prefix="/admin")
app.register_blueprint(ixstates.ui.errors.blueprint, url_prefix="/errors")
app.register_blueprint(ixstates.ui.mail.blueprint, url_prefix="/mail")

app.register_blueprint(ixstates.api.admin.blueprint, url_prefix="/api")
app.register_blueprint(ixstates.api.blog.blueprint, url_prefix="/api")
app.register_blueprint(ixstates.api.mail.blueprint, url_prefix="/api")
app.register_blueprint(ixstates.api.messages.blueprint, url_prefix="/api")
app.register_blueprint(
    ixstates.api.user_management.blueprint, url_prefix="/api")
app.register_blueprint(ixstates.api.lorewards.blueprint, url_prefix="/api")


@app.template_filter('render_markdown')
@functools.lru_cache(maxsize=32)
def render_markdown(content):
    "Render some Markdown content to HTML."
    return md.convert(content)


@app.route("/render_markdown", methods=["POST"])
def render_markdown_route():
    "Render Markdown and return the data."
    # Check if a user is logged in; this is the only time when the Markdown
    # preview should matter
    if flask.session.get("uid") is None:
        return ""
    return render_markdown(flask.request.form.get("content", ""))


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
    filepath = flask.url_for('static', filename=filename)
    flask.g.links.append((filepath, _as))
    return filepath


@app.template_global('cors_link')
def cors_link(url, _as=None):
    "Add a CORS link and append a header for preloading"
    if _as is None:
        _as = auto_translations[url.rpartition('.')[2]]
    flask.g.links.append((url, _as))
    return url


@app.after_request
def process_links(response):
    "Create headers for preloading and attach to the response"
    for link in flask.g.links:
        uri = link[0]
        _as = link[1]
        if link[1] == "font":
            # Must append crossorigin flag
            header_post = ";crossorigin"
        else:
            header_post = ""
        response.headers.add(
            'Link', "<{}>;rel=preload;as={}".format(uri, _as) + header_post)
    return response
