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
    return dataframe

def parse_ucl_2016_2022_matches_df(dataframe):
    """
    Parse the UCL 2016-2022 matches dataframe (data from the UEFA Champions League 2016-2022 Matches.csv)

    Args:
        dataframe: A pandas dataframe
    
    Returns:
        pd.Dataframe: A parsed dataframe
    """
    required_columns = ['SEASON', 'DATE_TIME', 'HOME_TEAM', 'AWAY_TEAM', 'STADIUM', 'HOME_TEAM_SCORE', 'AWAY_TEAM_SCORE']
    missing_columns = []

    for col in required_columns:
        if col not in dataframe.columns:
            missing_columns.append(col)

    if missing_columns:
        raise KeyError(f"There are missing columns in the dataframe: {missing_columns}")
   

    dataframe["date"] = pd.to_datetime(dataframe["DATE_TIME"], format='%d-%b-%y %I.%M.%S.%f %p')
    dataframe["hour"] = dataframe["date"].dt.hour
    dataframe["day"] = dataframe["date"].dt.dayofweek

    dataframe.drop('DATE_TIME', axis=1, inplace=True)

    home_rows = (
        dataframe.assign(
            team=dataframe['HOME_TEAM'],
            opponent=dataframe['AWAY_TEAM'],
            is_home=1,
            goals_for=dataframe['HOME_TEAM_SCORE'],
            goals_against=dataframe['AWAY_TEAM_SCORE']
        )
        .assign(
            result=lambda df: df.apply(
                lambda row: (
                    "win" if row["goals_for"] > row["goals_against"] 
                    else "lose" if row["goals_for"] < row["goals_against"] 
                    else "draw"
                ),
                axis=1
            )
        )
        .drop(columns=["HOME_TEAM", "AWAY_TEAM", "HOME_TEAM_SCORE", "AWAY_TEAM_SCORE"])
    )


    away_rows = (
        dataframe.assign(
            team=dataframe['AWAY_TEAM'],
            opponent=dataframe['HOME_TEAM'],
            is_home=0,
            goals_for=dataframe['AWAY_TEAM_SCORE'],
            goals_against=dataframe['HOME_TEAM_SCORE']
        )
        .assign(
            result=lambda df: df.apply(
                lambda row: (
                    "win" if row["goals_for"] > row["goals_against"] 
                    else "lose" if row["goals_for"] < row["goals_against"] 
                    else "draw"
                ),
                axis=1
            )
        )
        .drop(columns=["HOME_TEAM", "AWAY_TEAM", "HOME_TEAM_SCORE", "AWAY_TEAM_SCORE"])
    )

    result_dataframe = pd.concat([home_rows, away_rows]).sort_index().reset_index(drop=True)
    return result_dataframe





 