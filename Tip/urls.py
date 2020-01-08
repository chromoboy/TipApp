from . import views
from django.urls import path
from .models import Team, Match, Tip

urlpatterns = [
    path('', views.home, name='tip-home'),
    path('about/', views.about, name='tip-about'),
    path('matchday/<int:matchday_number>/', views.matchday, name='tip-matchday')
]
