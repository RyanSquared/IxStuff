"Utility library for IxStates."
import functools
import sqlite3
import arrow
import flask
import htmlmin

minifier = htmlmin.Minifier(  # pylint: disable=invalid-name
    remove_comments=True,
    remove_empty_space=True,
    remove_all_empty_space=True)
DB_CON = sqlite3.connect("ixnay.db")


def requires_login(function):
    "Raise 403 if given a route without being logged in."
    @functools.wraps(function)
    def subfunction(*args, **kwargs):
        "-"
        if flask.session.get("uid") is None:
            flask.abort(403)
        return function(*args, **kwargs)
    return subfunction


def requires_admin(function):
    "Decorator for checking for admin status before rendering page"
    @functools.wraps(function)
    def subfunction(*args, **kwargs):
        "-"
        if not flask.session.get("admin", False):
            flask.abort(403)
        return function(*args, **kwargs)
    return subfunction


def queue_message(message):
    "Add a string message to a `session` list."
    if "messages" not in flask.session:
        flask.session["messages"] = []
    flask.session["messages"].append(
        (message, arrow.get().shift(seconds=10).datetime))
    flask.session.modified = True


def redirect(url):
    "Return a redirect for `session.url` or a default URL."
    if flask.session.get('url'):
        return flask.redirect(flask.url_for(flask.session["url"]))
    return flask.redirect(flask.url_for(url))


def render_template_noredir(template, **kwargs):
    "Render and minify a template."
    # return minifier.minify(flask.render_template(template, **kwargs))
    return flask.render_template(template, **kwargs)


def render_template(url, template, **kwargs):
    "Set a session URL variable and render a template."
    flask.session['url'] = url
    return render_template_noredir(template, **kwargs)


def executeSQL(query, args=None):  # pylint: disable=invalid-name
    "Proxy wrapper to automatically create and destroy a cursor."
    if args is None:
        args = []
    DB_CON.execute(query, args)
    DB_CON.commit()


def querySQL(query, args=None):  # pylint: disable=invalid-name
    "Proxy wrapper to wrap responses from SQL server to a dict."
    if args is None:
        args = []
    cursor = DB_CON.cursor()
    cursor.execute(query, args)
    fields = [x[0] for x in cursor.description]
    return ({fields[i]: v for i, v in enumerate(row)} for row in cursor)


executeSQL("""
CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    admin TINYINT DEFAULT 0,
    UNIQUE(username)
);""")

executeSQL("""
INSERT OR IGNORE INTO users (username, password, admin) VALUES ('RyanSquared',
'$2b$12$bGLD75o2VfH4/YbaR/NSNuolyzS1Rfukcw80P7Xhj2ygDS0HyxUcy', 1);""")
executeSQL("""
INSERT OR IGNORE INTO users (username, password, admin) VALUES ('Burgbb',
'$2b$12$bGLD75o2VfH4/YbaR/NSNuolyzS1Rfukcw80P7Xhj2ygDS0HyxUcy', 0);""")


executeSQL("""
CREATE TABLE IF NOT EXISTS posts (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    poster INTEGER NOT NULL,
    date INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    UNIQUE(poster, date)
);""")

executeSQL("""
INSERT OR IGNORE INTO posts (poster, date, title, content) VALUES (
    1, ?, 'IxRebranding', ?
);""", (arrow.get().timestamp, """
Ixnay has been a region for many years, but this fuckin bitch ass cunt
we call Heku has a tad bit of an issue and wants to start redoing some
things. The forums that are currently being used aren't a good way to
manage Ixnay, so we're moving to this new custom CMS called IxStates.
So far, here's the battle plan:

- [ ] Create the IxBlog for the index page
- [ ] Make the admin dashboard
- [ ] Write the mail/notification system
- [ ] Let users edit their stats
- [ ] Create a map request submission form
- [ ] Make admins able to approve stats changes
- [ ] Give each user a miniblog for small ICN updates
- [ ] Recreate the forums as an IxStates subapp

These steps will take a bit of time, so we at IxStaff hope no one minds as
the nation undergoes our reimagining efforts. If you'd like to help or get
more information about the rebranding and about the plans for IxStates,
feel free to join us on IRC.

Do you have an idea that can Make Ixnay Great Again? Feel free to send any
requests to **LordRyan** on the Ixnay IRC channel."""))

executeSQL("""
CREATE TABLE IF NOT EXISTS lorewards (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    giver INTEGER NOT NULL, -- Links to `users.uid`
    receiver INTEGER NOT NULL, -- Links to `users.uid`
    date INTEGER NOT NULL,
    type TINYINT NOT NULL,
    UNIQUE(date, type) -- No more than once per day
);""")

executeSQL("""
INSERT OR IGNORE INTO lorewards (giver, receiver, date, type)
VALUES (1, 1, 1513814400, 1);""")

executeSQL("""
CREATE TABLE IF NOT EXISTS mails (
    uid INTEGER PRIMARY KEY AUTOINCREMENT,
    subject VARCHAR NOT NULL,
    archived TINYINT DEFAULT 0
);""")

executeSQL("""
CREATE TABLE IF NOT EXISTS users2mails (
    mail_uid INTEGER NOT NULL,
    user_uid INTEGER NOT NULL
);""")

executeSQL("""
CREATE TABLE IF NOT EXISTS messages2mails (
    mail_uid INTEGER NOT NULL,
    user_uid INTEGER NOT NULL,
    text VARCHAR NOT NULL,
    date INTEGER NOT NULL
);""")

try:
    next(querySQL("SELECT * FROM mails;"))
except StopIteration:
    executeSQL("INSERT INTO mails (subject) VALUES ('Testing Message');")
    executeSQL("INSERT INTO users2mails (mail_uid, user_uid) VALUES (1, 1);")
    executeSQL("INSERT INTO users2mails (mail_uid, user_uid) VALUES (1, 2);")
    executeSQL("""INSERT INTO messages2mails (mail_uid, user_uid, text, date)
    VALUES (1, 2, 'Work on IxStates', 1514390239);""")
    executeSQL("""INSERT INTO messages2mails (mail_uid, user_uid, text, date)
    VALUES (1, 1, 'no u fgt', 1514390253);""")
