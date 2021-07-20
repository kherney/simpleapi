from webob import Request, Response


class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response, *args, **kwargs):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)

    def add(self, middleware_cls):
        self.app = middleware_cls(self.app)

    def process_request(self, request: Request):
        pass

    def process_response(self, request: Request, response: Response):
        pass

    def handle_request(self, request: Request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)
        return response
