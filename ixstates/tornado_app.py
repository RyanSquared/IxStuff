"Start a Tornado webserver to serve `flask_app.app`."
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from ixstates.flask_app import app


def make_server(**kwargs):
    "Start Tornado miniserver"
    return HTTPServer(WSGIContainer(app), **kwargs)
