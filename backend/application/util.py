#!/usr/bin/env python
""" This is a catchall file for lots of stuff. It probably should be a dir """

import os
import pkgutil
import logging
import sys
import re

from optparse import OptionParser
from pkg_resources import resource_filename

import tornado.httpserver
import tornado.web
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler

from application.config import config
#from application.lib.mock import set_mock_data

log = logging.getLogger(__name__)


class route(object):
    """ Decorates RequestHandlers and builds a list of routables handlers """
    # From: https://gist.github.com/616347

    _routes = []

    def __init__(self, uri, name=None, module=None):
        self._uri = re.sub(r'{[a-z_]*}', u'([\w_\-]+)', uri) + '/?'
        self.name = name or uri
        self.module = module

    def __call__(self, _handler):
        log.info("Using {0} for {1}".format(_handler.__name__, self._uri))
        r = tornado.web.url(self._uri, _handler, name=self.name)
        r.module = self.module
        self._routes.append(r)
        return _handler

    @classmethod
    def get_routes(cls):
        """ Return a list of routes so tornado can listen for them """
        return cls._routes


def autoload(dirname):
    """ Autoload all modules in a directory """
    for path, directories, files in os.walk(dirname):
        for importer, package_name, _ in pkgutil.iter_modules([path]):
            # Supposedly, this means the module is already loaded, but that is
            # not the case for tests. It shouldn't hurt to reload them anyways.
            # if package_name not in sys.modules or True:
            importer.find_module(package_name).load_module(package_name)

def command_line_options():
    """ command line configuration """

    parser = OptionParser(usage="usage: %prog [options] <config_file>")

    parser.add_option('-d', '--debug',
                      action="store_true",
                      dest="debug",
                      default=False,
                      help="Start the application in debugging mode.")

    parser.add_option('-p', '--port',
                      action="store",
                      dest="port",
                      default=3000,
                      help="Set the port to listen to on startup.")

    parser.add_option('-a', '--address',
                      action="store",
                      dest="address",
                      default=None,
                      help="Set the address to listen to on startup. Can be a "
                      "hostname or an IPv4/v6 address.")

    parser.add_option('-m', '--mock',
                      action="store_true",
                      dest="mock",
                      default=False,
                      help="Only use Mock (fake) data")

    options, args = parser.parse_args()

    if len(args) >= 1:
        config.load_file(args[0])

    return options


def setup_logging():
    """ setup the logging system """

    base_log = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    f = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    handler.setFormatter(logging.Formatter(f))
    base_log.addHandler(handler)
    base_log.setLevel(logging.DEBUG)
    return handler


def get_routes(root, handler_path):
    """ Set up all the routes, both the JS side and the api side """
    autoload(resource_filename(handler_path, "handlers"))
    routes = route.get_routes()

    if os.path.exists(os.path.join(root, 'dist')):
        static_path = os.path.join(root, 'dist')
    else:
        static_path = os.path.join(root, '..', '..', 'frontend', 'app')
        static_path = os.path.abspath(static_path)

    log.info("Frontend path: {0}".format(static_path))

    routes.append((r'/api/docs/?', tornado.web.RedirectHandler,
                  {'url': '/api/docs/index.html'}))
    routes.append((r'/api/docs/(.*)', tornado.web.StaticFileHandler,
                  {'path': "docs"}))
    routes.append((r'/', IndexFileHandler))
    routes.append((r'/(.*)', tornado.web.StaticFileHandler,
                  {'path': static_path}))

    return routes

class IndexFileHandler(RequestHandler):
    def get(self):
        log.error(config)
        self.render(config["landing_page"])

def main(handler_path):
    """ entry point for the application """

    root = os.path.dirname(__file__)

    options = command_line_options()
    setup_logging()

    # setup the application
    log.info("Setting up the application")
    application = tornado.web.Application(
        get_routes(root, handler_path),
        debug=options.debug
    )

    # start the ioloop
    log.info("Starting the application on port 8000")
    application.listen(options.port, '0.0.0.0')
    IOLoop.instance().start()

