from django.shortcuts import render
from django.views.generic import RedirectView


def home(request):
    return render(request, 'home.html')


class ProfileRedirect(RedirectView):
    pattern_name = 'home'