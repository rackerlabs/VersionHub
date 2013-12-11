from application.util import route
from application.handlers.base import BaseHandler

@route(r'/applications')
class ApplicationHandler(BaseHandler):

    def get(self):
       pass 

