from django.shortcuts import render
from .models import Tip
from .models import Match, Team


def home(request):
    context = {
        'tip': Tip.objects.all(),
        'match': Match.objects.all(),
        'team': Team.objects.all(),
    }
    return render(request, 'tip/home.html', context)  # make tip accessible for request
    # HttpResponse('<h1> Tip Home</h1>')


def matchplan(request):
    context = {
        'match': Match.objects.all(),
        'team': Team.objects.all(),
    }
    return render(request, 'tip/matchplan.html', context)


def about(request):
    return render(request, 'tip/about.html', {'title': 'about'})  # add title by hand
