import boto3
from botocore.exceptions import ClientError
import json
import random
import string

class secret:
    def __init__(self,secret_name):
        self.secret_name = secret_name

    def generate_secret(self):
        # get random string of length 30 without repeating letters
        characters = string.ascii_letters + string.digits
        secret = ''.join(random.choice(characters) for i in range(30))
        return secret

    def get_secret(self):
        print("Getting the secret detail for",self.secret_name)
        region_name = "us-east-1"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=self.secret_name
            )
        except ClientError as e:
            raise e
        secret = get_secret_value_response['SecretString']
        return secret

    def rotate_secret(self):
        region_name = "us-east-1"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.put_secret_value(
                SecretId=self.secret_name,
                SecretString=self.generate_secret(),
            )
        except ClientError as e:
            raise e
        secret = get_secret_value_response
        return secret

    def set_secret(self,secret_string):
        region_name = "us-east-1"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.put_secret_value(
                SecretId=self.secret_name,
                SecretString=secret_string,
            )
        except ClientError as e:
            raise e
        secret = get_secret_value_response
        return secret
