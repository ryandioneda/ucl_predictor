import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

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

le = LabelEncoder()

# 2 = win, 1 = lose, 0 = draw
le = LabelEncoder()
parsed_matches_df['result'] = le.fit_transform(parsed_matches_df['result'])  # Ensuring the result column is encoded to 2=win, 1=lose, 0=draw

# Create target column: 1 for win (2), 0 for not win (1 or 0)
parsed_matches_df['target'] = (parsed_matches_df['result'] == 2).astype('int')

import matplotlib.pyplot as plt
from sklearn.tree import plot_tree

rf = RandomForestClassifier(n_estimators=100, min_samples_split=40, random_state=1)
train = parsed_matches_df[parsed_matches_df["SEASON"] < '2019-2020']
test = parsed_matches_df[parsed_matches_df["SEASON"] > '2019-2020']
predictors = ["team", "opponent", "is_home", "hour", "day"]
rf.fit(train[predictors], train["target"])
preds = rf.predict(test[predictors])


from sklearn.metrics import accuracy_score
acc = accuracy_score(test["target"], preds)
print(acc)
combined = pd.DataFrame(dict(actual=test["target"], prediction=preds))
pd.crosstab(index=combined["actual"], columns=combined["prediction"])

from sklearn.metrics import precision_score
precision_score(test["target"], preds)

# Visualize the first tree in the forest
plt.figure(figsize=(20,10))
plot_tree(rf.estimators_[0], filled=True, feature_names=predictors, class_names=["Lose", "Win"], rounded=True)
plt.savefig('plot.png')




