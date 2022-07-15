from calendar import week
import statsapi
import datetime


# date operations
now = datetime.date.today()
today = now - datetime.timedelta(days=1)
today_date = today.strftime('%m/%d/%Y')

week_ago = now - datetime.timedelta(days=8)
week_ago_date = week_ago.strftime('%m/%d/%Y')

# win/loss operations
def get_wins_and_losses(date):
    '''Get Padres record on a specified date this year'''

    standings = statsapi.standings_data(leagueId="104", date=date)
    nl_west = standings[203]['teams']
    padres = [ team for team in nl_west if team['name'] == 'San Diego Padres']

    wins = padres[0]['w']
    losses = padres[0]['l']

    return { 'wins': wins, 'losses': losses, 'team': padres[0], 'division': nl_west }


padres_today = get_wins_and_losses(today_date)
padres_last_week = get_wins_and_losses(week_ago_date)


week_wins = padres_today['wins'] - padres_last_week['wins']
week_losses = padres_today['losses'] - padres_last_week['losses']

current_record = f'{padres_today["wins"]}-{padres_today["losses"]}'
week_record = f'{week_wins}-{week_losses}'


# games-behind operations
padres = padres_today['team']
division = padres_today['division']

gb = float(padres['gb'])
wc_gb = float(padres['wc_gb'])

def is_float(num):
    try:
        float(num)
        return True
    except:
        return False

if is_float(gb):
    if wc_gb < gb:
        games_behind = wc_gb
    else:
        games_behind = gb
else:
    second_place = padres_today['division'][1]
    if '+' in second_place['wc_gb']:
        games_behind = float(second_place['gb']) + float(second_place['wc_gb'])
    else:
        games_behind = float(second_place['gb'])
    
print(current_record)
print(week_record)
print(games_behind)