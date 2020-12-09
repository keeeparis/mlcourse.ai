# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 03:21:55 2020

@author: Republic of Gamers
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import set_matplotlib_formats
set_matplotlib_formats('retina')   #'jpg', 'png', 'pdf'...

pd.set_option('display.precision', 2)
pd.set_option('display.max_columns', 0)       #all lines should be written with print()
                                              #in front in order to be visualised
#get datafile
df = pd.read_csv('dataset_1.csv')
#first 5 observations
df.head()
#size(n_rows,n_columns)
df.shape
#column names
df.columns
#info about data types
#df.info()

# change type of data in column
df['churn'] = df['churn'].astype('int64')

#statistical info about numerical columns- mean, std, min/max...
df.describe()
#info on non-numerical
df.describe(include=['object', 'bool'])
#distribution of zeros and ones
df['churn'].value_counts()
#same but in fractions
df['churn'].value_counts(normalize=True)

##SORTING

df.sort_values(by='total day charge', ascending=False).head()
#multiple feature sorting
df.sort_values(by=['churn', 'total day charge'], ascending=[True, False]).head()

##INDEXING
# what is the propotion of churned users in dataframe?
df['churn'].mean()
# what are the average values for churned users?
df[df['churn'] == 1].mean()
# how much on average do churned users spend on the phone during daytime?
df[df['churn'] == 1]['total day minutes'].mean()
# what is max length of int calls among loyal users who don't have int plan?
df[(df['churn'] == 0) & (df['international plan'] == 'no')]['total intl minutes'].max()

#give us the rows from 0 to 5 and columns from 'state' to 'area code'
df.loc[0:5, 'state':'area code']
# loc method - indexing by name, iloc - by number (results are the same)
df.iloc[0:5, 0:3]

##APPLYING FUNCTIONS TO CELLS, COLUMNS, ROWS

df.apply(np.max)
#select all states that starts with 'W'
df[df['state'].apply(lambda state: state[0]=='W')].head()
# map method to replace old values with new ones
d = {'no' : False, 'yes' : True}
df['international plan'] = df['international plan'].map(d)
# the same with replace method
df = df.replace({'voice mail plan' : d})

##GROUPING

#group date according to the values in 'churn' and display statistics
#of three columns in each group
columns_to_show = ['total day minutes', 'total eve minutes', 'total night minutes']
df.groupby(['churn'])[columns_to_show].describe(percentiles=[])
#same but using agg() to pass a list of functions to apply
df.groupby(['churn'])[columns_to_show].agg([np.mean, np.std, np.min, np.max])


##SUMMARY TABLES

#contingency table
pd.crosstab(df['churn'], df['international plan'])
pd.crosstab(df['churn'], df['voice mail plan'], normalize=True)
#pivot table
df.pivot_table(['total day calls', 'total eve calls', 'total night calls'], ['area code'], aggfunc='mean')


##TRANSFORMATIONS

#add new column
df['total calls'] = df['total day calls'] + df['total eve calls'] + \
                    df['total night calls'] + df['total intl calls']
#delete columns/rows
#axis=1 means columns, axis=0 or nothing means rows
#inplace=True means change current dataframe, =false means create new/changed one 
df.drop(['total calls'], axis=1, inplace=True)


#######
## 2 ##
#######


# pd.crosstab(df['churn'], df['international plan'], margins=True)
# sns.countplot(x='international plan', hue = 'churn', data = df)

# pd.crosstab(df['churn'], df['customer service calls'], margins=True)
# sns.countplot(x='customer service calls', hue = 'churn', data = df)

df['many_service_calls'] = (df['customer service calls'] > 3).astype('int')
pd.crosstab(df['many_service_calls'], df['churn'], margins=True)
sns.countplot(x='many_service_calls', hue = 'churn', data = df)

pd.crosstab(df['many_service_calls'] & df['international plan'], df['churn'])









