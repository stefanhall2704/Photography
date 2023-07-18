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
        
    def upload_file(self, file: str):
        with tempfile.NamedTemporaryFile() as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file.flush()
            self.client.upload_file(temp_file.name, self.bucket, self.file_name)

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

