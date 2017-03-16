from django.db import models

# Create your models here.
      
class Address(models.Model):
    city = models.CharField(max_length = 32)
    street = models.CharField(max_length = 32)
    house = models.CharField(max_length = 10)
    apartment = models.CharField(max_length = 10, null = True)

class Person(models.Model):
    name = models.CharField(max_length = 32)
    surname = models.CharField(max_length = 64)
    description = models.TextField(null = True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    
class Phone(models.Model):
    number = models.IntegerField(null = True, unique = True)
    description = models.CharField(max_length = 32, null = True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

class Email(models.Model):
    email = models.EmailField(max_length = 128, null = True, unique = True)
    description = models.CharField(max_length = 32, null = True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)