import pandas as pd

mvps = pd.read_csv('csvs/mvps.csv')
players_df = pd.read_csv('csvs/players.csv')
teams_df = pd.read_csv('csvs/teams.csv')


def read_mvp_csv(mvps):
    mvps = pd.read_csv('csvs/mvps.csv')
    mvps.columns = mvps.columns.str.replace(' ', '_').str.lower()
    mvps = mvps[["player", "year", "pts_won", "pts_max", "share"]]
    mvps['player'] = [i.lower() for i in mvps.player ] 
    return mvps

mvp = read_mvp_csv(mvps)
# print(mvp)


def read_player_csv(players):

    players.columns = players.columns.str.lower().str.replace(' ', '_')
    players['player'] = players.player.str.replace('*', '', regex=False)
    
    strings = ['player', 'tm']
    for col in strings:
        players[col] = players[col].str.lower()
        
    del players['unnamed:_0']
    del players['rk']
    
    def single_row(df):
        if df.shape[0] == 1:
            return df
        else:
            row = df[df['tm'] == 'tot']
            row['tm'] = df.iloc[-1, :]['tm']
            return row
    players = players.groupby(['player', 'year']).apply(single_row) 
    players.index = players.index.droplevel()
    players.index = players.index.droplevel()
    return players

    
players = read_player_csv(players_df)

mvp_players = players.merge(mvp, how='outer', on=['player', 'year'])
mvp_players[['pts_won', 'pts_max', 'share']] = mvp_players[['pts_won', 'pts_max', 'share']].fillna(0)


# TEAMS

def read_team_csv(teams):
    teams = teams.copy()

    teams.columns = teams.columns.str.lower().str.replace(' ', '')
    teams.team = [i for i in teams['team'].str.lower()]    
    del teams['unnamed:0']
    teams = teams[~teams['w'].str.contains('Division')]
    teams.team = teams['team'].str.replace('*', '', regex=False)
    return teams

nicknames = {}

with open("nicknames.txt", 'r') as f_in:
    lines = f_in.readlines()
    for line in lines[1:]:
        abbrev, name = line.replace('\n', '').replace('-', '').replace("'", '"').replace('\t', ':').split(':')
        nicknames[abbrev] = name
        for key, val in nicknames.copy().items():
            if val.upper():
                del nicknames[key]
                key = key.strip().lower()
                val = val.strip().replace('"', '').lower()
                nicknames[key] = val

mvp_players['team'] = mvp_players['tm'].map(nicknames)
mvp_players[['pts_won', 'pts_max', 'share']] = mvp_players[['pts_won', 'pts_max', 'share']].fillna(0)


teams = read_team_csv(teams_df)
stat = mvp_players.merge(teams, how='outer', on=['team', 'year'])
# stat = stat.dropna()

stat.to_csv('csvs/player_stats.csv')
# 