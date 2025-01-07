from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
class Team(models.Model):
    """A team in the current UCL Competition"""
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        """Return a string representation of the model"""
        return self.name
    
class HistoryTotalPerformance(models.Model):
    """A model for past UCL performances that tracks aggregate performance metrics"""
    rank = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    matches = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    
    # goals_scored = models.IntegerField(default=0)
    # goals_conceded = models.IntegerField(default=0)
    # points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.rank}, {self.team} - {self.matches} Matches, ({self.wins} Wins, {self.draws} Draws, {self.loses} Losses)" 
class HistoryFinals(models.Model):
    """A model for 1955-2023 UCL Finals that tracks the finalists and the results of each final"""
    season = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    match_venue = models.CharField(max_length=100)
    match_notes = models.TextField(blank=True, default="")
    result = models.CharField(max_length=10, blank=True, default="")
    
    def __str__(self):
        return f"{self.season}: {self.team} - {self.result} ({self.goals_for}-{self.goals_against})"
    
    
    
