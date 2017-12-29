"Create a route for sending back messages from a user's session."
import arrow
import flask

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.messages", __name__)


@blueprint.route("/messages")
def get_messages():
    "Return a JSON list of string messages from `session['messages']`."
    try:
        now = arrow.get()
        messages = (x for x in flask.session["messages"]
                    if arrow.get(x[1]) > now)
        flask.session["messages"] = []
        return flask.jsonify([x[0] for x in messages])
    except KeyError:
        return flask.jsonify([])
