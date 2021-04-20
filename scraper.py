import os
import random
import time
from datetime import datetime, date

import pandas as pd
import requests
from bs4 import BeautifulSoup

dates = []
f_date = []
titles = []
links = []
user_agents = []

with open('static/txt/useragents.txt', 'r') as ua:
    ua = ua.readlines()
    for p in ua:
        p = p.replace('\n', '')
        user_agents.append(p)

headers = {
    "User-Agent": random.choice(user_agents),
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive"
}


def LocaleGet(locale):
    codes = {
        'usa': 'hl=en-US&gl=US&ceid=US:en',
        'india': 'hl=en-IN&gl=IN&ceid=IN:en',
        'england': 'hl=en-GB&gl=GB&ceid=GB:en',
        'malaysia': 'hl=en-MY&gl=MY&ceid=MY:en',
        'canada': 'hl=en-CA&gl=CA&ceid=CA:en',
        'germany': 'gl=DE&hl=de&ceid=DE:de',
        'russia': 'gl=RU&hl=ru&ceid=RU:ru',
        'vietnam': 'gl=VN&hl=vi&ceid=VN:vi',
    }

    if locale.lower() in codes:
        location = codes.get(locale.lower())
        return location



def News(thing, count, location):
    global df_titles

    for i, j in zip(thing, count):
        # Initialize BeautifulSoup and requests
        URL = f"https://news.google.com/rss/search?q={i}&{location}"
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'xml')

        # Link filtering
        link_ = soup.find_all("link")
        for v in link_:
            links.append(v.get_text())

        # Title filtering
        title_ = soup.find_all("title")
        for v in title_:
            titles.append(v.get_text())

        # Date filtering
        Date_ = soup.find_all("pubDate")
        for n in Date_:
            dates.append(n.get_text())

        for t in dates:
            obj = datetime.strptime(t, '%a, %d %b %Y %H:%M:%S %Z')
            d = date(year=obj.year, month=obj.month, day=obj.day)
            f_date.append(d.strftime('%d-%b-%Y'))

        # Create dictionary
        t_dictionary = dict(zip(titles, f_date))
        l_dictionary = dict(zip(links, f_date))

        for key, value in dict(t_dictionary).items():
            vald = datetime.strptime(value, '%d-%b-%Y')
            today = date.today()

            if vald.month == today.month:
                if vald.day >= int(today.day) - 1:
                    pass
                else:
                    del t_dictionary[f'{key}']
            else:
                del t_dictionary[f'{key}']

            pass

        for key, value in dict(l_dictionary).items():
            vald = datetime.strptime(value, '%d-%b-%Y')
            today = date.today()

            if vald.month == today.month:
                if vald.day >= int(today.day) - 1:
                    pass
                else:
                    del l_dictionary[f'{key}']
            else:
                del l_dictionary[f'{key}']

            pass

        final_titles = list(t_dictionary.keys())
        final_links = list(l_dictionary.keys())

        final_titles.pop(0)
        final_links.pop(0)

        n_links = final_links[:int(j)]
        n_titles = final_titles[:int(j)]

        # Export data
        try:
            df_titles = pd.DataFrame(n_titles, columns=['titles'])
            df_titles.to_csv(f'titles/{i}.csv', encoding='utf-8')
        except:
            os.mkdir('titles')
            df_titles = pd.DataFrame(n_titles, columns=['titles'])
            df_titles.to_csv(f'titles/{i}.csv', encoding='utf-8')

        try:
            df_links = pd.DataFrame(n_links, columns=['links'])
            df_links.to_csv(f'links/{i}.csv', encoding='utf-8')
        except:
            os.mkdir('links')
            df_links = pd.DataFrame(n_links, columns=['links'])
            df_links.to_csv(f'links/{i}.csv', encoding='utf-8')

        # Reset lists so no overlap occurs
        del titles[:]
        del final_titles[:]
        del n_titles[:]

        del links[:]
        del final_links[:]
        del n_links[:]

        print(f"{i}'s news scraped successfully.")

        time.sleep(2)


def Import(things):
    for i in things:
        df_t = pd.read_csv(f'titles/{i}.csv', encoding='utf-8')
        df_l = pd.read_csv(f'links/{i}.csv', encoding='utf-8')

        title_list = df_t['titles'].tolist()
        link_list = df_l['links'].tolist()

        return title_list, link_list


def Exterminate(things):
    for i in things:
        os.remove(f'titles/{i}.csv')
        os.remove(f'links/{i}.csv')
