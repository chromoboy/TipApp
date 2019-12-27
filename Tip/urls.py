from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='tip-home'),
    path('about/', views.about, name='tip-about'),

]
