
import pandas as pd

def parse_UCL_history_finals_data(dataframe):
    """
    Parses the UCL history finals dataframe
    
    Args:
        dataframe: A pd dataframe
        
    Returns:
        pd.DataFrame: A parsed dataframe
    """
    
    try:
        required_columns = ['Season', 'Winner-Country', 'Winners', 'Score', 'Runners-up', 'Runners-up-Country', 'Venue', 'Notes']
        missing_columns = [col for col in required_columns if col not in dataframe.columns]
        if missing_columns:
            raise KeyError(f"There are missing columns in the dataframe: {missing_columns}")
        
        dataframe['Notes'] = dataframe['Notes'].fillna("No notes")
        
        split_score = dataframe['Score'].str.split('–', expand=True)
        #create new columns
        dataframe['Winners-Goals'] = pd.to_numeric(split_score[0]).fillna(0).astype(int)
        dataframe['Runners-up-Goals'] = pd.to_numeric(split_score[1]).fillna(0).astype(int)
        
        winners_df = dataframe[['Season', 'Winners', 'Winner-Country', 'Winners-Goals', 'Runners-up-Goals', 'Venue', 'Notes']].copy()
        winners_df.rename(columns={
            "Winners": "Team",
            "Winner-Country": "Country",
            "Winners-Goals": "Goals_For",
            "Runners-up-Goals": "Goals_Against",
            "Venue": "Match_Venue",
            "Notes": "Match_Notes",
        }, inplace=True)
        winners_df['Result'] = "Win"
        
        runners_up_df = dataframe[['Season', 'Runners-up', 'Runners-up-Country', 'Runners-up-Goals', 'Winners-Goals', 'Venue', 'Notes']].copy()
        runners_up_df.rename(columns={
            "Runners-up": "Team",
            "Runners-up-Country": "Country",
            "Runners-up-Goals": "Goals_For",
            "Winners-Goals": "Goals_Against",
            "Venue": "Match_Venue",
            "Notes": "Match_Notes",
        }, inplace=True)
        runners_up_df['Result'] = "Loss"
        
        combined_df = pd.concat([winners_df, runners_up_df], ignore_index=True)
        combined_df = combined_df.sort_values(by=['Season', 'Result'], ascending=[True, False]).reset_index(drop=True)
        
        return combined_df
    except KeyError as e:
        print(f"Error: Missing a column in the dataframe. Details: {e}")
    except ValueError as e:
        print(f"Error: Invalid data in the dataframe. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return pd.DataFrame()
    
def parse_UCL_history_performance_data(dataframe):
    """
    Parses the UCL all time performance dataframe
    
    Args:
        dataframe: A pd dataframe
    
    Returns:
        pd.DataFrame: A parsed dataframe
    """
    
    try:
        
        dataframe["Rank"] = dataframe["Rank"].ffill()
        required_columns = ["Rank", "Matches", "Wins", "Draws", "Losses"]
        
        missing_columns = [col for col in required_columns if col not in dataframe.columns]
        if missing_columns:
            raise KeyError(f"There are missing columns in the dataframe: {missing_columns}")
        
        
        return dataframe
    
    except KeyError as e:
        print(f"Error: Missing a column in the dataframe. Details: {e}")
    except ValueError as e:
        print(f"Error: Invalid data in the dataframe. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")    
    return pd.DataFrame()  
        
    