from requests_oauthlib import OAuth1Session
import json
import boto3
import record_data
import odds_data


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

# api credentials
CONSUMER_KEY = api_secrets['consumer-key']
CONSUMER_SECRET = api_secrets['consumer-secret']
ACCESS_TOKEN = api_secrets['access-token']
ACCESS_TOKEN_SECRET = api_secrets['access-token-secret']


def handler(event, context):
    '''
    🪐 Lambda handler 🪐
    This lambda takes data acquired in `record_data` and `odds_data`, as the payload for a tweet
    Tweet posts are 1230 EST every Monday and Thursday
    Account: @padsplayoffpush
    '''

    record_obj = record_data.get_win_loss_data() # { 'current_record', 'week_record', 'games_behind' }
    odds_obj = odds_data.get_postseason_odds() # { 'odds', 'change' }

    record = record_obj['current_record']
    percentage = odds_obj['odds']
    games_behind = record_obj['games_behind']
    last_7 = record_obj['week_record']
    change = odds_obj['change']

    tweet_text = f'''
    𝗥𝗲𝗰𝗼𝗿𝗱:      {record}
𝗣𝗹𝗮𝘆𝗼𝗳𝗳𝘀:     {percentage}
𝗚𝗕:             {games_behind}
    
𝗟𝗮𝘀𝘁 𝟳𝗱:      {last_7}
𝗖𝗵𝗮𝗻𝗴𝗲:    {change}

#TimeToShine #Padres
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

    json_response = response.json()

    return json.dumps(json_response, indent=4, sort_keys=True)