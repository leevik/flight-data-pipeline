import os
from pathlib import Path
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
LOCAL_DATA_DIR = Path(os.getenv("LOCAL_DATA_DIR", "data/sample"))


def get_latest_json_file(directory: Path) -> Path:
    json_files = list(directory.glob("*.json"))

    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {directory}")

    return max(json_files, key=lambda file: file.stat().st_mtime)


def build_s3_key(local_file: Path) -> str:
    now = datetime.now(timezone.utc)

    return (
        f"raw/flights/"
        f"year={now.year}/"
        f"month={now.month:02d}/"
        f"day={now.day:02d}/"
        f"{local_file.name}"
    )


def upload_file_to_s3(local_file: Path, bucket_name: str, s3_key: str) -> None:
    s3_client = boto3.client("s3", region_name=AWS_REGION)

    try:
        s3_client.upload_file(
            Filename=str(local_file),
            Bucket=bucket_name,
            Key=s3_key,
        )
        print(f"Uploaded {local_file} to s3://{bucket_name}/{s3_key}")

    except ClientError as error:
        raise RuntimeError(f"Failed to upload file to S3: {error}") from error


def main() -> None:
    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME is missing. Add it to your .env file.")

    latest_file = get_latest_json_file(LOCAL_DATA_DIR)
    s3_key = build_s3_key(latest_file)

    upload_file_to_s3(
        local_file=latest_file,
        bucket_name=S3_BUCKET_NAME,
        s3_key=s3_key,
    )


if __name__ == "__main__":
    main()