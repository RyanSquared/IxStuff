"Routes for managing mail"
import flask
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.mail", __name__)


@blueprint.route("/mail/send", methods=["POST"])
def send():
    "Send a message to another user"
    # ::TODO:: do
    return util.redirect("ui.mail.index")


@blueprint.route("/mail/new", methods=["POST"])
def new():
    "Start a new mail conversation"
    # ::TODO:: do
    return util.redirect("ui.mail.index")
