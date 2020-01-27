from django.utils import timezone
from . import views
from django.urls import path
from .models import Team, Match, Tip
from users.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView

urlpatterns = [
    path('', views.home, name='tip-home'),
    path('about/', views.about, name='tip-about'),
    path('matchday/<int:matchday_number>/', views.matchday, name='tip-matchday'),
    # gebe für rangliste queryset zurück, dass spieler nach punkten sortiert und als users zurückgibt
    path('ranking/', login_required(ListView.as_view(queryset=Profile.objects.order_by('-score', 'user__username'),
                                                     context_object_name='users', template_name='Tip/ranking.html')),
         name="tip-ranking"
         ),
    path('settings/<int:matchday_number>/', views.settings, name='tip-settings'),
    path('update_score_and_ranks/', views.update_scores_and_ranks, name='tip-settings-update'),
    ]


