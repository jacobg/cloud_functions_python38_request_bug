import flask
import werkzeug.datastructures


app = flask.Flask(__name__)

@app.route('/reflect', methods=['POST'])
def reflect():
    request = flask.request
    return request.data, 200


def process_request_in_app(request, app):
    # source: https://stackoverflow.com/a/55576232/1237919
    with app.app_context():
        headers = werkzeug.datastructures.Headers()
        for key, value in request.headers.items():
            headers.add(key, value)

        data = request.form or request.data

        ctx = app.test_request_context(
            method=request.method,
            base_url=request.base_url,
            path=request.path,
            query_string=request.query_string,
            headers=headers,
            data=data)
        ctx.request.data = data
        ctx.push()
        resp = app.full_dispatch_request()
        ctx.pop()
        return resp


def python38_request_bug_app(request):
    return process_request_in_app(request, app)
