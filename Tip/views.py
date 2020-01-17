from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from users.models import User
from .models import Match, Team, Tip
from django.http import Http404, HttpResponseRedirect
import re
from django.utils import timezone
from django.contrib import messages


def home(request):
    context = {
        'tip': Tip.objects.all(),
        'match': Match.objects.all(),
        'team': Team.objects.all(),
    }
    return render(request, 'tip/home.html', context)  # make tip accessible for request
    # HttpResponse('<h1> Tip Home</h1>')


@login_required
@csrf_protect
def matchday(request, matchday_number):
    m_nr: int = int(matchday_number)
    number_joker = 0  # checke anzahl an jokern
    if m_nr < 1 or m_nr > 7:
        # testing
        if m_nr != 0:
            raise Http404
    if request.method == 'POST':
        for k, v in request.POST.items():  # k id zu tipp post, v tipps
            # print(request.POST.items())
            print('k:', k)
            print('v:', v)
            if k.startswith('Tipp-'):
                try:
                    match_id = int(k.strip('Tipp-'))  # Tipp id started mit "Tipp-" + id
                    # print(match_id)
                except:
                    raise Http404
                # get input in {tipp : tipp} format
                m = re.match(r'^(?P<home_score>\d+):(?P<guest_score>\d+)', v)
                match = get_object_or_404(Match, pk=match_id)
                if m:
                    # match = get_object_or_404(Match, pk=match_id)
                    if not match.has_started():
                        try:
                            tipp = Tip.objects.get(author=request.user, match__id=match_id)
                        except:
                            tipp = None
                        home_score = m.group('home_score')  # string in v vor :
                        guest_score = m.group('guest_score')  # string in v nach :
                        if tipp:
                            # fülle model falls tipp schon vorhanden
                            tipp.date_posted = timezone.now
                            tipp.tip_home = home_score
                            tipp.tip_guest = guest_score
                            # falls tipp nicht vorhanden erstelle neuen
                        else:
                            tipp = Tip(
                                author=User.objects.get(pk=request.user.pk),
                                match=match,
                                tip_date=timezone.now(),
                                tip_home=home_score,
                                tip_guest=guest_score,
                            )
                        tipp.save()
                # falls tipp schon vorhanden aber joker wird rausgenommen, dann ist k leer und joker als 0 gespeichert.
                try:
                    tipp = Tip.objects.get(author=request.user, match__id=match_id)
                except:
                    tipp = None
                if tipp:
                    tipp.joker = 0
                    tipp.save()
            elif k.startswith('Joker-'):
                try:
                    match_id = int(k.strip('Joker-'))
                except:
                    raise Http404
                match = get_object_or_404(Match, pk=match_id)
                if not match.has_started():
                    # tipp muss existieren sonst fehler
                    try:
                        tipp = Tip.objects.get(author=request.user, match__id=match_id)
                    except:
                        tipp = None
                    number_joker += 1
                    # zu viele joker?
                    if joker_valid(m_nr, number_joker) == 1 and tipp:
                        tipp.joker = 1
                        tipp.save()
                    elif not joker_valid(m_nr, number_joker):
                        messages.warning(request, 'Zu viele Joker gesetzt! Anzahl Joker: %s' %number_joker)
        messages.success(request, 'Gespeichert!')
        return HttpResponseRedirect(reverse('tip-matchday', kwargs={'matchday_number': m_nr}))

    match = Match.objects.filter(matchday=m_nr)
    tipps = Tip.objects.filter(author=request.user).filter(match__matchday=m_nr)
    tipps_by_matches = {t.match.pk: t for t in tipps}
    context = {
        'number': m_nr,
        'match': match,
        'tipps': tipps_by_matches,
    }
    return render(request, 'tip/matchday.html', context)


def about(request):
    return render(request, 'tip/about.html', {'title': 'about'})  # add title by hand


def joker_valid(matchday_in, n_joker):
    """

    :param matchday_in: matchday da anzahl joker sich hier unterscheidet
    :param n_joker: anzahl joker
    :return: sind zu viele joker gesetzt? erstmal nur vorrunde
    """
    if matchday_in < 3 and n_joker > 3:
        return 0
    return 1
