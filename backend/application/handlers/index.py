from application.db.db import Db
from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications')
class ApplicationHandler(BaseHandler):

    def get(self):
        db = Db.connect()
        db.callproc('get_all_applications');

        r = db.fetchall()
        print(r)

        self.finish(r)

