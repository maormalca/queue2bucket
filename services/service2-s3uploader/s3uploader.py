import os
import time
import json
import uuid
import boto3

# Load configuration from environment variables (with defaults for local use)
AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")      # SQS queue URL
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")    # S3 bucket name
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "5"))  # Seconds between polling cycles

# Create AWS clients
sqs = boto3.client("sqs", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)


def process_message(msg_body: str):
    """
    Save one SQS message to S3 as a JSON file.
    The file name includes a timestamp and random UUID.
    """
    data = json.loads(msg_body)
    key = f"emails/{int(time.time())}-{uuid.uuid4().hex}.json"

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=key,
        Body=json.dumps(data).encode("utf-8"),
        ContentType="application/json",
    )

    print(f"Saved to s3://{S3_BUCKET_NAME}/{key}")


def main():
    """
    Continuously poll the SQS queue.
    For each new message, save it to S3 and then delete it from the queue.
    """
    print("Worker started, polling SQS...")

    while True:
        resp = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10,  # Use long polling to reduce empty responses
        )

        messages = resp.get("Messages", [])
        if not messages:
            time.sleep(POLL_INTERVAL)
            continue

        for msg in messages:
            receipt_handle = msg["ReceiptHandle"]
            body = msg["Body"]

            try:
                process_message(body)

                # Delete the message from the queue after successful processing
                sqs.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=receipt_handle,
                )
                print("Message processed and deleted.")
            except Exception as e:
                print(f"Error processing message: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
