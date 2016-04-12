import os
import time
import json
import logging

import tornado.gen
import tornado.web
import tornado.ioloop

from odin.http.routes.api import ApiRoute
from odin.http.routes.default import DefaultRoute

class HttpServer(object):

    def __init__(self, debug_mode=False):

        settings = {
            "static_path": os.path.abspath(os.path.join(os.path.dirname(__file__), "../static")),
            "debug" : debug_mode,
            }

        logging.debug("static_path is {}".format(settings['static_path']))

        # Create an API route
        api_route = ApiRoute()

        # Register adapters with the API route and get handlers
        api_route.register_adapter("dummy", "odin.adapters.dummy.DummyAdapter")
        handlers = api_route.get_handlers()

        # Craete a default route for static content and get handlers
        default_route = DefaultRoute()
        handlers += default_route.get_handlers()

        # Create the Tornado web application for these handlers
        self.application = tornado.web.Application(handlers, **settings)

    def listen(self, port, host=''):

        self.application.listen(port, host)