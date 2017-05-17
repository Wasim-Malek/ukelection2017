from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

# constituencies
urls = 'https://www.oddschecker.com/politics/british-politics/Twickenham/winning-party','https://www.oddschecker.com/politics/british-politics/Vauxhall/winning-party','https://www.oddschecker.com/politics/british-politics/Norwich-South/winning-party','https://www.oddschecker.com/politics/british-politics/Middlesbrough-South-and-East-Cleveland/winning-party','https://www.oddschecker.com/politics/british-politics/Darlington/winning-party','https://www.oddschecker.com/politics/british-politics/North-East-Derbyshire/winning-party','https://www.oddschecker.com/politics/british-politics/Croydon-Central/winning-party','https://www.oddschecker.com/politics/british-politics/South-Thanet/winning-party','https://www.oddschecker.com/politics/british-politics/Clacton/winning-party','https://www.oddschecker.com/politics/british-politics/Gower/winning-party','https://www.oddschecker.com/politics/british-politics/Derby-North/winning-party','https://www.oddschecker.com/politics/british-politics/City-Of-Chester/winning-party','https://www.oddschecker.com/politics/british-politics/Ynys-Mon/winning-party','https://www.oddschecker.com/politics/british-politics/Vale-Of-Clwyd/winning-party','https://www.oddschecker.com/politics/british-politics/Ealing-Central-and-Acton/winning-party','https://www.oddschecker.com/politics/british-politics/Berwickshire-Roxburgh-and-Selkirk/winning-party','https://www.oddschecker.com/politics/british-politics/Bury-North/winning-party','https://www.oddschecker.com/politics/british-politics/Wirral-West/winning-party','https://www.oddschecker.com/politics/british-politics/Morley-and-Outwood/winning-party','https://www.oddschecker.com/politics/british-politics/Halifax/winning-party','https://www.oddschecker.com/politics/british-politics/Brentford-and-Isleworth/winning-party','https://www.oddschecker.com/politics/british-politics/Plymouth-Sutton-and-Devonport/winning-party','https://www.oddschecker.com/politics/british-politics/Fermanagh-and-South-Tyrone/winning-party','https://www.oddschecker.com/politics/british-politics/Thurrock/winning-party','https://www.oddschecker.com/politics/british-politics/Ilford-North/winning-party','https://www.oddschecker.com/politics/british-politics/Cambridge/winning-party','https://www.oddschecker.com/politics/british-politics/Newcastle-Under-Lyme/winning-party','https://www.oddschecker.com/politics/british-politics/Brighton-Kemptown/winning-party','https://www.oddschecker.com/politics/british-politics/Telford/winning-party','https://www.oddschecker.com/politics/british-politics/Eastbourne/winning-party','https://www.oddschecker.com/politics/british-politics/Barrow-and-Furness/winning-party','https://www.oddschecker.com/politics/british-politics/Dumfriesshire-Clydesdale-and-Tweeddale/winning-party','https://www.oddschecker.com/politics/british-politics/Bolton-West/winning-party','https://www.oddschecker.com/politics/british-politics/Wolverhampton-South-West/winning-party','https://www.oddschecker.com/politics/british-politics/Weaver-Vale/winning-party','https://www.oddschecker.com/politics/british-politics/Orkney-and-Shetland/winning-party','https://www.oddschecker.com/politics/british-politics/Belfast-South/winning-party','https://www.oddschecker.com/politics/british-politics/South-Antrim/winning-party','https://www.oddschecker.com/politics/british-politics/Dartford/winning-party','https://www.oddschecker.com/politics/british-politics/Loughborough/winning-party','https://www.oddschecker.com/politics/british-politics/Northampton-North/winning-party','https://www.oddschecker.com/politics/british-politics/Portsmouth-North/winning-party','https://www.oddschecker.com/politics/british-politics/Watford/winning-party','https://www.oddschecker.com/politics/british-politics/Lincoln/winning-party','https://www.oddschecker.com/politics/british-politics/Bristol-North-West/winning-party'

# scrape
odds = []
for url in urls:
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    dump = soup.find_all('td', class_=['sel nm', "bc bs o"])
    con = [url.split('/')[5], str(datetime.now()).split()[0], datetime.now()]
    odds.append([con[0], con[1], con[2], dump])
cols = ['constituency', 'date', 'dt', 'html dump']
oddspd = DataFrame(odds, columns=cols)

# append to csv
oddspd.to_csv('C:\data\odds.csv', mode='a', header=False)
