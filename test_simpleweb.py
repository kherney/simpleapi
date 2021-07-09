from api import RequestSession, API, Request, Response


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

