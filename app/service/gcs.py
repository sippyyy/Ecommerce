import os
from google.cloud import storage
from fastapi import HTTPException,status

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'cert/gcs-key.json'

class GCStorage:
    def __init__(self):
        self.storage_client = storage.Client()
        self.bucket_name = 'ecommerce_sippyyy'
    def upload_file(self,file):
        allowed_formats = ['image/png', 'image/jpeg']
        
        if file.content_type not in allowed_formats:
            # Handle the case when the file format is not allowed
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file format")
        bucket = self.storage_client.get_bucket(self.bucket_name)
        file_path = "ecommerce_sippy" + file.filename
        blob = bucket.blob(file_path)
        blob.upload_from_file(file.file,content_type=file.content_type)
        return f'https://storage.cloud.google.com/{self.bucket_name}/{file_path}'
    
    def delete_file(self,bucket_name, file_path):
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.delete()
