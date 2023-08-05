from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd
import time


from selenium import webdriver
from selenium.webdriver.edge.service import Service

service = Service(executable_path="C:/Program Files/nodejs/msedgedriver.exe")
options = webdriver.EdgeOptions()
driver = webdriver.Chrome(service=service, options=options)



url_start = "https://www.basketball-reference.com/awards/awards_{}.html"
player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
teams_stat_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"

years = list(range(1991, 2022))

def data_url(url_start):

    df = []

    # download html pages to local
    for year in years:
        url =  url_start.format(year)
        data = requests.get(url)
        
        with open("mvp/{}.html".format(year), "w", encoding="utf-8") as f_in:
            f_in.write(data.text)   

    
    #  read html pages
    with open("mvp/2021.html", "r", encoding="utf-8") as f_out:
        page = f_out.read()


    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_='over_header').decompose()
    mvp_table = soup.find(id='mvp')
    mvp = pd.read_html(str(mvp_table))[0]
    mvp['year'] = year
    
    df.append(mvp)
    mvp = pd.concat(df)
    mvp.to_csv("mvps.csv")

    return mvp



def get_data_selenium(player_stats_url):
    for year in years:
        url = player_stats_url.format(year)

        driver.get(url)
        driver.execute_script("window.scrollTo(1,10000)")
        time.sleep(2)

        html = driver.page_source
        
        with open("players/{}.html".format(year), 'w+', encoding="utf-8") as f_in:
            f_in.write(html)


    df = []

    for year in years:
        
        with open("players/{}.html".format(year), "r", encoding="utf-8") as f_out:
            page = f_out.read()

        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_='thead').decompose()
        player_table = soup.find(id='per_game_stats')
        player = pd.read_html(str(player_table))[0]
        player['year'] = year
        df.append(player)

        players = pd.concat(df)
        players.to_csv("players.csv")

        return players
    


def get_teams_data():
    for year in years:
        url = teams_stat_url.format(year)

        data = requests.get(url)

        with open("teams/{}.html".format(year), "w+", encoding="utf-8") as f_in:
            page = f_in.write(data.text)

    df = []

    for year in years:

        with open("teams/{}.html".format(year), "r", encoding="utf-8") as f_out:
            page = f_out.read()

        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_='thead').decompose()
        team_table = soup.find(id="div_divs_standings_E")
        team = pd.read_html(str(team_table))[0]
        team['year'] = year
        df.append(team)

        soup = BeautifulSoup(page, "html.parser")
        soup.find('tr', class_='thead').decompose()
        team_table = soup.find(id='div_divs_standings_W')
        team = pd.read_html(str(team_table))[0]
        team['year'] = year
        df.append(team)

        teams = pd.concat(df)
        teams.to_csv('teams.csv')

        return teams