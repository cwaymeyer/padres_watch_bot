from requests_oauthlib import OAuth1Session
import json
import boto3
import leaders
import os


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
    This lambda takes data acquired in `leaders.py` as the payload for a tweet
    '''

    date_range = leaders.get_date_range()
    team_hitting = leaders.get_week_team_hitting_stats()
    hitters = leaders.week_hitting_leaders
    p1 = hitters[0]
    p2 = hitters[1]
    p3 = hitters[2]


    tweet_text = f'''
    #𝙋𝙖𝙙𝙧𝙚𝙨 𝙬𝙚𝙚𝙠𝙡𝙮 𝙝𝙞𝙩𝙩𝙞𝙣𝙜 𝙡𝙚𝙖𝙙𝙚𝙧𝙨  {date_range}

{p1['name']}: {p1['hits_abs']}, {p1['homeruns']} HR, {p1['rbis']} RBI, {p1['ops']} OPS
{p2['name']}: {p2['hits_abs']}, {p2['homeruns']} HR, {p2['rbis']} RBI, {p2['ops']} OPS
{p3['name']}: {p3['hits_abs']}, {p3['homeruns']} HR, {p3['rbis']} RBI, {p3['ops']} OPS

𝗧𝗲𝗮𝗺 𝗵𝗶𝘁𝘁𝗶𝗻𝗴: {team_hitting['avg']} / {team_hitting['obp']} / {team_hitting['slg']}

#LetsGoPadres
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
