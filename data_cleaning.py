import pandas as pd

mvps = pd.read_csv('csvs/mvps.csv')


def read_mvp_csv(mvps):


    mvps = pd.read_csv('csvs/mvps.csv')
    
    mvps.columns = mvps.columns.str.replace(' ', '_').str.lower()

    mvps = mvps[["player", "year", "pts_won", "pts_max", "share"]]
    
    mvps['player'] = [i.lower() for i in mvps.player ]
        
    return mvps

mvp = read_mvp_csv(mvps)
# print(mvp)

players_df = pd.read_csv('csvs/players.csv')


def read_player_csv(players):

    players.columns = players.columns.str.lower().str.replace(' ', '_')
    players['player'] = players.player.str.replace('*', '', regex=False)

    
    strings = ['player', 'tm']
    for col in strings:
        players[col] = players[col].str.lower()
        
    del players['unnamed:_0']
    del players['rk']
    
    return players

def single_row(df):
    if df.shape[0] == 1:
        return df
    else:
        row = df[df['tm'] == 'tot']
        row['tm'] = df.iloc[-1, :]['tm']

    return row
    
players = read_player_csv(players_df)
players = players.groupby(['player', 'year']).apply(single_row)

players.index = players.index.droplevel()
players.index = players.index.droplevel()


mvp_players = players.merge(mvp, how='outer', on=['player', 'year'])
mvp_players[['pts_won', 'pts_max', 'share']] = mvp_players[['pts_won', 'pts_max', 'share']].fillna(0)


# TEAMS
teams_df = pd.read_csv('csvs/teams.csv')

def read_team_csv(teams):
    teams.columns = teams.columns.str.lower().str.replace(' ', '')
    teams.team = [i for i in teams['team'].str.lower()]    
    del teams['unnamed:0']
    teams = teams[~teams['w'].str.contains('Division')]
    teams['team'] = teams['team'].str.replace('*', '', regex=False)
    return teams

nicknames = {}

with open("nicknames.txt", 'r') as f_in:
    lines = f_in.readlines()
    for line in lines[1:]:
        abbrev, name = line.replace('\n', '').replace('-', '').replace("'", '"').replace('\t', ':').split(':')
        nicknames[abbrev] = name
        for key, val in nicknames.items():
            names = key.strip()
            nicknames[names] = val.strip().replace('"', '').lower()

# teams = read_team_csv(teams_df)
print(nicknames)
