# -*- encoding: utf-8 -*-
'''
Created on 2016年6月17日
@author: LuoPei
'''
from __future__ import division
import json
path = 'usagov_bitly_data2012-03-16-1331923249.txt'
open(path).readline()
path = 'usagov_bitly_data2012-03-16-1331923249.txt'
records = [json.loads(line) for line in open(path)]

print(records[0]['tz'])

# time_zones = [rec['tz'] for rec in records] 有些记录没有tz字段，所有需要用下面一行代码~
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

print time_zones[:10]

def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts
from collections import defaultdict
def get_counts2(sequence):
    counts = defaultdict(int) # values will initialize to 0
    for x in sequence:
        counts[x] += 1
    return counts
counts = get_counts(time_zones)
print counts['America/New_York']
print len(time_zones)

def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]
print "top_counts_func1: ",top_counts(counts)

import operator
def top_counts_02(count_dict, n=10):
    sortedCount_dict=sorted(count_dict.items(),key=operator.itemgetter(1))
    return sortedCount_dict[-n:]
print "top_counts_func2: ",top_counts_02(counts)

from collections import Counter
counts = Counter(time_zones)
print "top_counts_func3: ",counts.most_common(10)

# ### Counting time zones with pandas
from numpy.random import randn
import numpy as np
import os
import matplotlib.pylab as plt
import pandas as pd
plt.rc('figure', figsize=(10, 6))
np.set_printoptions(precision=4)

import json
path = 'usagov_bitly_data2012-03-16-1331923249.txt'
lines = open(path).readlines()
records = [json.loads(line) for line in lines]
from pandas import DataFrame, Series
import pandas as pd
frame = DataFrame(records)
print frame
print frame['tz'][:10]

tz_counts = frame['tz'].value_counts()
print tz_counts[:10]

clean_tz = frame['tz'].fillna('Missing') #na值用Missing代替
clean_tz[clean_tz == ''] = 'Unknown' #空字符串用Unkown代替
tz_counts = clean_tz.value_counts()
print tz_counts[:10]

plt.figure(figsize=(10, 4))
tz_counts[:10].plot(kind='barh', rot=0)
print frame['a'][1]
print frame['a'][50]
print frame['a'][51]

results = Series([x.split()[0] for x in frame.a.dropna()])
print results[:5]
print results.value_counts()[:8]
cframe = frame[frame.a.notnull()]
operating_system = np.where(cframe['a'].str.contains('Windows'),
                            'Windows', 'Not Windows')
print operating_system[:5]

by_tz_os = cframe.groupby(['tz', operating_system])
agg_counts = by_tz_os.size().unstack().fillna(0)
print agg_counts[:10]


# Use to sort in ascending order
indexer = agg_counts.sum(1).argsort()
print indexer[:10]
count_subset = agg_counts.take(indexer)[-10:]
print count_subset
plt.figure()
count_subset.plot(kind='barh', stacked=True)
plt.show()
plt.figure()
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)
plt.show()

# ## MovieLens 1M data set
import pandas as pd
import os
encoding = 'latin1'
upath = os.path.expanduser('movielens/users.dat')
rpath = os.path.expanduser('movielens/ratings.dat')
mpath = os.path.expanduser('movielens/movies.dat')
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
mnames = ['movie_id', 'title', 'genres']
users = pd.read_csv(upath, sep='::', header=None, names=unames, encoding=encoding)
ratings = pd.read_csv(rpath, sep='::', header=None, names=rnames, encoding=encoding)
movies = pd.read_csv(mpath, sep='::', header=None, names=mnames, encoding=encoding)
print users[:5]
print ratings[:5]
print movies[:5]
print ratings

data = pd.merge(pd.merge(ratings, users), movies)
print data
print data.ix[0]
mean_ratings = data.pivot_table('rating', index='title',
                                columns='gender', aggfunc='mean')
