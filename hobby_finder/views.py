# fetches hobbies

from django.shortcuts import render # render templates
from .models import Hobby # import hobby model

def get_hobbies(request): # gets and show the hobbies
    hobbies = Hobby.objects.all() # get all hobbies
    return render(request, 'dashboard.html', {'hobbies': hobbies}) # render to the dashboard