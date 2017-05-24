from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

# initialise soup and df
urls = ['https://www.oddschecker.com/politics/british-politics/Twickenham/winning-party','https://www.oddschecker.com/politics/british-politics/Vauxhall/winning-party','https://www.oddschecker.com/politics/british-politics/Norwich-South/winning-party','https://www.oddschecker.com/politics/british-politics/Middlesbrough-South-and-East-Cleveland/winning-party','https://www.oddschecker.com/politics/british-politics/Darlington/winning-party','https://www.oddschecker.com/politics/british-politics/North-East-Derbyshire/winning-party','https://www.oddschecker.com/politics/british-politics/Croydon-Central/winning-party','https://www.oddschecker.com/politics/british-politics/South-Thanet/winning-party','https://www.oddschecker.com/politics/british-politics/Clacton/winning-party','https://www.oddschecker.com/politics/british-politics/Gower/winning-party','https://www.oddschecker.com/politics/british-politics/Derby-North/winning-party','https://www.oddschecker.com/politics/british-politics/City-Of-Chester/winning-party','https://www.oddschecker.com/politics/british-politics/Ynys-Mon/winning-party','https://www.oddschecker.com/politics/british-politics/Vale-Of-Clwyd/winning-party','https://www.oddschecker.com/politics/british-politics/Ealing-Central-and-Acton/winning-party','https://www.oddschecker.com/politics/british-politics/Berwickshire-Roxburgh-and-Selkirk/winning-party','https://www.oddschecker.com/politics/british-politics/Bury-North/winning-party','https://www.oddschecker.com/politics/british-politics/Wirral-West/winning-party','https://www.oddschecker.com/politics/british-politics/Morley-and-Outwood/winning-party','https://www.oddschecker.com/politics/british-politics/Halifax/winning-party','https://www.oddschecker.com/politics/british-politics/Brentford-and-Isleworth/winning-party','https://www.oddschecker.com/politics/british-politics/Plymouth-Sutton-and-Devonport/winning-party','https://www.oddschecker.com/politics/british-politics/Fermanagh-and-South-Tyrone/winning-party','https://www.oddschecker.com/politics/british-politics/Thurrock/winning-party','https://www.oddschecker.com/politics/british-politics/Ilford-North/winning-party','https://www.oddschecker.com/politics/british-politics/Cambridge/winning-party','https://www.oddschecker.com/politics/british-politics/Newcastle-Under-Lyme/winning-party','https://www.oddschecker.com/politics/british-politics/Brighton-Kemptown/winning-party','https://www.oddschecker.com/politics/british-politics/Telford/winning-party','https://www.oddschecker.com/politics/british-politics/Eastbourne/winning-party','https://www.oddschecker.com/politics/british-politics/Barrow-and-Furness/winning-party','https://www.oddschecker.com/politics/british-politics/Dumfriesshire-Clydesdale-and-Tweeddale/winning-party','https://www.oddschecker.com/politics/british-politics/Bolton-West/winning-party','https://www.oddschecker.com/politics/british-politics/Wolverhampton-South-West/winning-party','https://www.oddschecker.com/politics/british-politics/Weaver-Vale/winning-party','https://www.oddschecker.com/politics/british-politics/Orkney-and-Shetland/winning-party','https://www.oddschecker.com/politics/british-politics/Belfast-South/winning-party','https://www.oddschecker.com/politics/british-politics/South-Antrim/winning-party','https://www.oddschecker.com/politics/british-politics/Dartford/winning-party','https://www.oddschecker.com/politics/british-politics/Loughborough/winning-party','https://www.oddschecker.com/politics/british-politics/Northampton-North/winning-party','https://www.oddschecker.com/politics/british-politics/Portsmouth-North/winning-party','https://www.oddschecker.com/politics/british-politics/Watford/winning-party','https://www.oddschecker.com/politics/british-politics/Lincoln/winning-party','https://www.oddschecker.com/politics/british-politics/Bristol-North-West/winning-party']
for url in urls:
    odds = []
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    dump = soup.find_all('td', class_=['sel nm', 'bc bs o', 'bc bs o b', 'bc bs oo', 'bc bs oi b'])
    con = [url.split('/')[5], str(datetime.now()).split()[0], datetime.now()]
    odds.append([con[0], con[1], con[2], dump])
    cols = ['constituency', 'date', 'dt', 'html dump']
    oddspd = DataFrame(odds, columns=cols)

    # find headers
    z = []
    for i in oddspd['html dump'][0]:
        z.append(str(i).find('<td class="sel nm">'))
    ind = [i for i, val in enumerate(z) if val == 0]

    # column names
    col1 = str(oddspd['html dump'][0][0]).split()[4]  # con
    col2 = str(oddspd['html dump'][0][ind[1]]).split()[4]  # lab
    col3 = str(oddspd['html dump'][0][ind[2]]).split()[4]  # lib
    col4 = str(oddspd['html dump'][0][ind[3]]).split()[4]  # UKIP
    col5 = str(oddspd['html dump'][0][ind[4]]).split()[4]  # green

    # raw odds
    odd1 = str(oddspd['html dump'][0][1]).split()[6]
    odd2 = str(oddspd['html dump'][0][ind[1]+1]).split()[6]
    odd3 = str(oddspd['html dump'][0][ind[2]+1]).split()[6]
    odd4 = str(oddspd['html dump'][0][ind[3]+1]).split()[6]
    odd5 = str(oddspd['html dump'][0][ind[4]+1]).split()[6]

    # convert to floats
    s1 = odd1.find("\"") + 1
    e1 = odd1.find("\"", odd1.find("\"")+1)
    try:
        oddspd[col1] = float(odd1[s1:e1])
    except:
        oddspd[col1] = float(odd1[s1:e1].split('/')[0]) / float(odd1[s1:e1].split('/')[1]) + 1

    s2 = odd2.find("\"") + 1
    e2 = odd2.find("\"", odd2.find("\"")+1)
    try:
        oddspd[col2] = float(odd2[s2:e2])
    except:
        oddspd[col2] = float(odd2[s2:e2].split('/')[0]) / float(odd2[s2:e2].split('/')[1]) + 1

    s3 = odd3.find("\"") + 1
    e3 = odd3.find("\"", odd3.find("\"")+1)
    oddspd[col3] = str(odd3[s3:e3])

    s4 = odd4.find("\"") + 1
    e4 = odd4.find("\"", odd4.find("\"")+1)
    oddspd[col4] = str(odd4[s4:e4])

    s5 = odd5.find("\"") + 1
    e5 = odd5.find("\"", odd5.find("\"")+1)
    oddspd[col5] = str(odd5[s5:e5])

    # append to csv
    path = 'C:\data\local\\' + str(con[0]) + '.csv'
    oddspd.to_csv(path, mode='a', header=False)
