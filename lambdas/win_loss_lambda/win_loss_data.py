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
    '''Get win loss data as html soup for specified team'''

    game_results = get_html(GAME_RESULTS_URL)
    game_results_soup = BeautifulSoup(game_results, 'html.parser')

    game_results_table = game_results_soup.find('tbody')

    individual_games = game_results_table.find_all('tr')

    return individual_games


def get_win_loss_data():
    '''
    Scrapes baseball-reference.com game results for specified team
    Creates an array of game results (🟩=win, 🟥=loss)
    '''

    game_results_soup = get_game_results_soup()

    game_results = []

    for game in game_results_soup:
        if 'win_loss_result' not in str(game):
            break

        if 'thead' not in str(game):
            win_or_loss = game.find('td', attrs={'data-stat' : 'win_loss_result'}).text

            if 'W' in win_or_loss:
                game_results.append('🟩')
            elif 'L' in win_or_loss:
                game_results.append('🟥')
            else:
                raise Exception("Error: couldn't identify win or loss")

    data = {
        'results': game_results,
        'record': f'{len([x for x in game_results if x == "🟩"])}-{len([x for x in game_results if x == "🟥"])}'
    }
    
    return data

get_win_loss_data()