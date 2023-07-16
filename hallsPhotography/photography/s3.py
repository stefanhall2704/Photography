import boto3 
import tempfile
import os
import time
from django.http import FileResponse


class S3Storage:
    client = boto3.client("s3")
    
    def __init__(self, file_name: str, bucket: str):
        self.file_name = file_name
        self.bucket = bucket
        
    def upload_file(self, file_path: str):
        # TODO: Add to database table with file name and bucket name
        self.client.upload_file(file_path, self.bucket, self.file_name)

    def download_file(self):
        file_obj = self.client.get_object(
            Bucket=self.bucket,
            Key=self.file_name
        )
        file = file_obj.get("Body").read()  # Read the contents of the StreamingBody object
        response = FileResponse(file)
        response["Content-Disposition"] = f'attachment; filename="{self.file_name}"'
        return response


download = S3Storage("new_test.jpg", "portfoliophotographs")
temp_file_path = download.download_file()
print(temp_file_path)
