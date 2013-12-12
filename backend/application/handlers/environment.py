from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications/{app_id}/environments')
class EnvironmentsHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def post(app_id, self):
        details = {
            "environment_type": self.params.get("environment_type", ""),
            "endpoint": self.params.get("endpoint", "")
        }
        response = yield gen.Task(Environment.create_environment, app_id, details)
        self.finish(response)

@route(r'/applications/{app_id}/environments/{env_id}')
class EnvironmentHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def put(app_id, env_id, endpoint, self):
        response = yield gen.Task(Environment.update_environment, env_id, endpoint)
        self.finish(response)

    @asynchronous
    @gen.engine
    def delete(app_id, env_id, self):
        response = yield gen.Task(Environment.delete_environment, env_id)
        self.finish(response)



class Environment(object):

    @staticmethod
    def create_environment(app_id, details, callback):
        db = Db.connect()
        db.callproc('create_environment', 
            app_id,
            details["environment_type"], 
            details["endpoint"]);

        return callback()

    @staticmethod
    def update_environment(env_id, endpoing, callback):
        db = Db.connect()
        db.callproc('update_environment', 
            env_id,
            endpoint);

        return callback()

    @staticmethod
    def delete_environment(env_id, callback):
        db = Db.connect()
        db.callproc('delete_environment', env_id);

        return callback()
