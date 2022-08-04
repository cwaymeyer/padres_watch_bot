from bs4 import BeautifulSoup
import requests
import statsapi
import datetime


NOW = datetime.date.today()
last_month = NOW.month - 1

PADRES_ID = 135

HITTERS_LAST_7_URL = 'https://www.mlb.com/stats/san-diego-padres?playerPool=ALL&timeframe=-7'
PITCHERS_LAST_7_URL = 'https://www.mlb.com/stats/pitching/san-diego-padres?playerPool=ALL&sortState=asc&timeframe=-7'

HITTERS_LAST_MONTH_URL = f'https://www.mlb.com/stats/san-diego-padres?split={last_month}&playerPool=ALL'
PITCHERS_LAST_MONTH_URL = f'https://www.mlb.com/stats/pitching/san-diego-padres?split=7&playerPool=ALL&sortState=asc'

TEAM_HITTING_LAST_7_URL = 'https://www.mlb.com/stats/team?timeframe=-7'
TEAM_PITCHING_LAST_7_URL = 'https://www.mlb.com/stats/team/pitching?sortState=asc&timeframe=-7'

TEAM_HITTING_LAST_MONTH_URL = f'https://www.mlb.com/stats/team?split={last_month}'
TEAM_PITCHING_LAST_MONTH_URL = f'https://www.mlb.com/stats/team/pitching?split={last_month}&sortState=asc'


# get # of games played in the week

today = NOW - datetime.timedelta(days=1)
today_date = today.strftime('%m/%d/%Y')

week_ago = NOW - datetime.timedelta(days=7)
week_ago_date = week_ago.strftime('%m/%d/%Y')

game_range = statsapi.schedule(start_date=week_ago_date, end_date=today_date, team=PADRES_ID) # 7 days ago -> 1 day ago (7 days)
week_game_count = len(game_range)


def get_date_range():
    '''Return date range for statistics gathered'''

    date_range = f'{week_ago_date[0:5]} - {today_date[0:5]}'
    return date_range


def get_last_month():
    '''Return string name of last month used for stats queries'''

    months = ['𝙅𝙖𝙣𝙪𝙖𝙧𝙮', '𝙁𝙚𝙗𝙧𝙪𝙖𝙧𝙮', '𝙈𝙖𝙧𝙘𝙝', '𝘼𝙥𝙧𝙞𝙡', '𝙈𝙖𝙮', '𝙅𝙪𝙣𝙚', '𝙅𝙪𝙡𝙮', '𝘼𝙪𝙜𝙪𝙨𝙩', '𝙎𝙚𝙥𝙩𝙚𝙢𝙗𝙚𝙧', '𝙊𝙘𝙩𝙤𝙗𝙚𝙧', '𝙉𝙤𝙫𝙚𝙢𝙗𝙚𝙧', '𝘿𝙚𝙘𝙚𝙢𝙗𝙚𝙧']
    return months[last_month - 1]


def get_html(url):
    '''Get webpage html'''

    response = requests.get(url)
    return response.text


def get_player_rows(url):
    '''Scrape rows of team or player stats from mlb.com'''

    player_stats = get_html(url)

    player_stats_soup = BeautifulSoup(player_stats, 'html.parser')
    player_table = player_stats_soup.find('tbody')
    player_rows = player_table.find_all('tr')

    return player_rows


def get_top_hitters(url):
    '''Get top three hitters from specified time based on OPS, over 2.5 ABs/game'''

    hitters_rows = get_player_rows(url)
    top_performers = []

    for row in hitters_rows:
        at_bats = row.find('td', attrs={'data-col' : '3'}).text
        if int(at_bats) / week_game_count > 2.5:
            player_name = row.find('a')['aria-label']
            hits = row.find('td', attrs={'data-col' : '5'}).text
            homeruns = row.find('td', attrs={'data-col' : '8'}).text
            rbis = row.find('td', attrs={'data-col' : '9'}).text
            avg = row.find('td', attrs={'data-col' : '14'}).text
            obp = row.find('td', attrs={'data-col' : '15'}).text
            ops = row.find('td', attrs={'data-col' : '17'}).text

            player_obj = {
                'name': player_name,
                'hits_abs': f'{hits}-{at_bats}',
                'homeruns': homeruns,
                'rbis': rbis,
                'avg': avg,
                'obp': obp,
                'ops': ops
            }

            top_performers.append(player_obj)

            if len(top_performers) == 3:
                break

    return top_performers


