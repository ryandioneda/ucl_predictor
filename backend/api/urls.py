from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

from .views import (
    TeamsViewSet,
    HistoryTotalPerformanceViewSet,
    HistoryFinalsViewSet,

) 
api_router = DefaultRouter()

api_router.register(r'teams', views.TeamsViewSet, basename='teams')
api_router.register(r'totalperformance', views.HistoryTotalPerformanceViewSet, basename='totalperformance')
api_router.register(r'finals', views.HistoryFinalsViewSet, basename='finals')