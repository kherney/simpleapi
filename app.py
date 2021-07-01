# App interface used by gunicorn
from api import API, Request, Response


app = API()


@app.route("/home")
def home(request: Request, response: Response):
    response.text = "Welcome to Home \n{}".format(request.environ.get("HTTP_USER_AGENT", "NO USER FOUND"))


@app.route("/about_us/{name}")
def about_us(request, response: Response, **kwargs):
    response.text = "You are {}, You're in About  Us page".format(kwargs.get('name'))
