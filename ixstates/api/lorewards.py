"Routes to manage loading and sending weekly and daily lorewards"
import arrow
import flask
from ixstates import util

blueprint = flask.Blueprint(  # pylint: disable=invalid-name
    "api.lorewards", __name__)

DAILY_QUERY = """SELECT lorewards.*,
    recv_user.username as receiver_username,
    giver_user.username as giver_username
    FROM lorewards
    LEFT JOIN users recv_user ON lorewards.receiver = recv_user.uid
    LEFT JOIN users giver_user ON lorewards.giver = giver_user.uid
    WHERE date BETWEEN ? AND ?
    AND type = ?;"""

NOTDAILY_QUERY = """SELECT lorewards.*,
    recv_user.username as receiver_username,
    giver_user.username as giver_username
    FROM lorewards
    LEFT JOIN users recv_user ON lorewards.receiver = recv_user.uid
    LEFT JOIN users giver_user ON lorewards.giver = giver_user.uid
    WHERE type = ?;"""


@blueprint.route("/lorewards/daily/<int:year>/<int:month>")
def get_daily_loreward(year, month):
    "Return the daily lorewards for a month."
    date_arrow = arrow.get(year, month, 1)
    date = date_arrow.timestamp
    new_date = date_arrow.shift(months=1).timestamp
    return flask.jsonify(list(util.querySQL(DAILY_QUERY, (date, new_date, 1))))


@blueprint.route("/lorewards/weekly")
def get_weekly_loreward():
    "Return the weekly lorewards."
    return flask.jsonify(list(util.querySQL(NOTDAILY_QUERY, (2,))))


@blueprint.route("/lorewards/monthly")
def get_monthly_loreward():
    "Return the monthly lorewards."
    return flask.jsonify(list(util.querySQL(NOTDAILY_QUERY, (3,))))


@blueprint.route("/lorewards/annual")
def get_annual_loreward():
    "Return the annual lorewards."
    return flask.jsonify(list(util.querySQL(NOTDAILY_QUERY, (4,))))
