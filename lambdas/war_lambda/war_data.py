from bs4 import BeautifulSoup, Comment
import requests
import datetime 


current_year = datetime.date.today().strftime('%Y')

HITTERS_URL = f'https://www.baseball-reference.com/teams/SDP/{current_year}-batting.shtml'
PITCHERS_URL = f'https://www.baseball-reference.com/teams/SDP/{current_year}-pitching.shtml'


def get_html(url):
    '''Get webpage html'''

    response = requests.get(url)
    return response.text


def get_player_war(url, type):
    '''Get player WAR stats'''

    stats = get_html(url)
    stats_soup = BeautifulSoup(stats, 'html.parser')

    comments = stats_soup.find_all(string=lambda text:isinstance(text, Comment))
    result = [ comment.extract() for comment in comments if f'players_value_{type}' in comment]

    table = BeautifulSoup(str(result[0]), 'html.parser').find('tbody')
    table_rows = table.find_all('tr')

    player_list = []

    if type == 'batting':
        war_id = 'WAR'
    else:
        war_id = 'WAR_pitch'

    for row in table_rows:
        player = row.find('th').text.replace("*", "").replace("\xa0", " ")
        war = row.find('td', attrs={'data-stat' : war_id }).text
        war_val = row.find('td', attrs={'data-stat' : war_id })['csk']

        player_obj = { 'player': player, 'war': war, 'value': war_val }
        player_list.append(player_obj)

    return player_list


def get_war_data():
    '''Get WAR stats for hitters and pitchers, combined into a single array'''

    hitters = get_player_war(HITTERS_URL, 'batting')
    pitchers = get_player_war(PITCHERS_URL, 'pitching')

    return hitters + pitchers