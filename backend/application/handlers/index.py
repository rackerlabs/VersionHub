from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications')
class ApplicationHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self):
        response = yield gen.Task(Application.get_all_applications)
        self.finish(response)


class Application(object):

    @staticmethod
    def get_all_applications(callback):
        db = Db.connect()
        db.callproc('get_all_applications');

        r = db.fetchall()
        return callback({'applications': r})

