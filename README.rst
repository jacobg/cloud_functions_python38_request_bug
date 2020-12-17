
This repository is a minimally reproducible example of a bug in Google Cloud Functions Python 3.8 runtime.
The bug is that when using flask's test_request_context context manager to proxy GCF's request handler into
a flask application, the request data gets dropped somehow.
It works fine on GCF Python 3.7 runtime, and it also works fine on a local development Python 3.8 runtime when using functions-framework.

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
i.e., on Python 3.7 it prints out:
```
POST JSON:
{"data":"{\"foo\": \"bar\"}","form":null,"json":{"foo":"bar"}}
POST FORM:
{"data":"","form":{"foo":"bar"},"json":null}
POST BINARY DATA:
{"data":"foobar","form":{},"json":null}
```

But on Python 3.8 runtime, it does not do that. Instead the result is:
POST JSON:
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>The browser (or proxy) sent a request that this server could not understand.</p>
POST FORM:
{"data":"{\"foo\": \"bar\"}","form":{},"json":null}
POST BINARY DATA:
{"data":"foobar","form":{},"json":null}

That is, the json request fails, and the form request is missing the request.form value.

If you'd like to see it working properly on GCF Python 3.7 runtime, just edit deploy.sh to set python37 option
instead of python38. Then when invoking the function using the call_function.sh script, it will print the above
expected output to the console.

Here is Google's tracking issue:
https://issuetracker.google.com/issues/174365298
