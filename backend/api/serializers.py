from rest_framework import serializers
from .models import Team, HistoryTotalPerformance, HistoryFinals

class TeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        #pk to identify team in other models
        model = Team
        fields = ['pk', 'name', 'country']
        
class HistoryTotalPerformanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        #team_id is foreign key
        model = HistoryTotalPerformance
        fields = ['pk','wins', 'matches', 'rank', 'losses', 'draws', 'team_id']
        
class HistoryFinalsSerializer(serializers.ModelSerializer):
    
    class Meta:
        #team_id is foreign key
        model = HistoryFinals
        fields = ['pk', 'season', 'match_venue', 'goals_against', 'goals_for', 'match_notes', 'result', 'team_id']