from requests_oauthlib import OAuth1Session
import json
import boto3
import leaders


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
    This lambda takes data acquired in `leaders.py` as the payload for a tweet
    Account: @padres_watch
    '''

    last_month = leaders.get_last_month()
    team_hitting = leaders.get_month_team_hitting_stats()
    hitters = leaders.month_hitting_leaders
    p1 = hitters[0]
    p2 = hitters[1]
    p3 = hitters[2]


    tweet_text = f'''
    #𝙋𝙖𝙙𝙧𝙚𝙨 𝙢𝙤𝙣𝙩𝙝𝙡𝙮 𝙝𝙞𝙩𝙩𝙞𝙣𝙜 𝙡𝙚𝙖𝙙𝙚𝙧𝙨 | {last_month}

{p1['name']}: {p1['avg']} AVG, {p1['homeruns']} HR, {p1['rbis']} RBI, {p1['ops']} OPS
{p2['name']}: {p2['avg']} AVG, {p2['homeruns']} HR, {p2['rbis']} RBI, {p2['ops']} OPS
{p3['name']}: {p3['avg']} AVG, {p3['homeruns']} HR, {p3['rbis']} RBI, {p3['ops']} OPS

Team hitting: {team_hitting['avg']} / {team_hitting['obp']} / {team_hitting['slg']}

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