
PROJECT_ID=$1

curl \
    --header "Content-Type: application/json" \
    --request POST \
    --data '{"foo": "bar"}' \
    https://us-central1-$PROJECT_ID.cloudfunctions.net/python38_request_bug_app/reflect
