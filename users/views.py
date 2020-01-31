from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib import messages

from Tip.models import Match
from .forms import UserRegisterForm
from .forms import UserUpdateForm
from .forms import ProfileUpdateForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        # form kriegt postdata bei post und nichts bei allem anderen
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # also hashes pwd
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
    # passes to register.html form dict


def profile(request):
    current_matchday = Match.objects.filter(match_date__gte
                                            =timezone.now()).order_by('match_date')[0].matchday
    if request.method == 'POST':
        # gets post and files from current request
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    # pass context to template
    return render(request, 'users/profile.html', context)