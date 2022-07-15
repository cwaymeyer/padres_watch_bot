from requests_oauthlib import OAuth1Session
import json
import boto3
# import record_layer
# import odds_layer

SECRET_ID = 'twitter-api'
TW_URL = 'https://api.twitter.com/2/tweets'

def get_api_secrets():

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

# record = record_layer.get_win_loss_data()
# odds = odds_layer.get_postseason_odds()

# print(record)
# [print(odds)]

def handler():
    '''
    🪐 Lambda handler 🪐
    This lambda takes the data acquired in data_lambda and uses it to format and post a tweet
    Tweet posts are 1200 EST every Monday and Thursday
    '''

    record = '55-50'
    gb = '2.5'
    percentage = '56.7%'
    last_7 = '4-3'
    change = '+5.6%'

    tweet_text = f'''
    record:         {record}
    gb:             {gb}
    playoff %:    {percentage}

    last 7d:          {last_7}    🔥
    change:      {change} 📈
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

    # Saving the response as JSON
    json_response = response.json()
    return json.dumps(json_response, indent=4, sort_keys=True)

handler()