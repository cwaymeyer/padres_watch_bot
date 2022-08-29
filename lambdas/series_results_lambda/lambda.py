from requests_oauthlib import OAuth1Session
import json
import boto3
import series_results
import configparser

config = configparser.RawConfigParser()
config.read('config.properties')

SECRET_ID = config.get('AWS', 'secret_id')
TW_URL = 'https://api.twitter.com/2/tweets'


def get_api_secrets():
    '''Get twitter API keys from AWS Secrets Manager'''

    client = boto3.client('secretsmanager')
    response = client.get_secret_value(
        SecretId=SECRET_ID
    )
    secret = json.loads(response['SecretString'])

    return secret


api_secrets = get_api_secrets()

# api credentials
CONSUMER_KEY = api_secrets['consumer-key']
CONSUMER_SECRET = api_secrets['consumer-secret']
ACCESS_TOKEN = api_secrets['access-token']
ACCESS_TOKEN_SECRET = api_secrets['access-token-secret']


def handler(event, context):
    '''
    🪐 Lambda handler 🪐
    This lambda takes data acquired in `series_results.py` as the payload for a tweet
    Account: @padres_watch
    '''

    results = series_results.get_series_results()

    body = ''.join(map(str, results['results']))

    tweet_text = f'''
    #𝙋𝙖𝙙𝙧𝙚𝙨 𝙨𝙚𝙖𝙨𝙤𝙣 𝙨𝙚𝙧𝙞𝙚𝙨 𝙧𝙚𝙨𝙪𝙡𝙩𝙨

{body}

🧹 𝗦𝘄𝗲𝗲𝗽𝘀: {results['total_sweeps']}
🟢 𝗪𝗶𝗻𝘀: {results['total_wins']}
🔴 𝗟𝗼𝘀𝘀𝗲𝘀: {results['total_losses']}
🔵 𝗦𝗽𝗹𝗶𝘁𝘀: {results['total_splits']}

#TimeToShine
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