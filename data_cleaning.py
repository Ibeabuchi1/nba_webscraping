import pandas as pd

mvps = pd.read_csv('csvs/mvps.csv')


def read_mvp_csv(mvps):


    mvps = pd.read_csv('csvs/mvps.csv')
    
    mvps.columns = mvps.columns.str.replace(' ', '_').str.lower()

    mvps = mvps[["player", "year", "pts_won", "pts_max", "share"]]
    
    mvps['player'] = [i.lower() for i in mvps.player ]
        
    return mvps

# mvp = read_nba_data(mvps)
# print(mvp)

players = pd.read_csv('csvs/players.csv')


def read_player_csv(players):

    players.columns = players.columns.str.lower().str.replace(' ', '_')
    players['player'] = players.player.str.replace('*', '', regex=False)

    
    strings = ['player', 'tm']
    for col in strings:
        players[col] = players[col].str.lower()
        
    del players['unnamed:_0']
    del players['rk']
    
    return players

# def single_row(df):
#     if df.shape[0] == 1:
#         return df
#     else:
#         row = df[df['tm'] == 'tot']
#         row['tm'] = df.iloc[-1, :]['tm']

#     return row
    

# players = players.groupby(['player', 'year']).apply(single_row)

mvp = read_player_csv(players)
print(mvp)