from django.db import models
from django.contrib.auth.models import User
from Tip.models import Team, Tip, Match, Champion
from PIL import Image

champion_choices = [(team.team_ccode, team.team_name) for team in Team.objects.all()]
champion_choices.append([('----'), ('----')])
champion_choices = [(('----'), ('----'))]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    # champion = models.ForeignKey(Champion, on_delete=models.CASCADE)
    user_champion = models.CharField(max_length=12, choices=champion_choices, default='----')
    joker = models.IntegerField(default=0)

    # überschreibe joker und tipps
    def update_score_and_joker(self):

        tipps = Tip.objects.filter(author=self.user_id)
        score = 0
        joker = 0
        for tipp in tipps:
            score += tipp.points()
            if tipp.joker:
                joker += 1
        self.joker = joker
        self.score = score

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
