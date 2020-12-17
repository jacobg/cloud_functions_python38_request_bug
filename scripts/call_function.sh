
PROJECT_ID=$1

echo "POST JSON:"
curl \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"foo": "bar"}' \
    https://us-central1-$PROJECT_ID.cloudfunctions.net/python38_request_bug_app/reflect

echo "POST FORM:"
curl \
    --request POST \
    --form "foo=bar" \
    https://us-central1-$PROJECT_ID.cloudfunctions.net/python38_request_bug_app/reflect

echo "POST BINARY DATA:"
curl \
    --request POST \
    --header "Content-Type:application/octet-stream" \
    --data "foobar" \
    https://us-central1-$PROJECT_ID.cloudfunctions.net/python38_request_bug_app/reflect
