# simple server with wsgiref package
from wsgiref.simple_server import make_server
from swgi import ReverseMiddleware, application

if __name__ == '__main__':
    server = make_server('localhost', 9068, app=application)
    # reverse response with Middleware
    # server = make_server('localhost', 8000, app=ReverseMiddleware(application))
    server.serve_forever()
