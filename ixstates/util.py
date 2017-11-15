"Utility library for IxStates."
from datetime import datetime, date, timedelta
try:
    import itertools.izip as zip  # pylint: disable=redefined-builtin
except ImportError:  # We're in Py 3
    pass
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


def querySQL(query, args=None):  # pylint: disable=invalid-name
    "Proxy wrapper to wrap responses from SQL server to a dict."
    if args is None:
        args = []
    cursor = DB_CON.cursor()
    cursor.execute(query, args)
    fields = [x[0] for x in cursor.description]
    return (dict(zip(fields, row)) for row in cursor)


executeSQL("""
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    UNIQUE(username)
);""")

executeSQL("""
INSERT INTO users (username, password) VALUES ('RyanSquared',
'$2b$12$bGLD75o2VfH4/YbaR/NSNuolyzS1Rfukcw80P7Xhj2ygDS0HyxUcy');""")

executeSQL("""
CREATE TABLE IF NOT EXISTS announcements (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    poster INTEGER NOT NULL,
    date INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL
);""")

executeSQL("""
INSERT INTO announcements (poster, date, title, content) VALUES (
    1, ?, 'IxRebranding', ?
);""", (date.today(), """
Ixnay has been a region for many years, but this fuckin bitch ass cunt
we call Heku has a tad bit of an issue and wants to start redoing some
things. The forums that are currently being used aren't a good way to
manage Ixnay, so we're moving to this new custom CMS called IxStates.
So far, here's the battle plan:

1. Create the IxBlog for the index page
2. Make the admin dashboard
3. Write the mail/notification system
4. Let users edit their stats
5. Create a map request submission form
6. Make admins able to approve stats changes
7. Give each user a miniblog for small ICN updates
8. Recreate the forums as an IxStates subapp

These steps will take a bit of time, so we at IxStaff hope no one minds as
the nation undergoes our reimagining efforts. If you'd like to help or get
more information about the rebranding and about the plans for IxStates,
feel free to join us on IRC."""))
