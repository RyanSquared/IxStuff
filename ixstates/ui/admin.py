"Admin views for IxStates."
import sqlite3
import arrow
import flask
from ixstates import util

blueprint = flask.Blueprint('ui.admin',  # pylint: disable=invalid-name
                            __name__)


@blueprint.route("/")
@util.requires_admin
def index():
    "Admin control panel page."
    # ::TODO:: make nations table
    nations = (x["username"] for x
               in util.querySQL("SELECT username FROM users"))
    nonadmin_users = util.querySQL(
        "SELECT uid, username FROM users WHERE admin != 1")
    date = arrow.get().format("YYYY-MM-DD")
    return util.render_template('ui.admin.index', "admin.html",
                                nations=nations, date=date,
                                nonadmin_users=list(nonadmin_users))


INSERT_QUERY = """INSERT INTO lorewards (giver, receiver, date, type)
    VALUES (?, ?, ?, ?);"""
MAPPING = {
    "daily": 1,
    "weekly": 2,
    "monthly": 3,
    "annual": 4
}


@blueprint.route("/submit/loreward", methods=["POST"])
@util.requires_admin
def submit_loreward():
    "Form submit page for lorewards form."
    date = arrow.get(flask.request.form["lw_date"], "YYYY-MM-DD")
    nation = flask.request.form["lw_nation"]
    _type = MAPPING[flask.request.form["lw_type"]]
    if _type >= 2:
        # Shift down day of week for weekly
        date = date.shift(days=-(date.weekday() - 1))
    if _type >= 3:
        # Shift down day of month
        date = date.replace(day=1)
    if _type >= 4:
        # Shift down month
        date = date.replace(month=1)
    # ::TODO:: make nations table instead of poll users
    # Check for nation existing in nations table
    nations = util.querySQL(
        """SELECT uid, username FROM users WHERE username LIKE ?""",
        (nation,))
    try:
        nation = next(nations)
        util.executeSQL(
            INSERT_QUERY,
            (flask.session["uid"], nation["uid"], date.timestamp, _type))
        # ::TODO:: make nations table
        util.queue_message("Added loreward for %r." % nation["username"])
    except StopIteration:
        # Nation didn't exist, flash message
        util.queue_message("Nation %r did not exist. Please select a valid"
                           " nation." % nation)
        return util.redirect("ui.admin.index")
    except sqlite3.IntegrityError:
        util.queue_message("Unable to create/overwrite loreward for %r" %
                           nation["username"])
    return util.redirect("ui.admin.index")
