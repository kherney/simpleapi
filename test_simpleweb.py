from api import RequestSession, API, Request, Response
from middleware import Middleware
import pytest

FILE_DIR = "css"
FILE_NAME = "main.css"
FILE_CONTENTS = "body {background-color: red}"


def _create_asset(static_dir):
    asset = static_dir.mkdir(FILE_DIR).join(FILE_NAME)
    asset.write(FILE_CONTENTS)
    return asset

def test_server_connection(api: API, client: RequestSession):
    status_expected = 200

    @api.route('/')
    def root(request: Request, response: Response):
        response.text = "hello"

    response = client.get('http://testServer/')
    assert response.status_code == status_expected


def test_home_page(api: API, client: RequestSession):
    body_response = "Hello World"
    response_expected = '{}\t{}'.format(body_response, 200)

    @api.route("/home")
    def home(request: Request, response: Response):
        response.text = response_expected

    _response = client.get('http://testServer/home')
    assert response_expected == '{}\t{}'.format(_response.text.split('\t')[0], _response.status_code)


def test_not_found_page(client: RequestSession):
    status_code_expected = 404
    response_expected = "Not Found"
    _response = client.get('http://testServer/NotFound')
    assert _response.status_code == status_code_expected
    assert _response.text == response_expected


def test_bookstore_book(api: API, client: RequestSession):
    expected_text= "Get http request"

    @api.route('/bookstore/pencil')
    class Bookstore:
        def get(self, request: Request, response: Response):
            response.text = expected_text

    _response = client.get('http://testServer/bookstore/pencil')
    assert _response.status_code == 200
    assert _response.text == expected_text


def test_parameterized_route(api: API, client:RequestSession):
    @api.route("/{name}")
    def hello(request: Request, response: Response, **kwargs):
        response.text = "hey {}".format(kwargs.get('name'))

    assert client.get("http://testServer/matthew").text == "hey matthew"
    assert client.get("http://testServer/ashley").text == "hey ashley"


def test_add_route(api: API, client: RequestSession):
    text_expected = "This is new request"

    def new_request(request: Request, response: Response, **kwargs):
        response.text = "This is new request"

    api.add_route('/newrequest', new_request)
    _response = client.get('http://testServer/newrequest')
    assert _response.status_code == 200
    assert _response.text == text_expected


def test_template(api: API, client: RequestSession):

    def index(request: Request, response: Response):
        response.body = api.template('index.html', context={'name': 'kherney', 'country': 'Colombia'}).encode()

    api.add_route('/index', index)

    _response = client.get('http://testServer/index')
    assert 'text/html' in _response.headers.get('Content-Type')
    assert 'kherney' in _response.text
    assert 'Colombia' in _response.text


def test_handles_exception(api: API, client: RequestSession):

    def handler_exception(request: Request, response: Response, exc):
        response.text = "SomeAttributeExceptions"

    def root(request: Request, response: Response):
        raise AttributeError()

    api.add_route('/', root)
    api.add_exception(handler_exception)

    _response = client.get('http://testServer/')
    assert _response.text == "SomeAttributeExceptions"


def test_assert_served(tmpdir_factory):
    static_dir = tmpdir_factory.mktemp("static")
    _create_asset(static_dir)
    api = API(static_dir=str(static_dir))
    client = api.test_session()

    response = client.get("http://testServer/static/{}/{}".format(FILE_DIR, FILE_NAME))
    assert response.status_code == 200
    assert response.text == FILE_CONTENTS


def test_midleware_methods_are_called(api: API, client: RequestSession):
    process_request_called = False
    process_response_called = False

    class CallOwnMiddleware(Middleware):

        def process_request(self, request: Request):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, request: Request, response: Response):
            nonlocal process_response_called
            process_response_called = True

    @api.route('/')
    def root(request: Request, response: Response):
        response.text = "This is Sparta !!"

    api.add_middleware(CallOwnMiddleware)
    _response = client.get('http://testServer/')
    assert _response.status_code == 200
    assert process_response_called is True
    assert process_request_called is True
