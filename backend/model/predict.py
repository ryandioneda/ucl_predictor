import pandas as pd

from backend.util.parsers.historical_parsers import parse_ucl_2016_2022_matches_df

ucl_2016_2022_teams_df = pd.read_csv(
    'backend/data/historical/UEFA Champions League 2016-2022 Teams.csv',
    usecols=['TEAM_NAME', 'COUNTRY', 'HOME_STADIUM']
)

teams_dict = {}

for index, row in ucl_2016_2022_teams_df.iterrows():
    teams_dict[row['TEAM_NAME']] = {
        'team_code': index,
        'country': row['COUNTRY'],
        'home_stadium': row['HOME_STADIUM']
    }

#print(teams_dict['AC Milan']['team_code'])

ucl_2016_2022_matches_df = pd.read_csv(
    'backend/data/historical/UEFA Champions League 2016-2022 Matches.csv',
    usecols=['SEASON', 'DATE_TIME', 'HOME_TEAM', 'AWAY_TEAM', 'STADIUM', 'HOME_TEAM_SCORE', 'AWAY_TEAM_SCORE']
)

parsed_matches_df = parse_ucl_2016_2022_matches_df(ucl_2016_2022_matches_df)

parsed_matches_df['team'] = parsed_matches_df['team'].map(lambda team: teams_dict[team]['team_code'])
parsed_matches_df['opponent'] = parsed_matches_df['opponent'].map(lambda opponent: teams_dict[opponent]['team_code'])


print(parsed_matches_df)
