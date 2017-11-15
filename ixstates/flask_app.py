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
