"Utility library for IxStates."
from datetime import datetime, timedelta
import itertools
import sqlite3
import flask

DB_CON = sqlite3.connect(":memory:", check_same_thread=False)


def queue_message(message):
    "Add a string message to a `session` list."
    if "messages" not in flask.session:
        flask.session["messages"] = []
    flask.session["messages"].append(
        (message, datetime.now() + timedelta(seconds=10)))
    flask.session.modified = True


def redirect(url):
    "Return a redirect for `session.url` or a default URL."
    if flask.session.get('url'):
        return flask.redirect(flask.url_for(flask.session["url"]))
    return flask.redirect(flask.url_for(url))


def render_template(url, template, **kwargs):
    "Set a session URL variable and render a template."
    flask.session['url'] = url
    return flask.render_template(template, **kwargs)


def executeSQL(query, args=None):  # pylint: disable=invalid-name
    "Proxy wrapper to automatically create and destroy a cursor."
    if args is None:
        args = []
    cursor = DB_CON.cursor()
    cursor.execute(query, args)


def querySQL(query, args):  # pylint: disable=invalid-name
    "Proxy wrapper to wrap responses from SQL server to a dict."
    cursor = DB_CON.cursor()
    cursor.execute(query, args)
    fields = [x[0] for x in cursor.description]
    return (dict(itertools.izip(fields, row)) for row in cursor)


executeSQL("""
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    UNIQUE(username)
);""")
