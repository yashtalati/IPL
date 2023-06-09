# -*- coding: utf-8 -*-
"""new.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ff07c8Ywqrkh757g_5Wrz88nk-3L9gUE
"""

import pandas as pd
import numpy as np

match = pd.read_csv('/content/drive/MyDrive/IPL/IPL_Matches_2008_2022.csv')
delivery = pd.read_csv('/content/drive/MyDrive/IPL/IPL_Ball_by_Ball_2008_2022.csv')

total_score_df = delivery.groupby(['ID', 'innings']).sum()['total_run'].reset_index()

total_score_df = total_score_df[total_score_df['innings'] == 1]
total_score_df.head()

match_df = match.merge(total_score_df[['ID', 'total_run']], on='ID')

match_df.head(2)

teams = [
    'Chennai Super Kings',
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Punjab Kings',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Gujarat Titans',
    'Lucknow Super Giants'
]

match_df.replace('Gujarat Lions', 'Gujarat Titans', inplace=True)
match_df.replace('Delhi Daredevils', 'Delhi Capitals', inplace=True)
match_df.replace('Pune Warriors ', 'Lucknow Super Giants', inplace=True)
match_df.replace('Deccan Chargers', 'Sunrisers Hyderabad', inplace=True)
match_df.replace('Rising Pune Supergiant', 'Lucknow Super Giants', inplace=True)
match_df.replace('Kings XI Punjab', 'Punjab Kings', inplace=True)

match_df = match_df[match_df['Team1'].isin(teams)]
match_df = match_df[match_df['Team2'].isin(teams)]

match_df['Team1'].unique()

match_df['method'].unique()

match_df = match_df[match_df['method'] != 'D/L']

fdf= match_df

fdf = match_df[['ID', 'City', 'WinningTeam', 'total_run' , 'Team1' , 'Team2']]

fdf

delivery_df =  fdf.merge(delivery, on='ID')

delivery_df = delivery_df[delivery_df['innings'] == 2]

delivery_df['current_score']= delivery_df.groupby('ID').cumsum()['total_run_y']

delivery_df['runs_left']= delivery_df['total_run_x'] - delivery_df['current_score']

delivery_df.head(6)

delivery_df['balls_left']= 120 - (delivery_df['overs']*6 + delivery_df['ballnumber'])

delivery_df['player_out'] = delivery_df['player_out'].fillna("0")

delivery_df['player_out'] = delivery_df['player_out'].apply(lambda x:x if x=='0' else "1")

delivery_df.tail(5)

delivery_df['player_out'] = delivery_df['player_out'].astype('int')
wicket = delivery_df.groupby('ID').cumsum()['player_out'].values
delivery_df['wicket'] = 10-wicket

delivery_df['crr']=  (delivery_df['current_score']*6) / (120-delivery_df['balls_left'])
delivery_df['rrr']=  (delivery_df['runs_left']*6)/(delivery_df['balls_left'])

delivery_df.head(10)

def result(row):
    return 1 if row['BattingTeam'] == row['WinningTeam'] else 0

delivery_df['result'] = delivery_df.apply(result, axis=1)
delivery_df.tail(1)

d = delivery_df

Team1_mask = d['BattingTeam'] == d['Team1']

Team2_mask = d['BattingTeam'] == d['Team2']

d['BowlingTeam'] = np.where(Team1_mask, d['Team2'], d['Team1'])

d.columns

final_df = d[['BattingTeam', 'BowlingTeam', 'City', 'runs_left', 'balls_left', 'wicket', 'total_run_x', 'crr', 'rrr', 'result']]

final_df

teams = [
    'Chennai Super Kings',
    'Sunrisers Hyderabad',
    'Mumbai Indians',
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Punjab Kings',
    'Rajasthan Royals',
    'Delhi Capitals',
    'Gujarat Titans',
    'Lucknow Super Giants'
]

final_df.replace('Gujarat Lions', 'Gujarat Titans', inplace=True)
final_df.replace('Delhi Daredevils', 'Delhi Capitals', inplace=True)
final_df.replace('Pune Warriors ', 'Lucknow Super Giants', inplace=True)
final_df.replace('Deccan Chargers', 'Sunrisers Hyderabad', inplace=True)
final_df.replace('Rising Pune Supergiant', 'Lucknow Super Giants', inplace=True)
final_df.replace('Kings XI Punjab', 'Punjab Kings', inplace=True)

final_df = final_df[final_df['BattingTeam'].isin(teams)]
final_df = final_df[final_df['BowlingTeam'].isin(teams)]

final_df['BattingTeam'].unique()

final_df.sample()

final_df.dropna(inplace=True)

final_df.shape

final_df = final_df[final_df['balls_left'] != 0]

final_df.replace('Bengaluru', ' Bangalore', inplace=True)
final_df.replace('Navi Mumbai', 'Mumbai', inplace=True)
final_df.replace('Rajkot', 'Ahmedabad', inplace=True)
final_df.replace('Kanpur', 'Lucknow', inplace=True)
final_df.replace('Pune', 'Lucknow', inplace=True)
final_df.replace('Chandigarh', 'Mohali', inplace=True)
final_df.replace('Dharamsala', 'Mohali', inplace=True)

cities = ['Ahmedabad', 'Kolkata', 'Mumbai', 'Lucknow', 'Delhi', 'Chennai', 'Hyderabad',
        'Mohali', 'Jaipur', 'Bangalore']

final_df = final_df[final_df['City'].isin(cities)]

final_df.shape

final_df = final_df[final_df['balls_left'] != 0]

X = final_df.iloc[:,:-1]
y = final_df.iloc[:,-1]
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=1)

X_train

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

trf = ColumnTransformer([
    ('trf',OneHotEncoder(sparse=False,drop='first'),['BattingTeam','BowlingTeam','City'])
]
,remainder='passthrough')

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

pipe = Pipeline(steps=[
    ('step1',trf),
    ('step2',LogisticRegression(solver='liblinear'))
])


pipe.fit(X_train,y_train)

y_pred = pipe.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

pipe.predict_proba(X_test)[120]

import pickle
pickle.dump(pipe, open('p2.pkl','wb'))

from google.colab import files
files.download('p2.pkl')

final_df['City'].unique()

