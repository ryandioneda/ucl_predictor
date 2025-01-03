from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.util.csv.csv_parsers import *
from api.models import HistoryTotalPerformance, HistoryFinals, Team

import os
import sys
import pandas as pd

UCL_Finals_1955_2023_csv = os.path.join(settings.BASE_DIR, 'api', 'data', 'UCL_Finals_1955-2023.csv')
UCL_AllTime_Performance_csv = os.path.join(settings.BASE_DIR, 'api', 'data', 'UCL_AllTime_Performance_Table.csv')



class Command(BaseCommand):
    
    def handle(self, *args, **options):
        
        ucl_history_finals_dataframe = pd.read_csv(UCL_Finals_1955_2023_csv, usecols=[
            "Season", "Country", "Winners", "Score", "Runners-up", "Country.1", "Venue", "Notes"
        ])
        ucl_history_finals_dataframe.rename(columns={
            "Country": 'Winner-Country',
            "Country.1": 'Runners-up-Country'
        }, inplace=True)
        
        parsed_ucl_history_finals_dataframe = parse_UCL_history_finals_data(ucl_history_finals_dataframe)
        
        if not parsed_ucl_history_finals_dataframe.empty:
            for row in parsed_ucl_history_finals_dataframe.itertuples(index=False):
                team, created = Team.objects.get_or_create(name=row.Team)
                
                team.country = row.Country
                team.save()
                HistoryFinals.objects.create(
                    season=row.Season,
                    team=team,
                    goals_for=row.Goals_For,
                    goals_against=row.Goals_Against,
                    match_venue=row.Match_Venue,
                    match_notes=row.Match_Notes,
                    result=row.Result
                )
            print("Sucessfully imported UCL finals parsed data")
        else:
            print("Failed to import UCL finals data")
            
            
            
        ucl_history_performance_dataframe = pd.read_csv(UCL_AllTime_Performance_csv, usecols=[
            "#", "Team", "M.", "W", "D", "L", 
        ])
        ucl_history_performance_dataframe.rename(columns={
            "#": "Rank",
            "M.": "Matches",
            "W": "Wins",
            "D": "Draws",
            "L": "Losses"
        }, inplace=True)
        
        parsed_ucl_history_performance_dataframe = parse_UCL_history_performance_data(ucl_history_performance_dataframe)
        
        if not parsed_ucl_history_performance_dataframe.empty:
            for row in parsed_ucl_history_performance_dataframe.itertuples(index=False):
                team, created = Team.objects.get_or_create(name=row.Team)
                HistoryTotalPerformance.objects.create(
                    rank=row.Rank,
                    team=team,
                    matches=row.Matches,
                    wins=row.Wins,
                    draws=row.Draws,
                    losses=row.Losses,
                )
            print("Successfully imported UCL all time performance parsed data")
        else:
            print("Failed to import UCL all time performance data")
                