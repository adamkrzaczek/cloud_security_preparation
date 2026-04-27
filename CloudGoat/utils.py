import boto3
from botocore.exceptions import ClientError

def get_session():
    return boto3.Session()

def get_regions(session, user_regions=None):
    if user_regions:
        return user_regions
    return ["us-east-1"]

