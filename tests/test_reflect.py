import os
import subprocess
import time

import pytest
import requests

from cloud_functions_python38_request_bug import main

FUNCTION_SOURCE = os.path.abspath(main.__file__)

@pytest.fixture(scope="module", autouse=True)
def flask_app_server():
    proc = subprocess.Popen([
      'functions-framework',
      '--target=python38_request_bug_app',
      f'--source={FUNCTION_SOURCE}'
    ])
    time.sleep(0.5)  # wait for function handle to be ready to serve
    yield
    proc.terminate()

def test_reflect():
    response = requests.post("http://localhost:8080/reflect", json={'foo': 'bar'})

    assert response.status_code == 200
    assert response.content == b'{"foo": "bar"}'
