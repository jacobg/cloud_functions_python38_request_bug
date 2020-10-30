DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SRC_DIR=$DIR/../cloud_functions_python38_request_bug

PROJECT_ID=$1

gcloud functions deploy python38_request_bug_app \
  --project "$PROJECT_ID" \
  --source="$SRC_DIR" \
  --runtime python38 \
  --trigger-http \
  --allow-unauthenticated \
