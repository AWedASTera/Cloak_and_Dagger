from django.contrib import admin
from django.urls import path
from .views import UserAgentListView, AgentCreateView, AgentDeleteView, AgentDetailView, AgentListView, AgentUpdateView, TeamAgentListView
from . import views

urlpatterns = [
    path('', AgentListView.as_view(), name='char_roster-home'),
    path('statistics/', views.statistics, name='char_roster-statistics'),
    path('json_export/', views.json_export, name='json-export'),
    path('json_import/', views.json_import, name='json-import'),
    ################################################
    path('user/<str:username>/', UserAgentListView.as_view(), name='user-agents'),
    path('team/<str:name>/', TeamAgentListView.as_view(), name='team-agents'),
    path('agent/<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agent/new/', AgentCreateView.as_view(), name='agent-create'),
    path('agent/<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('agent/<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
    path('agent/<int:id>/attack/', views.attack, name='agent-attack'),
    path('agent/<int:id>/steal/', views.steal, name='agent-steal'),
    path('agent/<int:id>/work/', views.work, name='agent-work'),
    path('agent/<int:id>/heal/', views.heal, name='agent-heal'),
    path('agent/<int:id>/cover/', views.cover, name='agent-cover'),
    path('agent/<int:id>/buy_point/', views.buy_point, name='agent-buy_point'),
    path('agent/<int:id>/travel/', views.travel, name='agent-travel')
]

