"Index view for IxStates."
import flask
from ixstates import util

blueprint = flask.Blueprint('ui.index',  # pylint: disable=invalid-name
                            __name__)

APP_QUERY = ("SELECT * FROM announcements LEFT JOIN users ON "
             "announcements.poster = users.uid ORDER BY announcements.date;")


@blueprint.route("/")
def index():
    "Index page."
    announcements = util.querySQL(APP_QUERY)
    return util.render_template('ui.index.index', "index.html",
                                announcements=announcements)
