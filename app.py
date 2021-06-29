# App interface used by gunicorn
from api import API


app = API()


@app.route("/home")
def home(request, response):
    response.text = "Welcome to Home ccddd \n{}".format(request.environ.get("HTTP_USER_AGENT", "NO USER FOUND"))


@app.route("/about_us")
def about_us(request, response):
    response.text = "About  Us"
