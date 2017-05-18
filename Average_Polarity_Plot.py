
# coding: utf-8

# In[1]:

import pymongo
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
from pandas import DataFrame, TimeSeries

import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import plotly
import cufflinks as cf
import json
from pandas.io.json import json_normalize
get_ipython().magic(u'matplotlib inline')
def connect_to_mongo():
    try:
        client = MongoClient()
        print 'Connection to Mongo successful'
    except pymongo.errors.ConnectionFailure as e:
        print e
        return

    return client

def connect_to_collection(db_string, coll_string):
    try:

        client = connect_to_mongo()
        db = client[db_string]
        collection = db[coll_string]
        print 'Connection to collection successful'
    except pymongo.errors.ConnectionFailure as e:
        print e
        return
    return collection


def tweets_into_DataFrame(Collection):

    query = {'Polarity':1,'text':1,'Subjectivity':1,'created_at':1,'Party':1}


    data = json_normalize(list(Collection.find(filter = {}, projection = query)))

    #data = DataFrame(list(Collection.find()))
    return data


# In[2]:

col = connect_to_collection('tweetsdb','nationaltweets')

data = tweets_into_DataFrame(col) # ALL DATA

data['created_at'] = pd.to_datetime(data['created_at'])


# In[3]:

Con_Data = data[data['Party']=='Conservative']
Labour_Data = data[data['Party'] == 'labour']
LibDem_Data = data[data['Party'] == 'libDem']


# In[4]:

Con_Data.set_index(['created_at'], inplace = True)

Labour_Data.set_index(['created_at'], inplace = True)

LibDem_Data.set_index(['created_at'], inplace = True)


# In[5]:

#LibDem_Data.head()


# In[6]:

#Labour_Data.head()


# In[7]:

Time_Series = Con_Data['Polarity']
Time_SeriesLab = Labour_Data['Polarity']
Time_SeriesLib = LibDem_Data['Polarity']


# In[8]:

#Time_SeriesLab.head()


# In[9]:

df=DataFrame(Time_Series)
df.reset_index(inplace = True)

dfLab=DataFrame(Time_SeriesLab)
dfLab.reset_index(inplace = True)

dfLib=DataFrame(Time_SeriesLib)
dfLib.reset_index(inplace = True)




# In[10]:

#dfLib.head()


# In[11]:

df.index = df['created_at']
dfLab.index = dfLab['created_at']
dfLib.index = dfLib['created_at']


# In[ ]:




# In[12]:

#df.resample('H')
#dfLab.resample('H')
#dfLib.resample('H')


# In[13]:

df2 = df.resample('6H').mean()
df3 = dfLab.resample('6H').mean()
df4 = dfLib.resample('6H').mean()

trace = go.Scatter(
    x = df2.index,
    y = df2.fillna(df2.mean())['Polarity'],
    name = 'Conservative'
    
)
trace1 = go.Scatter(
    x = df3.index,
    y = df3.fillna(df3.mean())['Polarity'],
    name = 'Labour'
)
trace2 = go.Scatter(
    x = df4.index,
    y = df4.fillna(df4.mean())['Polarity'],
    name = 'LibDem'
)

data = [trace ,trace1, trace2]


# In[14]:

py.iplot(data)


# In[15]:

trace = go.Box(
    x = df2.index,
    y = df2.fillna(df2.mean())['Polarity'],
    name = 'Conservative'
    
)
trace1 = go.Box(
    x = df3.index,
    y = df3.fillna(df3.mean())['Polarity'],
    name = 'Labour'
)
trace2 = go.Box(
    x = df4.index,
    y = df4.fillna(df4.mean())['Polarity'],
    name = 'LibDem'
)

data = [trace ,trace1, trace2]


# In[16]:

py.iplot(data)


# In[ ]:



