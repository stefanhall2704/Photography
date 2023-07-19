import boto3
import tempfile
import os
import time
from django.http import HttpResponse
import logging
from botocore.exceptions import ClientError


class S3Storage:
    client = boto3.client("s3")

    def __init__(self, file_name: str, bucket: str):
        self.file_name = file_name
        self.bucket = bucket

    def upload_file(self, file: str):
        with tempfile.NamedTemporaryFile() as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file.flush()
            self.client.upload_file(temp_file.name, self.bucket, self.file_name)

    def download_file(self):
        file_obj = self.client.get_object(Bucket=self.bucket, Key=self.file_name)
        file_data = file_obj["Body"].read()

        response = HttpResponse(content_type="application/octet-stream")
        response["Content-Disposition"] = f'attachment; filename="{self.file_name}"'
        response.write(file_data)

        return response

    def get_photo(self):
        try:
            response = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": self.file_name},
                ExpiresIn=3600,
            )
            # response = self.client.generate_presigned_url('get_object', Params={'Bucket': self.bucket, 'Key': self.file_name}, ExpiresIn=3600)
            return response
        except Exception as e:
            print(e)
