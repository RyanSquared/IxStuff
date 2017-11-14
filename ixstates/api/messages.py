"Create a route for sending back messages from a user's session."
import itertools
import flask
from datetime import datetime

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.messages", __name__)


@blueprint.route("/messages")
def get_messages():
    "Return a JSON list of string messages from `session['messages']`."
    try:
        now = datetime.now()
        messages = itertools.ifilter(
            lambda x: x[1] > now, flask.session["messages"])
        flask.session["messages"] = []
        return flask.jsonify(list(itertools.imap(lambda x: x[0], messages)))
    except KeyError:
        return flask.jsonify([])
