import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
import numpy as np

df = pd.read_csv('csvs/player_stats.csv')
years = list(range(1991, 2021))
del df['Unnamed: 0']

predictors = ['age', 'g', 'gs', 'mp', 'fg', 'fga', 'fg%', '3p',
       '3pa', '3p%', '2p', '2pa', '2p%', 'efg%', 'ft', 'fta', 'ft%', 'orb',
       'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'year', 'w', 'l', 'w/l%', 'gb', 'ps/g',
       'pa/g', 'srs']

df['gb'] = pd.to_numeric(df['gb'].replace('—', 0))

train = df[df['year'] < 2020]
test = df[df['year'] == 2020]

rdg = Ridge(alpha=0.1)
rdg.fit(train[predictors], train['share'])

predictions = rdg.predict(test[predictors])

predictions = pd.DataFrame(predictions, columns=['predictions'], index=test.index)

combination = pd.concat([test[['player', 'share', 'year']], predictions], axis=1)
combination = combination.sort_values('share', ascending=False)
combination['rk'] = list(range(1, len(combination) + 1))

combination = combination.sort_values('predictions', ascending=False)
combination['predicted_rk'] = list(range(1, len(combination) + 1))


def find_ap(df):
    actual = combination.sort_values('share', ascending=False).head(5)
    predicted = combination.sort_values('predictions', ascending=False)
    ps = []
    found = 0
    seen = 1
    
    for index, row in predicted.iterrows():
        if row['player'] in actual['player'].values:
            found += 1
            ps.append(found/seen)
        seen += 1
    return sum(ps) / len(ps)

def add_rank(combination):
    combination = combination.sort_values('predictions', ascending=False)
    combination['predicted_rk'] = list(range(1, len(combination) + 1))
    combination = combination.sort_values('share', ascending=False)
    combination['rk'] = list(range(1, len(combination) + 1))
    combination['diff'] = combination['rk'] - combination['predicted_rk']
    return combination

def backtest(df, model, year, predictors):
    aps = []
    all_predictions = []

    for year in years[5:]:
        train = df[df['year'] < year ]
        test = df[df['year'] == year]
        model.fit(train[predictors], train['share'])
        y_pred = model.predict(test[predictors])
        y_pred = pd.DataFrame(y_pred, columns=['predictions'], index=test.index)
        new_df = pd.concat([test[['player', 'share']], y_pred], axis=1)
        new_df = add_rank(new_df)
        all_predictions.append(new_df)
        aps.append(find_ap(new_df))
        
    return sum(aps)/len(aps)

aps = backtest(df, rdg, years[5:], predictors)
print(aps)