import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from backend.util.parsers.historical_parsers import parse_ucl_history_finals_df, parse_ucl_all_time_performance_df
pd.set_option('display.max_rows', None)

ucl_finals_1955_2023_df = pd.read_csv(
    'backend/data/historical/UCL_Finals_1955-2023.csv',
    usecols=["Season", "Country", "Winners", "Score", "Runners-up", "Country.1", "Venue", "Notes"]
)

ucl_finals_1955_2023_df.rename(columns={
    "Runners-up": "Runners_up",
    "Country": "Winner_country",
    "Country.1": "Runners_up_country"
}, inplace=True)

parsed_ucl_finals_1955_2023_df = parse_ucl_history_finals_df(ucl_finals_1955_2023_df) 

ucl_all_time_performance_df = pd.read_csv(
    'backend/data/historical/UCL_AllTime_Performance_Table.csv',
    usecols=["#", "Team", "M.", "W", "D", "L"]
)



ucl_all_time_performance_df.rename(columns={
    "#": "Rank",
    "M.": "Matches",
    "W": "Wins",
    "D": "Draws",
    "L": "Losses"
}, inplace=True)

parsed_ucl_all_time_performance_df = parse_ucl_all_time_performance_df(ucl_all_time_performance_df)

# combine all teams into a pandas series to iterate
all_teams = pd.concat([
    parsed_ucl_all_time_performance_df['Team'],
    parsed_ucl_finals_1955_2023_df['Team']
]).drop_duplicates()

team_code_map = {}

for index, team in enumerate(all_teams):
    team_code_map[team] = index
    
parsed_ucl_all_time_performance_df['Team_code'] = parsed_ucl_all_time_performance_df['Team'].map(team_code_map)
parsed_ucl_finals_1955_2023_df['Team_code'] = parsed_ucl_finals_1955_2023_df['Team'].map(team_code_map)

parsed_ucl_all_time_performance_df["Win_rate"] = parsed_ucl_all_time_performance_df['Wins'] / parsed_ucl_all_time_performance_df['Matches']
parsed_ucl_all_time_performance_df["Draw_rate"] = parsed_ucl_all_time_performance_df['Draws'] / parsed_ucl_all_time_performance_df['Matches']
parsed_ucl_all_time_performance_df["Loss_rate"] = parsed_ucl_all_time_performance_df['Losses'] / parsed_ucl_all_time_performance_df['Matches']

matches_min = parsed_ucl_all_time_performance_df['Matches'].min()
matches_max = parsed_ucl_all_time_performance_df['Matches'].max()

parsed_ucl_all_time_performance_df['Weighted_match_experience'] = (
    (parsed_ucl_all_time_performance_df['Matches'] - matches_min) / (matches_max - matches_min)
) * parsed_ucl_all_time_performance_df['Win_rate']



# parsed_ucl_all_time_performance_df.drop(['Rank', 'Team', 'Matches', 'Wins', 'Draws', 'Losses'], axis=1, inplace=True)
# print(parsed_ucl_all_time_performance_df)

#! Elbow method plotting to find k
# inertia_values = []
# k_range = range(1, 11)
# for k in k_range:
#     kmeans = KMeans(n_clusters=k, random_state=42)
#     kmeans.fit(parsed_ucl_all_time_performance_df)
#     inertia_values.append(kmeans.inertia_)

# plt.plot(k_range, inertia_values, marker='o')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Inertia')
# plt.title('Elbow Method for Optimal k')
# plt.savefig('elbow_method_plot.png')


cluster_features = parsed_ucl_all_time_performance_df[['Win_rate', 'Draw_rate', 'Loss_rate', 'Weighted_match_experience']]

scaler = StandardScaler()
x_scaled = scaler.fit_transform(cluster_features)


kmeans = KMeans(n_clusters=3, random_state=42)
parsed_ucl_all_time_performance_df['Cluster_group'] = kmeans.fit_predict(x_scaled)
print(parsed_ucl_all_time_performance_df)
