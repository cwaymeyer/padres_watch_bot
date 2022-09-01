from requests_oauthlib import OAuth1Session
import json
import boto3
import team_stats
import math


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
    This lambda takes data acquired in `team_stats.py` as the payload for a tweet
    Account: @padres_watch
    '''

    record_obj = team_stats.get_stats() # { 'ops', 'runs', 'starter_era', 'reliever_era' }

    ops = record_obj['ops']
    runs = record_obj['runs']
    starter_era = record_obj['starter_era']
    reliever_era = record_obj['reliever_era']

    def get_ranking_with_suffix(num):
        suffixes = {1: 'st', 2: 'nd', 3: 'rd', 21: 'st', 22: 'nd', 23: 'rd' }
        rank_expr = {1: '🔥', 2: '🟢', 3: '🟡', 4: '🟠', 5: '🔴', 6: '🗑'}

        rank_expr_key = math.ceil(num / 5)
        rank_emoji = rank_expr[rank_expr_key]

        if num in suffixes:
            return f'({num}{suffixes["num"]}) {rank_emoji}'
        else:
            return f'({num}th) {rank_emoji}'

    ops_rank = get_ranking_with_suffix(int(ops[1]))
    runs_rank = get_ranking_with_suffix(int(runs[1]))
    starter_era_rank = get_ranking_with_suffix(int(starter_era[1]))
    reliever_era_rank = get_ranking_with_suffix(int(reliever_era[1]))

    tweet_text = f'''
    #𝙋𝙖𝙙𝙧𝙚𝙨 𝙩𝙚𝙖𝙢 𝙨𝙩𝙖𝙩𝙨 𝙪𝙥𝙙𝙖𝙩𝙚

𝗢𝗣𝗦:           {ops[0]}  {ops_rank}
𝗥𝘂𝗻𝘀:          {runs[0]}/g  {runs_rank}

𝗥𝗼𝘁𝗮𝘁𝗶𝗼𝗻 𝗘𝗥𝗔:      {starter_era[0]}  {starter_era_rank}
𝗕𝘂𝗹𝗹𝗽𝗲𝗻 𝗘𝗥𝗔:       {reliever_era[0]}  {reliever_era_rank}

#GoPadres #TimeToShine
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