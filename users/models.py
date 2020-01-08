from django.db import models
from django.contrib.auth.models import User
from Tip.models import Team, Tip
from PIL import Image
from Tip.models import TEST_CHOICES


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    champion = models.CharField(max_length=12, choices=TEST_CHOICES, default='spanien')

    def update_score(self):
        tipps = Tip.objects.filter(user=self)
        score = 0
        for tipp in tipps:
            score += tipp.points()
        self.score = score

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
