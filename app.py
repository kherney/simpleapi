# App interface used by gunicorn
from api import API, Request, Response


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


def index(request: Request, response: Response, **kwargs):
    response.body = app.template('index.html', context={'name': 'Kevin', 'country': 'Colombia'}).encode()


app.add_route('/index', index)
