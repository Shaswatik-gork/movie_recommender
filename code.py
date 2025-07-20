import numpy as np
import pandas as pd
column_names = ['user_id','item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=column_names)
movie_titles = pd.read_csv('Movie_Id_Titles.txt')
movie_titles.head()
df = pd.merge(df, movie_titles, on='item_id')

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
df.groupby('title')['rating'].mean().sort_values(ascending=False).head(20)
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())

ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
pivot_table = df.pivot_table(index='user_id', columns='title', values='rating')
starwars_rating = pivot_table['Star Wars (1977)']
starwars_rating.head(10)
similar_to_starwars = pivot_table.corrwith(starwars_rating)
corr_starwars = pd.DataFrame(similar_to_starwars, columns=['Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars.head(10)
corr_starwars.sort_values('Correlation', ascending=False)
corr_starwars = corr_starwars.join(ratings['num of ratings'])
corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation', ascending=False).head(10)
