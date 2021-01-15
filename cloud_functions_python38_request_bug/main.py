import flask
import json
import werkzeug.datastructures


app = flask.Flask(__name__)

@app.route('/reflect', methods=['POST'])
def reflect():
    request = flask.request

    data = (json.dumps(request.data)
            if isinstance(request.data, dict)
            else request.data.decode('utf-8'))

    content = flask.jsonify({
        'data': data,
        'form': request.form,
        'json': request.json,
    })

    return content, 200


def process_request_in_app(request, app):
    # source: https://stackoverflow.com/a/55576232/1237919

    with app.app_context():
        headers = werkzeug.datastructures.Headers()
        for key, value in request.headers.items():
            # Do not forward 'Transfer-Encoding' header, as explained in the following Cloud Function issue:
            # https://issuetracker.google.com/issues/174365298
            if key == 'Transfer-Encoding':
                continue
            headers.add(key, value)

        data = request.form or request.data

        with app.test_request_context(
            method=request.method,
            base_url=request.base_url,
            path=request.path,
            query_string=request.query_string,
            headers=headers,
            data=data,
        ):
            resp = app.full_dispatch_request()
            return resp


def python38_request_bug_app(request):
    return process_request_in_app(request, app)
