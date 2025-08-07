import boto3
from dotenv import load_dotenv
import os

load_dotenv()
REGION = os.getenv("AWS_REGION")

def get_client(service_name):
    return boto3.client(service_name, region_name=REGION)

def get_resource(service_name):
    return boto3.resource(service_name, region_name=REGION)

