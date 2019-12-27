from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Group(models.Model):
    group_name = models.CharField(max_length=1, default="", editable=False)


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_ccode = models.CharField(max_length=3)
    team_rank = models.IntegerField(default=1)
    # one group has many teams
    team_group = models.ForeignKey(Group, default="", on_delete=models.PROTECT)

    # date_posted = models.DateTimeField(default=timezone.now)
    # date when team is created saved for later use

    def __str__(self):
        return self.team_name


class Match(models.Model):
    # one team has many matches
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.PROTECT)
    guest_team = models.ForeignKey(Team, related_name="guest_team", on_delete=models.PROTECT)
    match_time = models.DateTimeField(default=timezone.now)
    match_type = models.IntegerField(default=1)


class Tip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    tip = models.CharField(max_length=10)
    date_posted = models.DateTimeField(default=timezone.now)

# TODO: add User with Points entity which is calculated by external method given the tip and result of a tip
# TODO: add Champion and possibility to decide if tip was submit before game has started.