def get_top_pitchers(url):
    '''Get top three pitchers from specified time based on ERA, over 0.65 INNs/game'''

    pitchers_rows = get_player_rows(url)
    top_performers = []

    for row in pitchers_rows:
        innings_pitched = row.find('td', attrs={'data-col' : '11'}).text
        if float(innings_pitched) / week_game_count > 0.7:
            player_name = row.find('a')['aria-label']
            hits = row.find('td', attrs={'data-col' : '12'}).text
            walks = row.find('td', attrs={'data-col' : '17'}).text
            strikeouts = row.find('td', attrs={'data-col' : '18'}).text
            era = row.find('td', attrs={'data-col' : '4'}).text

            player_obj = {
                'name': player_name,
                'innings': innings_pitched,
                'hits': hits,
                'walks': walks,
                'strikeouts': strikeouts,
                'era': era
            }

            top_performers.append(player_obj)

            if len(top_performers) == 3:
                break

    return top_performers


week_hitting_leaders = get_top_hitters(HITTERS_LAST_7_URL)
week_pitching_leaders = get_top_pitchers(PITCHERS_LAST_7_URL)
month_hitting_leaders = get_top_hitters(HITTERS_LAST_MONTH_URL)
month_pitching_leaders = get_top_pitchers(PITCHERS_LAST_MONTH_URL)


def get_team_stats(url):
    '''Get Padres team stack from specified time'''

    hitting_rows = get_html(url)

    hitting_rows_soup = BeautifulSoup(hitting_rows, 'html.parser')
    teams_table = hitting_rows_soup.find('tbody')
    
    team_row = teams_table.find('a', attrs={'aria-label' : 'San Diego Padres'}).find_parent('tr')

    return team_row


def get_week_team_hitting_stats():
    '''Get select Padres team hitting stats for the week (returns { 'avg', 'obp', 'slg' })'''

    team_hitting_stats = get_team_stats(TEAM_HITTING_LAST_7_URL)

    avg = team_hitting_stats.find('td', attrs={'data-col' : '14'}).text
    obp = team_hitting_stats.find('td', attrs={'data-col' : '15'}).text
    slg = team_hitting_stats.find('td', attrs={'data-col' : '16'}).text

    return { 'avg': avg, 'obp': obp, 'slg': slg }


def get_week_team_pitching_stats():
    '''Get select Padres team pitching stats for the week (returns { 'era', 'whip' })'''

    team_pitching_stats = get_team_stats(TEAM_PITCHING_LAST_7_URL)

    era = team_pitching_stats.find('td', attrs={'data-col' : '4'}).text
    whip = team_pitching_stats.find('td', attrs={'data-col' : '19'}).text

    return { 'era': era, 'whip': whip }


def get_month_team_hitting_stats():
    '''Get select Padres team hitting stats for the month (returns { 'avg', 'obp', 'slg' })'''

    team_hitting_stats = get_team_stats(TEAM_HITTING_LAST_MONTH_URL)

    avg = team_hitting_stats.find('td', attrs={'data-col' : '14'}).text
    obp = team_hitting_stats.find('td', attrs={'data-col' : '15'}).text
    slg = team_hitting_stats.find('td', attrs={'data-col' : '16'}).text

    return { 'avg': avg, 'obp': obp, 'slg': slg }


def get_month_team_pitching_stats():
    '''Get select Padres team pitching stats for the month (returns { 'era', 'whip' })'''

    team_pitching_stats = get_team_stats(TEAM_PITCHING_LAST_MONTH_URL)

    era = team_pitching_stats.find('td', attrs={'data-col' : '4'}).text
    whip = team_pitching_stats.find('td', attrs={'data-col' : '19'}).text

    return { 'era': era, 'whip': whip }