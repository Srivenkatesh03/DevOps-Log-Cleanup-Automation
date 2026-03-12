import os
import boto3
import datetime
import subprocess
import logging

# Configuration
LOG_DIRECTORY = "/var/log"
S3_BUCKET = "s3-linux-log-12-3-26"
DAYS_OLD = 30
EMAIL = "srivenkatesh49175@gmail.com"

# Logging setup
logging.basicConfig(
    filename="/var/log/log_cleanup_execution.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

s3 = boto3.client("s3")

summary = []

def find_old_logs():
    old_files = []
    now = datetime.datetime.now()

    for root, dirs, files in os.walk(LOG_DIRECTORY):
        for file in files:
            if file.endswith(".log"):
                path = os.path.join(root, file)
                modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(path))

                if (now - modified_time).days > DAYS_OLD:
                    old_files.append(path)

    return old_files

def upload_to_s3(file_path):
    try:
        filename = os.path.basename(file_path)
        s3.upload_file(file_path, S3_BUCKET, filename)
        logging.info(f"Uploaded {file_path} to S3")
        return True
    except Exception as e:
        logging.error(f"S3 Upload failed for {file_path}: {str(e)}")
        return False


def delete_file(file_path):
    try:
        os.remove(file_path)
        logging.info(f"Deleted local file {file_path}")
    except Exception as e:
        logging.error(f"Delete failed for {file_path}: {str(e)}")

def send_email(message):
    ses = boto3.client("ses", region_name="ap-south-1")

    ses.send_email(
        Source="srivenkatesh49175@gmail.com",
        Destination={
            "ToAddresses": ["srivenkatesh49175@gmail.com"]
        },
        Message={
            "Subject": {"Data": "Log Cleanup Report"},
            "Body": {"Text": {"Data": message}}
        }
    )
    print("Log cleanup completed. Email report sent.")

def main():

    files = find_old_logs()

    if not files:
        summary.append("No log files older than 30 days found.")

    for file in files:

        uploaded = upload_to_s3(file)

        if uploaded:
            delete_file(file)
            summary.append(f"Uploaded & deleted: {file}")
        else:
            summary.append(f"Upload failed: {file}")

    report = "\n".join(summary)

    logging.info(report)

    send_email(report)


if __name__ == "__main__":
    main()
