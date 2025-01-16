import pandas as pd
from backend.util.parsers.historical_parsers import parse_ucl_history_finals_df, parse_ucl_all_time_performance_df


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


parsed_ucl_all_time_performance_df["Win_rate"] = parsed_ucl_all_time_performance_df['Wins'] / parsed_ucl_all_time_performance_df['Matches']
parsed_ucl_all_time_performance_df["Draw_rate"] = parsed_ucl_all_time_performance_df['Draws'] / parsed_ucl_all_time_performance_df['Matches']
parsed_ucl_all_time_performance_df["Loss_rate"] = parsed_ucl_all_time_performance_df['Losses'] / parsed_ucl_all_time_performance_df['Matches']


print(parsed_ucl_all_time_performance_df)


