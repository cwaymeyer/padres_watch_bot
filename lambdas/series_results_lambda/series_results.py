from bs4 import BeautifulSoup
import requests
import datetime 


current_year = datetime.date.today().strftime('%Y')

GAME_RESULTS_URL = f'https://www.baseball-reference.com/teams/SDP/{current_year}-schedule-scores.shtml'


def get_html(url):
    '''Get webpage html'''

    response = requests.get(url)
    return response.text


def get_game_results_soup():
    '''Get playoff odds data as html soup for specified team'''

    game_results = get_html(GAME_RESULTS_URL)
    game_results_soup = BeautifulSoup(game_results, 'html.parser')

    game_results_table = game_results_soup.find('tbody')

    individual_games = game_results_table.find_all('tr')

    return individual_games


def get_series_results():
    '''
    Scrapes baseball-reference.com game results for specified team
    Creates an array of series results (🧹=sweep, 🟢=win, 🔴=loss, 🔵=tie, ⚪=not played)
    '''

    game_results_soup = get_game_results_soup()

    counter = 0
    series_results = []
    t_sweeps = 0
    t_wins = 0
    t_losses = 0
    t_splits = 0
    last_opponent = ''
    win_count = 0
    loss_count = 0
    break_now = False

    while len(series_results) < 56: # 52 series' plus 4 newline characters
        if len(series_results) == 0:
            for game in game_results_soup:
                if 'win_loss_result' not in str(game):
                    break_now = True # if new series game hasn't happened yet, append the series result before breaking loop

                if 'thead' not in str(game):
                    opponent = game.find('td', attrs={'data-stat' : 'opp_ID'}).text

                    if counter == 13:
                        series_results.append('\n')
                        counter = 0
                    
                    if opponent != last_opponent:
                        if (win_count or loss_count): # prevents failure for first run
                            counter += 1

                            if loss_count == 0:
                                t_sweeps += 1
                                result = '🧹'
                            elif (win_count - loss_count > 0):
                                t_wins += 1
                                result = '🟢'
                            elif (win_count - loss_count < 0):
                                t_losses += 1
                                result = '🔴'
                            else:
                                t_splits += 1
                                result = '🔵'
                                
                            series_results.append(result)

                            win_count = 0
                            loss_count = 0

                    if break_now == True:
                        break
                    
                    win_or_loss = game.find('td', attrs={'data-stat' : 'win_loss_result'}).text

                    if 'W' in win_or_loss:
                        win_count += 1
                    elif 'L' in win_or_loss:
                        loss_count += 1

                    last_opponent = opponent  

        if (len(series_results) - series_results.count('\n')) % 13 == 0 and not repr(series_results[-1]) == repr('\n'):
            series_results.append('\n')
        else:
            series_results.append('⚪')   

    return { 
        'results': series_results,
        'total_sweeps': t_sweeps,
        'total_wins': t_wins, 
        'total_splits': t_splits,
        'total_losses': t_losses
    }