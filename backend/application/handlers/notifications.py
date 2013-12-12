from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications/{app_id}/enviornments/{env_id}/notifications')
class NotificationsHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self, app_id, env_id):
        response = yield gen.Task(Notification.get_notifications, env_id)
        self.finish(response)


@route(r'/applications/{app_id}/enviornments/{env_id}/notifications/{notification_id}')
class NotificationHandler(BaseHandler):
    
    @asynchronous
    @gen.engine
    def put(self, app_id, env_id, notification_id):
        response = yield gen.Task(Notification.set_notification_read, notification_id)
        self.finish(response)


class Notification(object):

    @staticmethod
    def get_notification(env_id, callback):
        db = Db.connect()
        db.callproc('get_environment_noifications', env_id);

        r = db.fetchall()
        return callback({'notifications': r})

    @staticmethod
    def get_detailed_notification_log(notification_id, callback):
        db = Db.connect()
        db.callproc('set_notification_read', notification_id);

        return callback()
