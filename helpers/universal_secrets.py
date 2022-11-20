import boto3
from botocore.exceptions import ClientError
import json
import random
import string

class universal_secret:
    def __init__(self,secret_type):
        ## secret_type = primary or archive
        self.secret_type = secret_type

    def get_secrets(self):
        region_name = "us-east-1"
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
        try:
            get_secret_value_response = client.list_secrets()
            secret_list = []
            for secret in get_secret_value_response['SecretList']:
                secretName = secret['Name']
                if (self.secret_type == "archive"):
                    if ("archive" in secretName):
                        secret_list.append(secretName)
                else:
                    if ("archive" not in secretName):
                        secret_list.append(secretName)
        except ClientError as e:
            raise e
        return secret_list