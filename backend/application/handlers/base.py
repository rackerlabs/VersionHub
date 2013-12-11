#!/usr/bin/env python
""" This is the base class from which all handlers should extend """

import logging
import json

from tornado import gen
from tornado.web import HTTPError
from tornado.web import RequestHandler

from application.services.auth import Auth
from application.services.base import BaseService
from application.config import config

log = logging.getLogger(__name__)


def handler_access(role):
    """Decorates things w/ restricted access"""
    def rapper(func):
        def _wrapped(self, *args, **kwargs):
            if not role in self.racker["roles"]:
                raise HTTPError(403, "You can't do that.")
            return func(self, *args, **kwargs)
        return _wrapped
    return rapper

class BaseHandler(RequestHandler):
    """
        This handles all of the setup of our requests. There are two
        interesting bits of magic done here: racker and params

        self.params: This is set to a dictionary representation of the parsed
                     json body received.

        self.racker: This is all of the information we get from auth for the
                     current racker (auth token).

    """

    def get_service_instance(self, username, region=None, catalog=None):
        """
        This method will build and apply the specific service instance needed.

        """
        args = [username, self.racker_token]
        
        if region:
            args.append(region)

        if catalog:
            args.append(catalog)
            
        return self.service_obj(*args)

    @gen.coroutine
    def prepare(self):
        """ Ensure the request is well formed json and that they are auth'd """

        #self.racker = yield gen.Task(self.ensure_login)
        self.params = self.parse_request()

    @gen.engine
    def ensure_login(self, callback):
        """ Verify the racker is logged in """
        if getattr(self, "no_auth", False):
            callback()
            return

        # Get the token from the cookie, or failing that, the header
        token = self.get_cookie('X-Auth-Token', None)
        if(token is None):
            token = self.request.headers.get('X-Auth-Token', None)
            if(token is None):
                raise HTTPError(401, "No X-Auth-Token provided")

        try:
            racker = yield gen.Task(Auth().is_racker_token_valid, token)
            racker["roles"] = [role['name'] for role in racker['roles']]
            self.racker_token = token
            callback(racker)
        except Exception as e:
            log.debug("Failed to authenticate token: ")
            log.info(e)
            raise HTTPError(401, "Unable to authenticate you")

    def parse_request(self):

        content_type = self.request.headers.get(
            "Content-Type", 'application/json')

        if self.request.body in [None, b"", ""]:
            return

        if content_type.startswith("application/json"):
            try:
                return json.loads(self.request.body.decode('utf-8'))
            except Exception:
                raise HTTPError(400, "Bad Request. Could not parse JSON")
        else:
            # Content type is something other than application/json
            raise HTTPError(415, "Unsupported Media Type")

        return {}

    def write(self, chunk):
        """ Make sure we only write json and ensure content-type is correct """
        if isinstance(chunk, dict):
            chunk = json.dumps(chunk)
            self.set_header("Content-Type", "application/json; charset=UTF-8")

        super(BaseHandler, self).write(chunk)


def no_auth(cls):
    cls.no_auth = True
    cls.get.no_auth = True
    cls.put.no_auth = True
    cls.post.no_auth = True
    cls.delete.no_auth = True
    return cls

