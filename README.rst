
This repository is a minimally reproducible example of a regression in Google Cloud Functions Python 3.8 runtime,
and the necessary workaround to make it work.
That is, on GCF's Python 3.8 runtime, there is a new request header `Transfer-Encoding: chunked` that will break
flask's test_request_context context manager to proxy GCF's request handler into a flask application.
It is necessary on 3.8 to not copy this new header into the flask app.

You can verify local development functionality by running the included unit test. The python poetry tool must be installed.
Then just run:
```
poetry install
poetry run pytest
```

To deploy this function to GCF run:
```
bash scripts/deploy.sh $PROJECT_ID
```

To invoke the function, and view output, run:
```
bash scripts/call_function.sh $PROJECT_ID
```

The correct behavior would be for the script to print the data posted to the function, which reflects it back in the response,
as follows:
```
POST JSON:
{"data":"{\"foo\": \"bar\"}","form":{},"json":{"foo":"bar"}}
POST FORM:
{"data":"","form":{"foo":"bar"},"json":null}
POST BINARY DATA:
{"data":"foobar","form":{},"json":null}
```

If you'd like to see it working properly on GCF Python 3.7 runtime, just edit deploy.sh to set python37 option
instead of python38. Then when invoking the function using the call_function.sh script, it will print the above
expected output to the console.

Here is Google's tracking issue:
https://issuetracker.google.com/issues/174365298
