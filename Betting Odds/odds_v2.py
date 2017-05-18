from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

# initialise soup and df
odds = []
url = 'https://www.oddschecker.com/politics/british-politics/next-uk-general-election/most-seats'
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'lxml')
dump = soup.find_all('td', class_=['sel nm', 'bc bs o', 'bc bs o b', 'np o', 'bc bs oo', 'bc bs oi b'])
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
oddspd[col1] = float(odd1[s1:e1])

s2 = odd2.find("\"") + 1
e2 = odd2.find("\"", odd2.find("\"")+1)
oddspd[col2] = float(odd2[s2:e2])

s3 = odd3.find("\"") + 1
e3 = odd3.find("\"", odd3.find("\"")+1)
oddspd[col3] = float(odd3[s3:e3])

s4 = odd4.find("\"") + 1
e4 = odd4.find("\"", odd4.find("\"")+1)
oddspd[col4] = float(odd4[s4:e4])

s5 = odd5.find("\"") + 1
e5 = odd5.find("\"", odd5.find("\"")+1)
oddspd[col5] = float(odd5[s5:e5])

# append to csv
oddspd.to_csv('C:\data\odds_national_v2.csv', mode='a', header=False)
