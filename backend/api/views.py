from django.shortcuts import render
from .models import Team, HistoryTotalPerformance, HistoryFinals
from rest_framework import viewsets
from .serializers import TeamSerializer, HistoryTotalPerformanceSerializer, HistoryFinalsSerializer

# Create your views here.
class TeamsViewSet(viewsets.ModelViewSet):
    # API endpoint to view list of all teams or a single team
    serializer_class = TeamSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        
        if pk:
            return Team.objects.filter(pk=pk)
        else:
            return Team.objects.all()
    
    
class HistoryTotalPerformanceViewSet(viewsets.ModelViewSet):
    # API endpoint to view list of all all-time performances or a single team's all-time performances
    serializer_class = HistoryTotalPerformanceSerializer
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        
        if team_id:
            return HistoryTotalPerformance.objects.filter(team_id=team_id)
        else:
            return HistoryTotalPerformance.objects.all()


class HistoryFinalsViewSet(viewsets.ModelViewSet):
    # API endpoint to view list of all past finals or list of a single team's finals
    serializer_class = HistoryFinalsSerializer
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        
        if team_id:
            return HistoryFinals.objects.filter(team_id=team_id)
        else:
            return HistoryFinals.objects.all()
        