from bs4 import BeautifulSoup
import requests


OPS_URL = 'https://www.mlb.com/stats/team'
GAMES_URL = 'https://www.mlb.com/stats/team/games'
RUNS_URL = 'https://www.mlb.com/stats/team/runs'
STARTER_ERA_URL = 'https://www.mlb.com/stats/team/pitching?split=sp&sortState=asc'
RELIEVER_ERA_URL = 'https://www.mlb.com/stats/team/pitching?split=rp&sortState=asc'


def get_statistic_and_rank(url):
    '''Takes an mlb stats page url and returns a tuple containing the selected stat and rank across MLB'''

    response = requests.get(url)
    team_stats = response.text

    team_stats_soup = BeautifulSoup(team_stats, 'html.parser')

    stats_table = team_stats_soup.find('tbody')

    team_row = stats_table.find('a', attrs={'aria-label' : 'San Diego Padres'}).find_parent('tr')

    statistic = team_row.select_one('td[class*="selected"]').text
    stat_rank = team_row.find('th')['data-row']

    return (statistic, stat_rank)
    

def get_stats():
    '''Get stat and rank for team OPS, runs, starter ERA and bullpen ERA'''

    team_ops = get_statistic_and_rank(OPS_URL)
    team_games = get_statistic_and_rank(GAMES_URL)
    team_runs = get_statistic_and_rank(RUNS_URL)
    team_starter_era = get_statistic_and_rank(STARTER_ERA_URL)
    team_reliever_era = get_statistic_and_rank(RELIEVER_ERA_URL)

    runs_per_game = round(int(team_runs[0]) / int(team_games[0]), 1)

    runs_data = (runs_per_game, team_runs[1])

    return {
        'ops': team_ops, 
        'runs': runs_data, 
        'starter_era': team_starter_era, 
        'reliever_era': team_reliever_era
    }