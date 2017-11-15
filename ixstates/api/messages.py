"Create a route for sending back messages from a user's session."
try:
    import itertools.imap as map  # pylint: disable=redefined-builtin
    import itertools.ifilter as filter  # pylint: disable=redefined-builtin
except ImportError:  # Python 3
    pass
from datetime import datetime
import flask

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.messages", __name__)


@blueprint.route("/messages")
def get_messages():
    "Return a JSON list of string messages from `session['messages']`."
    try:
        now = datetime.now()
        messages = filter(
            lambda x: x[1] > now, flask.session["messages"])
        flask.session["messages"] = []
        return flask.jsonify(list(map(lambda x: x[0], messages)))
    except KeyError:
        return flask.jsonify([])
