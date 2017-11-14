"Index view for IxStates."
import flask
from ixstates import util

blueprint = flask.Blueprint('ui.index',  # pylint: disable=invalid-name
                            __name__)


@blueprint.route("/")
def index():
    "Index page."
    return util.render_template('ui.index.index', "index.html")


@blueprint.route("/login", methods=['POST'])
def login():
    "Testing logins"
    print flask.request.form
    return util.redirect('ui.index.index')
