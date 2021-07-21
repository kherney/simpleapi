# API in webob
import os

from webob import Request, Response
from parse import parse
from inspect import isclass
from requests import Session as RequestSession
from wsgiadapter import WSGIAdapter
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise

from middleware import Middleware

# class API:
#     def __call__(self, environ, start_response, *args, **kwargs):
#         status = "200 OK"
#         response = b'Hello World cLASS'
#         start_response(status, headers=[])
#         return iter([response])


class API:
    def __init__(self, template_dir: str = 'template', static_dir: str = 'static'):
        self.env_template = Environment(loader=FileSystemLoader(os.path.abspath(template_dir)))
        self.paths = dict()
        self.handler_exception = None
        self.whitenoise = WhiteNoise(self.wsgi_app, root=static_dir)
        self.middleware = Middleware(self)

    def __call__(self, environ, start_response, *args, **kwargs):
        path_info = environ.get("PATH_INFO")

        if path_info.startswith("/static"):
            environ.update([('PATH_INFO', path_info[len('/static'):])])
            return self.whitenoise(environ, start_response)
        return self.middleware(environ, start_response)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def add_route(self, path: str, handler: object, methods_allowed=None):
        assert path not in self.paths, "Such Router already exists"
        if methods_allowed is None:
            methods_allowed = ['get', 'post', 'put', 'delete', 'options', ]

        # self.paths[path] = handler
        self.paths.update([(path, {'handler': handler, 'methods_allowed': methods_allowed, })])

    def route(self, path: str, methods_allowed=None):
        # if path not in self.paths:
        #     raise AssertionError(" Such Router already exists")
        # assert path not in self.paths, "Such Router already exists"

        def wrapper_function(handler):
            # self.paths[path] = handler
            self.add_route(path, handler, methods_allowed)
            print("return", handler)
            return handler
        return wrapper_function

    def handle_request(self, request: Request):
        response = Response()
        handler_data, kwargs = self.find_handler(request.path)

        try:
            if handler_data is not None:
                handler = handler_data.get("handler")
                methods_allowed = handler_data.get('methods_allowed')

                if isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method {} not Allowed".format(request.method))
                else:
                    if request.method.lower() not in methods_allowed:
                        raise AttributeError("Method {} not Allowed".format(request.method))

                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.handler_exception is None:
                raise e
            else:
                self.handler_exception(request, response, e)

        return response

    def find_handler(self, request_path):
        for path, handler_data in self.paths.items():
            parse_path = parse(path, request_path)
            if parse_path is not None:
                return handler_data, parse_path.named

        return None, None

    def add_exception(self, exception):
        self.handler_exception = exception

    def template(self, file_name: str, context=None):
        if context is None:
            context = dict()

        return self.env_template.get_template(file_name).render(**context)

    def add_middleware(self, middleware_cls):
        self.middleware.add(middleware_cls)

    def default_response(self, response: Response):
        response.status_code = 404
        response.text = "Not Found"

    def test_session(self, base_url: str = "http://testServer"):
        session = RequestSession()
        session.mount(base_url, WSGIAdapter(self))
        return session
