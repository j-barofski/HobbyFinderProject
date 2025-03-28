# Model for my hobbies

from django.db import models # import models module from django

class Hobby(models.model): # hobby model
    name = models.CharField(max_length = 255) # character field with max length of 255
    
    def __str__(self): # string to show name 
        return self.name