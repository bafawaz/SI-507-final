# name: Bilal Fawaz
# unique name: bafawaz


from enum import unique
from ntpath import join
from re import T
import requests
from bs4 import BeautifulSoup
import pandas as pd
import ast
from collections import defaultdict, Counter
import ast
import seaborn as sns
import numpy as np
from collections import Counter
from click import style
import matplotlib.pyplot as plt

url = ('https://www.skysports.com/premier-league-table')

r = requests.get(url)
# print(r.status_code) # gives us back 200

soup = BeautifulSoup(r.text, 'html.parser')


league_table = soup.find('table', class_ = 'standing-table__table callfn') # table info

pl_table = [] # stores the table (live and current)
for team in league_table.find_all('tbody'):
    rows = team.find_all('tr')
    for row in rows:
        pl_team = row.find('td', class_ = 'standing-table__cell standing-table__cell--name').text.strip()
        pl_points = row.find_all('td', class_ = 'standing-table__cell')[9].text
        pl_page1 = pl_team +':' + ' ' + pl_points + ' ' + 'points' # combines the two information
        # pl_page1 = pl_page1.split('\n')
        pl_table.append(pl_page1)



url_2 = ('https://www.skysports.com/football-results')

r_2 = requests.get(url_2)

soup_2 = BeautifulSoup(r_2.text, 'html.parser')

league_results = soup_2.find_all('div', class_ = 'fixres__item') # match results info

pl_matches = []  # stores all of the fixures
for day in league_results:
    opp1 = day.find('span', class_ = 'matches__item-col matches__participant matches__participant--side1').text.strip()
    opp2 = day.find('span', class_ = 'matches__item-col matches__participant matches__participant--side2').text.strip()
    full_time = day.find('span', class_ = 'matches__teamscores').text.strip()
    pl_page2 = f"{opp1} {full_time[0]} vs {opp2} {full_time[-1]}"
    pl_matches.append(pl_page2)
    # print(f"{opp1} vs {opp2}, result:\n{full_time}")
    # print(full_time.rfind('2            \n\n                4'))



teams = ['Manchester City', 'Liverpool', 'Chelsea', 'Arsenal', 'Tottenham Hotspur', 'Manchester United', 'West Ham United', 'Wolverhampton Wanderers', 'Newcastle United', 'Leicester City',
'Brighton and Hove Albion', 'Brentford', 'Southampton', 'Crystal Palace', 'Aston Villa', 'Leeds United', 'Burnley', 'Everton', 'Watford', 'Norwich City']


# getstting a dataframe of the table info using pandas
df1 = pd.read_html('https://www.skysports.com/premier-league-table', header= 0)
df = df1[0]


actual_fixtures = [] # contains only premier leagure fixures that we are interested in

for x in teams:
    for i in pl_matches:
        if x in i and 'Women' not in i and 'Ladies' not in i:
            actual_fixtures.append(i)


def get_unique_list(numbers):
    # takes a list and returns all unique elements

    list_of_unique = []

    unique_numbers = set(numbers)

    for number in unique_numbers:
        list_of_unique.append(number)

    return list_of_unique


# adding fixures (match results) column to df to make it easier to work with
for i, v in df['Team'].iteritems():
    for x in get_unique_list(actual_fixtures):
        if v in x:
            df.loc[df['Team'].str.contains(v),'Fixtures'] = x


# print(df)


class Teams:
    # parent class for all teams
    def __init__(self, row):
        self.name = row['Team']
        self.fixtures = row['Fixtures']
        self.pts = row['Pts']
        self.rank = row['#']

    def fixtures_info(self):
        if self.fixtures:
            return f"Recent fixures include {self.fixtures}"
        else:
            return f"{self.name} has no recent fixures"

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th." # for the middle of the table (ones with no rank or releg)


class Champs(Teams):
    # subclass for teams that qualify for champions league
    def __init__(self, row):
        super().__init__(row)
        self.champseleg = True

    def info(self):
        if self.rank == 1:
            return f"{self.name} has {self.pts} points and is in {self.rank}st and is elegible for the Champions League."
        elif self.rank == 2:
            return f"{self.name} has {self.pts} points and is in {self.rank}nd and is elegible for the Champions League."
        elif self.rank == 3:
            return f"{self.name} has {self.pts} points and is in {self.rank}rd and is elegible for the Champions League."
        else:
            return f"{self.name} has {self.pts} points and is in {self.rank}th and is elegible for the Champions League."


class Euro(Teams):
    # subclass for teams that qualify for europa league
    def __init__(self, row):
        super().__init__(row)
        self.euro = True

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th and is elegible for the Europa League."


class PlayIn(Teams):
    # subclass for teams that qualify for play ins
    def __init__(self, row):
        super().__init__(row)
        self.play_in = True

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th and is elegible for play-ins."


class Relegation(Teams):
    # subclass for teams that are at risk of relegation
    def __init__(self, row):
        super().__init__(row)
        self.releg = True

    def info(self):
        return f"{self.name} has {self.pts} points and is in {self.rank}th and is in relegation"



instance_dict = {'champs' : [], 'euro' : [], 'play_in' : [], 'relegation' : [], 'other_teams' : []}

for i, r in df.iterrows():
    if int(r['#']) <= 4:
        instance = Champs(r)
        instance_dict['champs'].append(instance)
    elif int(r['#']) == 5:
        instance = Euro(r)
        instance_dict['euro'].append(instance)
    elif int(r['#']) == 6:
        instance = PlayIn(r)
        instance_dict['play_in'].append(instance)
    elif int(r['#']) >= 18:
        instance = Relegation(r)
        instance_dict['relegation'].append(instance)
    else:
        instance = Teams(r)
        instance_dict['other_teams'].append(instance)



search_ = input('Please enter a team name or enter table: ')


while True:
    while True:
        if search_.title() not in teams and search_.lower() != 'table':
            search_ = input('Invalid search, please try again: ')
            continue
        else:
            break

    if search_.lower() == 'table':
        print(plt.figure(figsize=(12,8)))
        print(sns.barplot(data = df
            ,x = 'Pts'
            ,y = 'Team'
            ,ci = None
            ))
        print(plt.title('Current Premier League Table'))
        print(plt.show())

    else:
        for k, v in instance_dict.items():
            for i in v:
                if search_.title() == i.name:
                    print(i.info())
                    print(i.fixtures_info())
                # print(i.info())

    search_ = input('Please enter another team name or table for more information, or exit to leave program: ')
    if search_ == 'exit':
        break
    else:
        continue


