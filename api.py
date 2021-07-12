# API in webob
from webob import Request, Response
from parse import parse
from inspect import isclass
from requests import Session as RequestSession
from wsgiadapter import WSGIAdapter

# class API:
#     def __call__(self, environ, start_response, *args, **kwargs):
#         status = "200 OK"
#         response = b'Hello World cLASS'
#         start_response(status, headers=[])
#         return iter([response])


class API:
    def __init__(self):
        self.paths = dict()

    def __call__(self, environ, start_response, *args, **kwargs):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def add_route(self, path: str, handler: object):
        assert path not in self.paths, "Such Router already exists"
        self.paths[path] = handler

    def route(self, path: str):
        # if path not in self.paths:
        #     raise AssertionError(" Such Router already exists")
        # assert path not in self.paths, "Such Router already exists"

        def wrapper_function(handler):
            # self.paths[path] = handler
            self.add_route(path, handler)
            print("return", handler)
            return handler
        return wrapper_function

    def handle_request(self, request: Request):
        response = Response()
        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            if isclass(handler):
                handler_function = getattr(handler(), request.method.lower(), None)
                if handler_function is None:
                    raise AttributeError("Method {} not implemented".format(request.method))
                handler_function(request, response, **kwargs)
            else:
                handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, request_path):
        for path, handler in self.paths.items():
            parse_path = parse(path, request_path)
            if parse_path is not None:
                return handler, parse_path.named

        return None, None

    def default_response(self, response: Response):
        response.status_code = 404
        response.text = "Not Found"

    def test_session(self, base_url: str = "http://testServer"):
        session = RequestSession()
        session.mount(base_url, WSGIAdapter(self))
        return session
