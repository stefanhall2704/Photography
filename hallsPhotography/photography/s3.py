import boto3 
import tempfile
import os
import time
from django.http import HttpResponse



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
        file_data = file_obj['Body'].read()

        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{self.file_name}"'
        response.write(file_data)

        return response

