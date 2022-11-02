import boto3

from boto3.s3.transfer import S3Transfer
from storages.backends.s3boto3 import S3Boto3Storage

from django.conf import settings


class PublicMediaStorage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        super(PublicMediaStorage, self).__init__(*args, **kwargs)