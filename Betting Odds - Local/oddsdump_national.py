from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series


# scrape
odds = []
url = 'https://www.oddschecker.com/politics/british-politics/next-uk-general-election/most-seats'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'lxml')
dump = soup.find_all('td', class_=['sel nm', "bc bs o"])
con = [url.split('/')[5], str(datetime.now()).split()[0], datetime.now()]
odds.append([con[0],con[1],con[2],dump])
cols = ['constituency','date','dt','html dump']
oddspd = DataFrame(odds, columns=cols)

# append to csv
oddspd.to_csv('C:\data\odds_national.csv', mode='a')
