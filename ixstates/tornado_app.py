"Start a Tornado webserver to serve `flask_app.app`."
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from ixstates.flask_app import app


def main():
    "Start Tornado miniserver"
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
