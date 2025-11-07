from flask import Flask, request, jsonify
import os
import boto3
import json

app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")         # SQS queue URL
TOKEN_PARAM_NAME = os.getenv("TOKEN_PARAM_NAME", "queue2bucket-api-token")  # Name of SSM parameter that stores the API token

# Initialize AWS service clients
ssm = boto3.client("ssm", region_name=AWS_REGION)  # AWS Systems Manager (for Parameter Store)
sqs = boto3.client("sqs", region_name=AWS_REGION)  # AWS Simple Queue Service

def get_expected_token():
    resp = ssm.get_parameter(Name=TOKEN_PARAM_NAME, WithDecryption=True)
    return resp["Parameter"]["Value"]


#Validate the structure of the incoming JSON payload.
def validate_payload(body):

    # Check that both 'data' and 'token' exist in the request body
    if "data" not in body or "token" not in body:
        return False, "Missing 'data' or 'token'"

    data = body["data"]
    required_fields = ["email_subject", "email_sender", "email_timestream", "email_content"]

    # Verify that all required fields exist inside the 'data' section
    for field in required_fields:
        if field not in data:
            return False, f"Missing field in data: {field}"

    return True, ""  # Validation passed successfully


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/email", methods=["POST"])
def handle_email():
    try:
        body = request.get_json()
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400
    if body is None:
        return jsonify({"error": "Missing JSON body"}), 400

    # Validate the JSON structure and required fields
    valid, msg = validate_payload(body)
    if not valid:
        return jsonify({"error": msg}), 400

    # Validate the token sent by the client against the expected one
    sent_token = body.get("token")
    expected_token = get_expected_token()

    if sent_token != expected_token:
        return jsonify({"error": "Invalid token"}), 401

    # If validation passes, publish the message to the SQS queue
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(body["data"])  # Only send the data section to SQS
    )

    return jsonify({"status": "queued"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
