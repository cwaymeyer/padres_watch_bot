from bs4 import BeautifulSoup
import requests

URL = 'https://www.baseball-reference.com/leagues/majors/2022-playoff-odds.shtml'


def get_html(url):
    '''Get webpage html'''

    response = requests.get(url)
    return response.text

def get_team_odds_soup(team):
    '''Get playoff odds data as html soup for specified team'''

    teams = get_html(URL)
    teams_soup = BeautifulSoup(teams, 'html.parser')

    playoff_odds = teams_soup.find_all('tbody')[1]

    team_odds = [item for item in playoff_odds if team in str(item)][0]
    team_odds_soup = BeautifulSoup(str(team_odds), 'html.parser')

    return team_odds_soup

def get_postseason_odds():
    '''
    🪐 Lambda handler 🪐
    Hits baseballreference.com and returns an object with values:
        - Postseason odds
        - Change in postseason odds over the last 7 days
    '''

    padres_soup = get_team_odds_soup('Padres')

    postseason_odds = padres_soup.find('td', attrs={'data-stat' : 'ppr_postseason'})['csk']
    seven_day_postseason_change = padres_soup.find('td', attrs={'data-stat' : 'ppr_change_7day'}).text

    return {'odds': postseason_odds, 'change': seven_day_postseason_change}
