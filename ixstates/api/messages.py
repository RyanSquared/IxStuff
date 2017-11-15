"Create a route for sending back messages from a user's session."
from datetime import datetime
import flask

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.messages", __name__)


@blueprint.route("/messages")
def get_messages():
    "Return a JSON list of string messages from `session['messages']`."
    try:
        now = datetime.now()
        messages = (x for x in flask.session["messages"]
                    if x[1] > now)
        flask.session["messages"] = []
        return flask.jsonify([x[0] for x in messages])
    except KeyError:
        return flask.jsonify([])
