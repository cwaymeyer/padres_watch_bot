from requests_oauthlib import OAuth1Session
import json
import boto3
import war_data


SECRET_ID = 'twitter-api'
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

CONSUMER_KEY = api_secrets['consumer-key']
CONSUMER_SECRET = api_secrets['consumer-secret']
ACCESS_TOKEN = api_secrets['access-token']
ACCESS_TOKEN_SECRET = api_secrets['access-token-secret']


def handler(event, context):
    '''
    🪐 Lambda handler 🪐
    This lambda takes data acquired in `war_data.py`, as the payload for a tweet
    '''

    players = war_data.get_war_data() # { 'player', 'war', 'value' }

    players.sort(key=lambda player: player['value'], reverse=True)
    print(players)

    leaders_list = ''

    for i in range(10):
        leaders_list += f'{players[i]["player"]} - {players[i]["war"]}\n'

    tweet_text = f'''
#𝙋𝙖𝙙𝙧𝙚𝙨 𝙨𝙚𝙖𝙨𝙤𝙣 𝙒𝘼𝙍 𝙡𝙚𝙖𝙙𝙚𝙧𝙨

{leaders_list}

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