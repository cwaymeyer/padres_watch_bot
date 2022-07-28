import statsapi
import datetime


EXPRESSIONS = {
-8: '🤮',
-7: '🤡',
-6: '🤢',
-5: '😫',
-4: '🥴',
-3: '😓',
-2: '😬', 
-1: '😒',
0: '😐',
1: '😀',
2: '😎',
3: '💪',
4: '😤',
5: '🤑',
6: '🔥',
7: '🔥',
8: '💥'
}

# date operations
now = datetime.date.today()
today = now - datetime.timedelta(days=1)
today_date = today.strftime('%m/%d/%Y')

week_ago = now - datetime.timedelta(days=8)
week_ago_date = week_ago.strftime('%m/%d/%Y')


def get_win_loss_data():
    '''
    Hits the mlbstats-api and returns an object with three values:
        - Current record 
        - Wins pace
        - Record over the past week
        - Games out of a playoff spot
    '''

    # win/loss operations
    def get_wins_and_losses(date):
        '''Get Padres record on a specified date this year'''

        standings = statsapi.standings_data(leagueId='104', date=date)
        nl_west = standings[203]['teams']
        padres = [ team for team in nl_west if team['name'] == 'San Diego Padres']

        wins = padres[0]['w']
        losses = padres[0]['l']

        return { 'wins': wins, 'losses': losses, 'team': padres[0], 'division': nl_west }

    padres_today = get_wins_and_losses(today_date)
    padres_last_week = get_wins_and_losses(week_ago_date)

    # get win-loss records
    current_wins = padres_today['wins']
    current_losses = padres_today['losses']

    week_wins = current_wins - padres_last_week['wins']
    week_losses = current_losses - padres_last_week['losses']

    current_record = f'{current_wins}-{current_losses}'
    week_record = f'{week_wins}-{week_losses}'

    # set week record expression
    week_diff = week_wins - week_losses
    if week_diff in EXPRESSIONS:
        if week_losses == 0:
            emoji = '🧹'
        else:
            emoji = EXPRESSIONS[week_diff]
        week_record_expr = f'{week_record}  {emoji}'
    else:
        week_record_expr = f'{week_record}  😳'

    # pace operations
    win_percentage = current_wins / (current_wins + current_losses)
    pace = round(win_percentage * 162)
    wins_pace = f'{pace} wins'

    # games-behind operations
    padres = padres_today['team']
    division = padres_today['division']

    gb = float(padres['gb'])
    wc_gb = float(padres['wc_gb'])


    def get_fourth_place_games_behind():
        '''Get games behind for the first team outside of the wildcard spot'''
        wc_standings = statsapi.standings_data(leagueId='104', date=today_date)

        fourth_place_games_behind = 0
        i = 203
        while (i <= 205):
            div_standings = wc_standings[i]['teams']
            for team in div_standings:
                if team['wc_rank'] == '4':
                    fourth_place_games_behind = team['wc_gb']
                    break
            i += 1
        
        return fourth_place_games_behind


    def is_float(num):
        '''True or false, is num a float'''

        try:
            float(num)
            return True
        except:
            return False

    if is_float(gb): # if team not in 1st place
        if '+' in padres['wc_gb']:
            first_out_of_wc_gb = get_fourth_place_games_behind() if is_float(get_fourth_place_games_behind()) else 0
            games_behind = padres['wc_gb'] + float(first_out_of_wc_gb)
        elif wc_gb < gb:
            games_behind = wc_gb
        else:
            games_behind = gb
    else:
        second_place = division[1]
        if '+' in second_place['wc_gb']:
            games_behind = float(second_place['gb']) + float(second_place['wc_gb'])
        else:
            games_behind = float(second_place['gb'])

    return {  
        'current_record': current_record,
        'wins_pace': wins_pace,
        'week_record': week_record_expr, 
        'games_behind': games_behind 
    }