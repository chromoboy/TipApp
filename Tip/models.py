from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

TEST_CHOICES = [
    ('GER', 'Deutschland'),
    ('ESP', 'Spanien'),
    ('ENG', 'England'),
]


class Champion(models.Model):
    champion = models.CharField(max_length=100)


class Team(models.Model):
    team_name = models.CharField(max_length=100)
    team_ccode = models.CharField(max_length=3)
    win_points = models.IntegerField(default=10)

    def __str__(self):
        return self.team_name


class Match(models.Model):
    # one team has many matches
    home_team = models.ForeignKey(Team, related_name="home_team", on_delete=models.CASCADE, default="tba")
    guest_team = models.ForeignKey(Team, related_name="guest_team", on_delete=models.CASCADE, default="tba")
    match_date = models.DateTimeField(default=timezone.now)
    matchday = models.IntegerField(default=0)
    guest_score = models.IntegerField(default=-1)
    home_score = models.IntegerField(default=-1)

    def has_started(self):
        return self.match_date <= timezone.now() - timedelta(seconds=60)

    def has_finished(self):
        return timezone.now() >= self.match_date + timedelta(minutes=720)


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
        if -1 in [sh, sg, th, tg]:
            return 0
        sgn = lambda x: 0 if x == 0 else x / abs(x)
        points = 0
        ds = sh - sg
        dt = th - tg

        if sgn(ds) == sgn(dt):
            # correct tendency
            points += 1
            if ds == dt:
                # correct difference
                points += 1
                if sh == th:
                    # correct result
                    points += 1
        if self.joker:
            points *= self.joker_multiplier()
        return points

    def joker_multiplier(self):
        """
        :return: gibt joker faktor zurück. Vergabe Richtig?
        """
        if self.match.matchday < 3:
            return 2
        if self.match.matchday < 5:
            return 3
        if self.match.matchday < 7:
            return 4
        return 1
    # joker immer mal 2


# TODO: Joker müssen noch eingesetzt werden. Wie wird die Anzahl an Jokern angegeben?
# --> über funktion in user modell mit x = int(x == 'true') und matchday angabe, also n_joker = 3 für matchday 1,2,3
# TODO: Wie werden überhaupt ergebnisse eingetragen? --> admin page
# TODO: Weltmeister wird über dict mit tipps verglichen.
# TODO: Vllt doch Weltmeister als Dropdown über Foreign Key auf Teams?
