from requests_oauthlib import OAuth1Session
import json
import boto3
import base64
from botocore.exceptions import ClientError


def get_secret():

    client2 = boto3.client('secretsmanager')
    response = client2.get_secret_value(
        SecretId='new-keys'
    )
    secrets = json.loads(response['SecretString'])
    print(secrets)

# --------------------------------------------

    # secret_name = 'MY/SECRET/NAME'
    # region_name = 'us-east-1'

    # # Create a Secrets Manager client
    # session = boto3.Session()
    # client = session.client(
    #     service_name='secretsmanager',
    #     region_name=region_name
    # )

    # # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # # We rethrow the exception by default.

    # try:
    #     get_secret_value_response = client.get_secret_value(
    #         SecretId=secret_name
    #     )
    # except ClientError as e:
    #     raise e
    # else:
    #     # Decrypts secret using the associated KMS CMK.
    #     # Depending on whether the secret is a string or binary, one of these fields will be populated.
    #     if 'SecretString' in get_secret_value_response:
    #         secret = get_secret_value_response['SecretString']
    #     else:
    #         decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    return

get_secret()