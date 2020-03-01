from django.utils import timezone
from . import views
from django.urls import path
from .models import Team, Match, Tip, Champion
from users.models import User, Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView, TemplateView

# print(Champion.champion.team_ccode)

urlpatterns = [
    path('', views.home, name='tip-home'),
    # path('about/', views.about, name='tip-about'),
    path('tipps/<int:matchday_number>/', views.matchday, name='tip-matchday'),
    path('all_matches/', views.all_matches, name='tip-all-matches'),
    # gebe für rangliste queryset zurück, dass spieler nach punkten sortiert und als users zurückgibt
    path('ranking/', login_required(ListView.as_view(queryset=Profile.objects.order_by('-score', 'user__username', 'joker'),
                                                     context_object_name='users', template_name='tip/ranking.html')),
         name="tip-ranking"
         ),
    path('ergebnisse/<int:matchday_number>/', views.ergebnisse, name='tip-settings'),
    # path('update_score_and_ranks/', views.update_scores_and_ranks, name='tip-settings-update'),
    path('champion/', views.champion, name='tip-champion'),
    path('email/', views.email, name='tip-mail'),
    ]

