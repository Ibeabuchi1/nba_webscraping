import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import numpy as np

df = pd.read_csv('csvs/player_stats.csv')

del df['Unnamed: 0']

predictors = ['age', 'g', 'gs', 'mp', 'fg', 'fga', 'fg%', '3p',
       '3pa', '3p%', '2p', '2pa', '2p%', 'efg%', 'ft', 'fta', 'ft%', 'orb',
       'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'year', 'w', 'l', 'w/l%', 'gb', 'ps/g',
       'pa/g', 'srs']

print(df.columns)