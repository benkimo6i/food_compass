from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.



class Circle(models.Model):
    name = models.CharField(max_length = 120)
    location = models.CharField(max_length = 400)

    def __unicode__(self):
        return self.name

class Foodie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    circles = models.ManyToManyField(Circle)

    def __unicode__(self):
        return self.user.username

class Restaurant(models.Model):
    name = models.CharField(max_length = 120)
    description = models.CharField(max_length=400, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    lat = models.DecimalField(max_digits=12,decimal_places=10)
    log = models.DecimalField(max_digits=12,decimal_places=10)


    def __unicode__(self):
        return self.name

    def get_address(self):
        full_address = "%s, %s, %s %s" %(self.street, self.city, self.state)
        return full_address


class Review(models.Model):
    subject = models.CharField(max_length=80, null=False)
    restaurant = models.ForeignKey(Restaurant)
    wouldGo = models.BooleanField(default=True)
    score = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    comment = models.CharField(max_length=800, null=True)


def foodie_saved_receiver(sender, instance, created, *args, **kwargs):
    print("create new foodie")
    user = instance
    foodie = Foodie.objects.filter(user = user)
    if not foodie:
        new_foodie = Foodie()
        new_foodie.user = user
        new_foodie.save()
        print new_foodie

post_save.connect(foodie_saved_receiver,sender = User)