from requests_oauthlib import OAuth1Session
import json
import boto3
import os
import datetime
import win_loss_data


TODAY = datetime.date.today().strftime('%m-%d-%Y')


TW_URL = 'https://api.twitter.com/2/tweets'
SECRET_ID = os.environ['TW_SECRET_ID']


def get_api_secrets():
    '''Get twitter API keys from AWS Secrets Manager'''

    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId=SECRET_ID
    )
    secret = json.loads(response['SecretString'])

    return secret


api_secrets = get_api_secrets()

CONSUMER_KEY = api_secrets['consumer-key']
CONSUMER_SECRET = api_secrets['consumer-secret']
ACCESS_TOKEN = api_secrets['access-token']
ACCESS_TOKEN_SECRET = api_secrets['access-token-secret']


def handler(event, context):
    '''
    🪐 Lambda handler 🪐
    This lambda takes data acquired in `win_loss_data.py` as the payload for a tweet
    '''

    wl_data = win_loss_data.get_win_loss_data()

    results = ''.join(map(str, wl_data['results']))
    record = wl_data['record']

    tweet_text = f'''
    #𝙋𝙖𝙙𝙧𝙚𝙨 𝙧𝙚𝙨𝙪𝙡𝙩𝙨 | {TODAY} | {record}

{results}

#BringTheGold
    '''

    payload = {'text': tweet_text}

    oauth = OAuth1Session(
        CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_TOKEN_SECRET,
    )

    response = oauth.post(
        TW_URL,
        json=payload,
    )

    if response.status_code != 201:
        raise Exception(
            'Request returned an error: {} {}'.format(response.status_code, response.text)
        )

    print('Response code: {}'.format(response.status_code))

    return json.dumps(response.json(), indent=4, sort_keys=True)