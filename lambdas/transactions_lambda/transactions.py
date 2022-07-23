from bs4 import BeautifulSoup
import requests
import boto3
from botocore.exceptions import ClientError


TRANSACTIONS_URL = 'https://www.mlb.com/padres/roster/transactions'

dynamodb = boto3.client('dynamodb')

response = requests.get(TRANSACTIONS_URL)   
team_transactions = response.text

team_transactions_soup = BeautifulSoup(team_transactions, 'html.parser')

transactions_list = team_transactions_soup.find_all('tr')

for item in transactions_list:
    transaction = item.text
    print(transaction)

# response = dynamodb.put_item(
#     TableName='cxwtest-table2',
#     Item={"transaction_id":{"transaction_id":"righthere"}
# })