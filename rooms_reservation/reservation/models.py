from django.db import models

# Create your models here.
class Rooms(models.Model):
    name = models.CharField(max_length = 128)
    capacity = models.IntegerField(null = False)
    projector = models.BooleanField(default = False)
    
class Reservations(models.Model):
    date_from = models.DateField(null = False)
    date_to = models.DateField(null = False)
    days = models.IntegerField()
    description = models.CharField(max_length = 512, null = True)
    room = models.ForeignKey(Rooms, on_delete = models.CASCADE)