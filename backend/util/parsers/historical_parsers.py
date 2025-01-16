import pandas as pd

def parse_ucl_history_finals_df(dataframe):
    """
    Parses the UCL history finals dataframe (data from UCL_finals_1955-2023.csv)

    Args:
        dataframe: A pandas dataframe

    Returns:
        pd.DataFrame: A parsed dataframe
    """
    required_columns = ['Season', 'Winner_country', 'Winners', 'Score', 'Runners_up', 'Runners_up_country', 'Venue', 'Notes']
    missing_columns = []

    for col in required_columns:
        if col not in dataframe.columns:
            missing_columns.append(col)

    if missing_columns:
        raise KeyError(f"There are missing columns in the dataframe: {missing_columns}")
    
    dataframe['Notes'] = dataframe['Notes'].fillna("No notes")

    split_score = dataframe['Score'].str.split('–', expand=True)
    
    dataframe['Winners_goals'] = pd.to_numeric(split_score[0]).fillna(0).astype(int)
    dataframe["Runners_up_goals"] = pd.to_numeric(split_score[1]).fillna(0).astype(int)

    winners_df = dataframe[['Season', 'Winners', 'Winner_country', 'Runners_up_goals', 'Winners_goals', 'Venue', 'Notes']].copy()
    winners_df.rename(columns={
        'Winners': 'Team',
        'Winner_country': 'Country',
        'Winners_goals': 'Goals_for',
        'Runners_up_goals': 'Goals_against',
        'Venue': 'Match_venue',
        'Notes': 'Match_notes',
    }, inplace=True)

    winners_df['Result'] = 'Win'

    runners_up_df = dataframe[['Season', 'Runners_up', 'Runners_up_country', 'Runners_up_goals', 'Winners_goals', 'Venue', 'Notes']].copy()
    runners_up_df.rename(columns={
        'Runners_up': 'Team',
        'Runners_up_country': 'Country',
        'Runners_up_goals': 'Goals_for',
        'Winners_goals': 'Goals_against',
        'Venue': 'Match_venue',
        'Notes': 'Match_notes',
    }, inplace=True)

    runners_up_df['Result'] = "Loss"

    combined_df = pd.concat([winners_df, runners_up_df], ignore_index=True)
    combined_df = combined_df.sort_values(by=['Season', 'Result'], ascending=[True, False]).reset_index(drop=True)

    return combined_df

def parse_ucl_all_time_performance_df(dataframe):
    """
    Parse the UCL all time performance dataframe (data from UCL_AllTime_Performance_Table.csv)

    Args:
        dataframe: A pandas dataframe

    Returns:
        pd.Dataframe: A parsed dataframe
    """
    dataframe['Rank'] = dataframe['Rank'].ffill().astype(int)
    required_columns = ['Rank', 'Matches', 'Wins', 'Draws', 'Losses']
    missing_columns = []

    for col in required_columns:
        if col not in dataframe.columns:
            missing_columns.append(col)

    if missing_columns:
        raise KeyError(f"There are missing columns in the dataframe: {missing_columns}")
    print("hello") 
    return dataframe






 