import json
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

def test_reflect_json():
    response = requests.post("http://localhost:8080/reflect", json={'foo': 'bar'})

    assert response.status_code == 200

    content = json.loads(response.content)

    assert content == {
      'data': '{"foo": "bar"}',
      'form': {},
      'json': {"foo": "bar"}
    }

def test_reflect_form():
    response = requests.post("http://localhost:8080/reflect", data={'foo': 'bar'})

    assert response.status_code == 200

    content = json.loads(response.content)

    assert content == {
      'data': '',
      'form': {"foo": "bar"},
      'json': None
    }

def test_reflect_binary_data():
    response = requests.post(
      "http://localhost:8080/reflect",
      data=b'foobar',
      headers={'Content-Type': 'application/octet-stream'}
    )

    assert response.status_code == 200

    content = json.loads(response.content)

    assert content == {
      'data': 'foobar',
      'form': {},
      'json': None
    }
