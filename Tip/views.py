from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from users.models import User, Profile
from .models import Match, Team, Tip, Champion
from users.models import Profile
from django.http import Http404, HttpResponseRedirect
import re
from django.utils import timezone
from django.contrib import messages


def home(request):
    current_matchday = Match.objects.filter(match_date__gte
                                            =timezone.now()).order_by('match_date')[0].matchday
    context = {
        'tip': Tip.objects.all(),
        'match': Match.objects.all(),
        'team': Team.objects.all(),
        # 'c_mday': current_matchday,
    }
    return render(request, 'tip/home.html', context)  # make tip accessible for request
    # HttpResponse('<h1> Tip Home</h1>')


@login_required
@csrf_protect
def matchday(request, matchday_number):
    author_profile = Profile.objects.get(user=request.user)
    print('author_profil', author_profile)
    m_nr: int = int(matchday_number)
    # checke anzahl an jokern
    if m_nr < 1 or m_nr > 7:
        # testing
        if m_nr != 0:
            raise Http404
    if request.method == 'POST':
        for k, v in request.POST.items():  # k id zu tipp post, v tipps
            # print(request.POST.items())
            print('k:', k)
            print('v:', v)
            m = re.match(r'^(?P<home_score>\d+):(?P<guest_score>\d+)', v)
            if k.startswith('Tipp-'):
                try:
                    match_id = int(k.strip('Tipp-'))  # Tipp id started mit "Tipp-" + id
                    # print(match_id)
                except:
                    raise Http404
                # get input in {tipp : tipp} format
                # m = re.match(r'^(?P<home_score>\d+):(?P<guest_score>\d+)', v)
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
                # falls tipp schon vorhanden aber joker wird rausgenommen,
                # dann ist k leer und joker nicht gespeichert.
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

                    print('number_joker: ', get_n_joker(request, m_nr))
                    print('tipp: ', tipp)
                    if is_joker_valid(m_nr, get_n_joker(request, m_nr)) and tipp:
                        print('hihihi')
                        tipp.joker = 1
                        tipp.save()
                    elif not is_joker_valid(m_nr, get_n_joker(request, m_nr)):
                        print('huhuhu')
                        messages.warning(request, 'Zu viele Joker gesetzt! Anzahl Joker:'
                                         + str(get_n_joker(request, m_nr)))
        return HttpResponseRedirect(reverse('tip-matchday', kwargs={'matchday_number': m_nr}))

    match = Match.objects.filter(matchday=m_nr).order_by('match_date')

    tipps = Tip.objects.filter(author=request.user).filter(match__matchday=m_nr)
    tipps_by_matches = {t.match.pk: t for t in tipps}
    current_matchday = Match.objects.filter(match_date__gte=timezone.now()).order_by('match_date')[0].matchday
    context = {
        'number': m_nr,
        'match': match,
        'tipps': tipps_by_matches,
        'c_mday': current_matchday,
    }
    return render(request, 'tip/matchday.html', context)


def is_joker_valid(matchday_in, njoker):
    if matchday_in < 3 and njoker >= 3:
        return False
    return True


def get_n_joker(request, m_nr):
    tipps = Tip.objects.filter(author=request.user).filter(match__matchday=m_nr)
    n_jokes = 0
    for tipp in tipps:
        if tipp.joker:
            n_jokes += 1
    return n_jokes


def about(request):
    return render(request, 'tip/about.html', {'title': 'about'})  # add title by hand


@login_required
@csrf_protect
def update_scores_and_ranks(request):
    for user in Profile.objects.all():
        user.update_score_and_joker()
        user.save()

    # update ranks
    users = Profile.objects.all().order_by('score').reverse()
    rank, tick, score = 1, 0, users[0].score
    for user in users:
        if user.score < score:
            rank += tick
            tick = 1
            score = user.score
        else:
            tick += 1
        if user.rank != rank:
            user.rank = rank
            user.save()
    current_matchday = Match.objects.filter(match_date__gte=timezone.now()).order_by('match_date')[0].matchday
    print(current_matchday)
    return HttpResponseRedirect(reverse('tip-settings', kwargs={'matchday_number': current_matchday}))


@login_required
@csrf_protect
def settings(request, matchday_number):
    m_nr = int(matchday_number)
    current_matchday = Match.objects.filter(match_date__gte
                                            =timezone.now()).order_by('match_date')[0].matchday
    if request.method == 'POST':
        for k, v in request.POST.items():  # k id zu tipp post, v tipps
            # print(request.POST.items())
            print('k_joker:', k)
            print('v_joker:', v)
            if k.startswith('Match-'):
                try:
                    match_id = int(k.strip('Match-'))  # Tipp id started mit "Tipp-" + id
                    print(match_id)
                except:
                    raise Http404
                m = re.match(r'^(?P<home_score>\d+):(?P<guest_score>\d+)', v)
                match = get_object_or_404(Match, pk=match_id)
                print('m', m)
                # match = get_object_or_404(Match, pk=match_id)
                if m:
                    home_score = m.group('home_score')
                    guest_score = m.group('guest_score')
                    if match.has_started():
                        match.home_score = home_score
                        match.guest_score = guest_score
                        print('score:', home_score, guest_score)
                        match.save()
        messages.success(request, 'Gespeichert!')
        return HttpResponseRedirect(reverse('tip-settings', kwargs={'matchday_number': current_matchday}))

    matches = Match.objects.filter(matchday=m_nr)
    matches = matches.order_by('match_date')
    context = {
        'matches': matches,
        'number': m_nr,
        'c_mday': current_matchday,
    }
    return render(request, 'tip/settings.html', context)


def champion(request):
    if request.method == 'POST':
        for k, v in request.POST.items():
            print('k_champion:', k)
            print('v_champion:', v)
            if k.startswith('Champion-'):
                try:
                    champion_id = int(k.strip('Champion-'))  # Tipp id started mit "Tipp-" + id
                    print(champion_id)
                except:
                    raise Http404
                champion = Champion.objects.get(champion__id=champion_id)
                champion.out = 1
                champion.save()
        messages.success(request, 'Gespeichert!')
        return HttpResponseRedirect(reverse('tip-champion'))
    champions = Champion.objects.all()
    context = {
        'champions': champions,
    }
    print(champions)
    return render(request, 'tip/settings/champion.html', context)

