# A swgi demo interface server
class ReverseMiddleware:
    def __init__(self, app):
        self.wrapped_app = app

    def __call__(self, env_var, start_response, *args, **kwargs):
        wrapped_app_response = self.wrapped_app(env_var, start_response)
        return [r[:: -1] for r in wrapped_app_response]


def application(env_var, start_response):
    resp_body =[
        '{}: {}'.format(key, value) for key, value in env_var.items()
    ]
    resp_body = '\n'.join(resp_body)
    status = "200 OK"
    header_response = [('Content-type', 'text/plain')]
    start_response(status, header_response)

    return [resp_body.encode('utf-8')]
