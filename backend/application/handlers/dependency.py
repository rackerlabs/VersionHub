from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications/{app_id}/enviornments/{env_id}/dependencies')
class DependenciesHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(app_id, env_id, self):
        response = yield gen.Task(Dependency.get_dependencies, env_id)
        self.finish(response)

    @asynchronous
    @gen.engine
    def post(app_id, env_id, self):
        dependency = self.params.get("dependency", "")

        response = yield gen.Task(Dependency.create_dependency, env_id, dependency)
        self.finish(response)

        @asynchronous
    @gen.engine
    def delete(app_id, env_id, self):
        dependency = self.params.get("dependency", "")

        response = yield gen.Task(Dependency.delete_dependency, env_id, dependency)
        self.finish(response)


class Dependency(object):

    @staticmethod
    def get_dependencies(env_id, callback):
        db = Db.connect()
        db.callproc('get_environment_dependencies', env_id);

        r = db.fetchall()
        return callback({'dependencies': r})

    @staticmethod
    def create_dependency(env_id, dependency, callback):
        db = Db.connect()
        db.callproc('create_dependency', env_id, dependency);

        return callback()

    @staticmethod
    def delete_dependency(env_id, callback):
        db = Db.connect()
        db.callproc('delete_dependency', env_id, dependency);

        return callback()
