"Creates blueprints from submodules and create a Flask app."
import flask
import ixstates.ui.index
import ixstates.api.messages
import ixstates.api.user_management

app = flask.Flask(__name__)  # pylint: disable=invalid-name
app.config['appname'] = "IxStates"
with open("/dev/random") as f:
    app.secret_key = f.read(24)

app.register_blueprint(ixstates.ui.index.blueprint)

app.register_blueprint(ixstates.api.messages.blueprint, url_prefix="/api")
app.register_blueprint(
    ixstates.api.user_management.blueprint, url_prefix="/api")
