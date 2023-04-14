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
    team_pitching = leaders.get_week_team_pitching_stats()
    pitchers = leaders.week_pitching_leaders
    p1 = pitchers[0]
    p2 = pitchers[1]
    p3 = pitchers[2]


    tweet_text = f'''
   #𝙋𝙖𝙙𝙧𝙚𝙨 𝙬𝙚𝙚𝙠𝙡𝙮 𝙥𝙞𝙩𝙘𝙝𝙞𝙣𝙜 𝙡𝙚𝙖𝙙𝙚𝙧𝙨  {date_range}

{p1['name']}: {p1['innings']} IP, {p1['hits']} H, {p1['strikeouts']} K, {p1['era']} ERA
{p2['name']}: {p2['innings']} IP, {p2['hits']} H, {p2['strikeouts']} K, {p2['era']} ERA
{p3['name']}: {p3['innings']} IP, {p3['hits']} H, {p3['strikeouts']} K, {p3['era']} ERA

𝗧𝗲𝗮𝗺 𝗽𝗶𝘁𝗰𝗵𝗶𝗻𝗴: {team_pitching['era']} ERA / {team_pitching['whip']} WHIP

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