print mean_ratings[:5]
ratings_by_title = data.groupby('title').size()
print ratings_by_title[:5]
active_titles = ratings_by_title.index[ratings_by_title >= 250]
print active_titles[:10]
mean_ratings = mean_ratings.ix[active_titles]
print mean_ratings
mean_ratings = mean_ratings.rename(index={'Seven Samurai (The Magnificent Seven) (Shichinin no samurai) (1954)':
                           'Seven Samurai (Shichinin no samurai) (1954)'})
top_female_ratings = mean_ratings.sort_index(by='F', ascending=False)
print top_female_ratings[:10]


# ### Measuring rating disagreement
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_index(by='diff')
print sorted_by_diff[:15]
# Reverse order of rows, take first 15 rows
print sorted_by_diff[::-1][:15]
# Standard deviation of rating grouped by title
rating_std_by_title = data.groupby('title')['rating'].std()
# Filter down to active_titles
rating_std_by_title = rating_std_by_title.ix[active_titles]
# Order Series by value in descending order
print rating_std_by_title.order(ascending=False)[:10]



# ### US Baby Names 1880-2010
from numpy.random import randn
import numpy as np
import matplotlib.pyplot as plt
plt.rc('figure', figsize=(12, 5))
np.set_printoptions(precision=4)
# http://www.ssa.gov/oact/babynames/limits.html

import pandas as pd
names1880 = pd.read_csv('names/yob1880.txt', names=['name', 'sex', 'births'])
print names1880

names1880.groupby('sex').births.sum()

# 2010 is the last available year right now
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = 'names/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)
    
# Concatenate everything into a single DataFrame
names = pd.concat(pieces, ignore_index=True)
total_births = names.pivot_table('births', index='year',
                                 columns='sex', aggfunc=sum)
print total_births.tail()
plt.figure()
total_births.plot(title='Total births by sex and year')
plt.show()


def add_prop(group):
    # Integer division floors
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group
names = names.groupby(['year', 'sex']).apply(add_prop)
print "names:",names
print "isclosed? :", np.allclose(names.groupby(['year', 'sex']).prop.sum(), 1)

def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]
grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
pieces = []
for year, group in names.groupby(['year', 'sex']):
    pieces.append(group.sort_index(by='births', ascending=False)[:1000])
top1000 = pd.concat(pieces, ignore_index=True)
top1000.index = np.arange(len(top1000))
print top1000
# ### Analyzing naming trends
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
total_births = top1000.pivot_table('births', index='year', columns='name',
                                   aggfunc=sum)
print total_births

plt.figure()
subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
subset.plot(subplots=True, figsize=(12, 10), grid=False,
            title="Number of births per year")
plt.show()


# #### Measuring the increase in naming diversity
plt.figure()
table = top1000.pivot_table('prop', index='year',
                            columns='sex', aggfunc=sum)
table.plot(title='Sum of table1000.prop by year and sex',
           yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
df = boys[boys.year == 2010]
df
prop_cumsum = df.sort_index(by='prop', ascending=False).prop.cumsum()
prop_cumsum[:10]
prop_cumsum.values.searchsorted(0.5)
df = boys[boys.year == 1900]
in1900 = df.sort_index(by='prop', ascending=False).prop.cumsum()
in1900.values.searchsorted(0.5) + 1

def get_quantile_count(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1
diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')

def get_quantile_count_02(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False)
    return group.prop.cumsum().values.searchsorted(q) + 1

diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count_02)
diversity = diversity.unstack('sex')
print diversity.head()
diversity.plot(title="Number of popular names in top 50%")
plt.show()

# #### The "Last letter" Revolution
# extract last letter from name column
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births', index=last_letters,
                          columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
subtable.head()
subtable.sum()
letter_prop = subtable / subtable.sum().astype(float)
import matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female',
                      legend=False)
plt.subplots_adjust(hspace=0.25)
plt.show()
letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
dny_ts.head()
plt.close('all')
dny_ts.plot()
plt.show()

# #### Boy names that became girl names (and vice versa)
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
print lesley_like
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()
table = filtered.pivot_table('births', index='year',
                             columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
table.tail()
plt.close('all')
table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()
