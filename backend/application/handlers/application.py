from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications')
class ApplicationsHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self):
        response = yield gen.Task(Application.get_all_applications)
        self.finish(response)

    @asynchronous
    @gen.engine
    def post(self):
        details = {
            "name": self.params.get("name", ""),
            "description": self.params.get("description", ""),
            "github": self.params.get("github", ""),
            "contact_email": self.params.get("contact_email", "")
        }
        response = yield gen.Task(Application.create_application, details)
        self.finish(response)

@route(r'/applications/{app_id}')
class ApplicationHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self, app_id):
        response = yield gen.Task(Application.get_application, app_id)
        self.finish(response)

    @asynchronous
    @gen.engine
    def put(self, app_id):
        details = {
            "name": self.params.get("name", ""),
            "description": self.params.get("description", ""),
            "github": self.params.get("github", ""),
            "contact_email": self.params.get("contact_email", "")
        }
        response = yield gen.Task(Application.update_application, app_id, details)
        self.finish(response)

    @asynchronous
    @gen.engine
    def delete(self, app_id):
        response = yield gen.Task(Application.delete_application, app_id)
        self.finish(response)



class Application(object):

    @staticmethod
    def get_all_applications(callback):
        db = Db.connect()
        db.callproc('get_all_applications');

        r = db.fetchall()
        return callback({'applications': r})

    @staticmethod
    def get_application(app_id, callback):
        db = Db.connect()
        db.callproc('get_application', app_id);

        r = db.fetchall()
        return callback({'application': r})

    @staticmethod
    def create_application(details, callback):
        db = Db.connect()
        db.callproc('create_application', 
            details["name"], 
            details["description"], 
            details["github"], 
            details["contact_email"]);

        #Only returns id
        r = db.fetchall()
        return callback({'application': r})

    @staticmethod
    def update_application(app_id, details, callback):
        db = Db.connect()
        db.callproc('update_application', 
            app_id,
            details["name"], 
            details["description"], 
            details["github"], 
            details["contact_email"]);

        #returns nothing
        return callback()

    @staticmethod
    def delete_application(app_id, callback):
        db = Db.connect()
        db.callproc('delete_application', app_id);

        return callback()
