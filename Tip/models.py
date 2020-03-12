from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_ccode = models.CharField(max_length=3)
    win_points = models.IntegerField(default=10)

    def __str__(self):
        return self.team_name


class Match(models.Model):
    # one team has many matches
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.CASCADE, default=0)
    guest_team = models.ForeignKey(Team, related_name="guest_team", on_delete=models.CASCADE, default=0)
    match_date = models.DateTimeField(default=timezone.now)
    matchday = models.IntegerField(default=0)
    guest_score = models.IntegerField(default=-1)
    home_score = models.IntegerField(default=-1)

    def has_started(self):
        return self.match_date <= timezone.now() - timedelta(seconds=60)

    # def has_finished(self):
    #     return timezone.now() >= self.match_date + timedelta(minutes=150)


class Tip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.PROTECT)
    tip_date = models.DateTimeField(default=timezone.now)
    tip_home = models.IntegerField(default=-1)
    tip_guest = models.IntegerField(default=-1)
    joker = models.BooleanField(default=0)

    def points(self):
        sh = self.match.home_score
        sg = self.match.guest_score
        th = self.tip_home
        tg = self.tip_guest
        # no tip
        if -1 in [sh, sg, th, tg]:
            return 0
        sgn = lambda x: 0 if x == 0 else x / abs(x)
        points = 0
        ds = sh - sg
        dt = th - tg
        if sh == th or sg == tg:
            points += 1
            print("===========================")
            print("ein ergbniss richtig")
            print("points", points)
        if sgn(ds) == sgn(dt):
            print("tendenz richtig:")
            print(sh,sg,th,tg, ds, dt )
            print(sgn(ds))
            print(sgn(dt))
            # correct tendency
            points += 3
        if ds == dt:
            # correct difference
            points += 1
        if sh == th and tg == sg:
            # correct result
            points += 1
        if self.joker:
            points *= 2
        return points


class Champion(models.Model):
    champion = models.ForeignKey(Team, max_length=100, on_delete=models.CASCADE)
    points = models.IntegerField(default=30)
    eliminated = models.BooleanField(default=0)

    # print(champion_choices)
    # def champion_list(self):
    #     champion_choices = [(team.team_ccode, team.team_name) for team in Team.objects.all()]
    #     champion_choices.append([('---'), ('---')])
    #     return champion_choices

    def __str__(self):
        return self.champion.team_name

#TODO: punkte von europameister anrechnen.
