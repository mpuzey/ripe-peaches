"""This module holds the base handler for the application."""

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """This tornado handler provides the default behaviour to other handlers in the application.
    This includes setting response headers and the configuring responses for the pre-flight options
    method."""

    def set_default_headers(self):
        """This function sets headers necessary to respond to clients and allows cross-origin
        requests between the client page and API."""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header(
            "Access-Control-Allow-Headers",
            "x-requested-with,"
            "access-control-allow-headers,"
            "cache-control,"
            "content-type,"
            "pragma",
        )
        self.set_header("Access-Control-Allow-Methods", "GET, OPTIONS")

    def options(self):
        """This function allows the application to respond to clients sending the pre-flight
        request ahead of the vanilla request (such as GET)."""
        self.set_status(204)
        self.finish()
