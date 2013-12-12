from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications/{app_id}/dependencies')
class DependenciesHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self, app_id):
        environment = self.get_argument('environment', None)
        response = yield gen.Task(Dependency.get_dependencies, app_id, environment)
        self.finish(response)

    @asynchronous
    @gen.engine
    def post(self, app_id):
        dependency = self.params.get("dependency", "")

        response = yield gen.Task(Dependency.create_dependency, app_id, dependency)
        self.finish(response)

    @asynchronous
    @gen.engine
    def delete(self, app_id):
        dependency = self.params.get("dependency", "")

        response = yield gen.Task(Dependency.delete_dependency, app_id, dependency)
        self.finish(response)


class Dependency(object):

    @staticmethod
    def get_dependencies(app_id, environment, callback):
        db = Db.connect()
        db.callproc('get_environment_dependencies', app_id);

        r = db.fetchall()
        if environment is not None:
            r = [x for x in r if x['environment_type'].lower() == environment.lower()]

        return callback({'dependencies': r})

    @staticmethod
    def create_dependency(app_id, dependency, callback):
        db = Db.connect()
        db.callproc('create_dependency', app_id, dependency);

        return callback()

    @staticmethod
    def delete_dependency(app_id, callback):
        db = Db.connect()
        db.callproc('delete_dependency', app_id, dependency);

        return callback()
