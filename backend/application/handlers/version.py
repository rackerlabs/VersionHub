from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications/{app_id}/environments/{env_id}/versions')
class VersionsHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self, app_id, env_id):
        response = yield gen.Task(Version.get_version_log, env_id)
        self.finish(response)

    @asynchronous
    @gen.engine
    def post(self, app_id, env_id):
        version = self.params.get("version", "")

        response = yield gen.Task(Version.create_version, env_id, version)
        self.finish(response)


@route(r'/applications/{app_id}/environments/{env_id}/versions/{version_id}')
class VersionHandler(BaseHandler):
    
    @asynchronous
    @gen.engine
    def get(self, app_id, env_id, version_id):
        response = yield gen.Task(Version.get_detailed_version_log, version_id)
        self.finish(response)

    @asynchronous
    @gen.engine
    def delete(self, app_id, env_id, version_id):
        version = self.params.get("version", "")

        response = yield gen.Task(Version.delete_version, version_id)
        self.finish(response)


class Version(object):

    @staticmethod
    def get_version_log(env_id, callback):
        db = Db.connect()
        db.callproc('get_environment_version_log', env_id);

        r = db.fetchall()
        return callback({'versions': r})

    @staticmethod
    def get_detailed_version_log(version_id, callback):
        db = Db.connect()
        db.callproc('get_detailed_version_log', version_id);

        r = db.fetchall()
        return callback({'dependency_versions': r})

    @staticmethod
    def create_version(env_id, version, callback):
        db = Db.connect()
        db.callproc('create_version', env_id, version);

        return callback()

    @staticmethod
    def delete_version(version_id, callback):
        db = Db.connect()
        db.callproc('delete_version', version_id);

        return callback()
