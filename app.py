# App interface used by gunicorn
from api import API, Request, Response
from middleware import Middleware


app = API()


@app.route("/home")
def home(request: Request, response: Response):
    response.text = "Welcome to Home \n{}".format(request.environ.get("HTTP_USER_AGENT", "NO USER FOUND"))


@app.route("/about_us/{name}")
def about_us(request, response: Response, **kwargs):
    response.text = "You are {}, You're in About  Us page".format(kwargs.get('name'))


@app.route('/bookstore/book')
class BaseRequest:
    def get(self, request: Request, response: Response):
        response.text = "Simple get Request"

    def post(self, request: Request, response: Response):
        response.text = "Update Book by post method"

    def put(self, request: Request, response: Response):
        response.text = "PUt method for book method"


class CustomMiddleware(Middleware):

    def process_request(self, request: Request):
        message = "[{}] Processing request {} ".format(request.date, request.url)
        print(message)

    def process_response(self, request: Request, response: Response):
        message = "[{}] Processing response {} ".format(request.date, request.url)
        print(message)


def index(request: Request, response: Response, **kwargs):
    response.body = app.template('index.html', context={'name': 'Kevin', 'country': 'Colombia'}).encode()


def custom_exeptions(request: Request, response: Response, exception_cls):
    response.text = str(exception_cls)


app.add_exception(custom_exeptions)
app.add_route('/index', index)
app.add_middleware(CustomMiddleware)
