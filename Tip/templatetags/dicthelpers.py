from datetime import timedelta
from django.template.defaultfilters import register
from Tip.models import Match
from django.utils import timezone


@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return None


@register.filter(name='current_matchday')
def current_matchday(matchday):
    print(matchday)
    next_matchday = Match.objects.filter(match_date__gte=timezone.now() + timedelta(seconds=150 * 60))
    return next_matchday.values('matchday')
