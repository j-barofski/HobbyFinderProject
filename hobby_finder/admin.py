# for registering the models.py file 
# trying to connect the sql

from django.contrib import admin # import admin module
from .models import Hobby # import hobby model from models.py

@admin.register(Hobby) # register model
class HobbyAdmin(admin.ModelAdmin):
    list_display = ('name') # show the names