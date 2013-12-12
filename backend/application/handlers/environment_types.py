from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/environment_types')
class EnvironmentTypesHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self):
        response = yield gen.Task(EnvironmentType.get_environment_types)
        self.finish(response)


class EnvironmentType(object):

    @staticmethod
    def get_environment_types(callback):
        db = Db.connect()
        db.callproc('get_environment_types');

        r = db.fetchall()
        return callback({'environment_types': r})
