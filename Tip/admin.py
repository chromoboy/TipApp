from django.contrib import admin
from .models import Tip
from .models import Match
from .models import Team
from .models import Champion

admin.site.register(Tip)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(Champion)

