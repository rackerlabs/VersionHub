import datetime

from tornado import gen
from tornado.web import asynchronous

from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications/{app_id}/notifications')
class NotificationsHandler(BaseHandler):

    @asynchronous
    @gen.engine
    def get(self, app_id):
        environment = self.get_argument('environment', None)
        response = yield gen.Task(Notification.get_notifications, app_id, environment)
        self.finish(response)


@route(r'/applications/{app_id}/notifications/{notification_id}')
class NotificationHandler(BaseHandler):
    
    @asynchronous
    @gen.engine
    def put(self, app_id, notification_id):
        response = yield gen.Task(Notification.set_notification_read, notification_id)
        self.finish(response)


class Notification(object):

    @staticmethod
    def get_notifications(app_id, environment, callback):
        db = Db.connect()
        db.callproc('get_environment_noifications', app_id);

        r = db.fetchall()
        if environment is not None:
            r = [x for x in r if x['environment_type'].lower() == environment.lower()]
        for l in r:
            for k, v in l.items():
                l[k] = v.isoformat() if isinstance(v, datetime.datetime) or isinstance(v, datetime.date) else v
        return callback({'notifications': r})

    @staticmethod
    def get_detailed_notification_log(notification_id, callback):
        db = Db.connect()
        db.callproc('set_notification_read', notification_id);

        return callback()
