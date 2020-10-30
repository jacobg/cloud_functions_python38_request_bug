
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
i.e., '{"foo": "bar"}'. But on Python 3.8 runtime, it does not do that.

If you'd like to see it working properly on GCF Python 3.7 runtime, just edit deploy.sh to set python37 option
instead of python38. Then when invoking the function using the call_function.sh script, it will print
'{"foo": "bar"}' to the console.