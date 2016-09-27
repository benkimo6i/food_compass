from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.text import slugify
# Create your models here.

POLLS_STATUS_CHOICES = (('open', 'Open'),
                        ('closed', 'Closed'),
                        )




class Foodie(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __unicode__(self):
        return self.user.username

def image_upload_to(instance, filename):
    title = instance.owner.user.username
    print("Image title: "+title)
    slug = slugify(title)
    return "profile_images/%s/%s" %(slug, filename)

class ProfileImage(models.Model):
    owner = models.ForeignKey(Foodie)
    datafile = models.ImageField(upload_to=image_upload_to)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.datafile)



class Restaurant(models.Model):
    name = models.CharField(max_length = 120)
    description = models.CharField(max_length=400, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    lat = models.DecimalField(max_digits=12,decimal_places=10)
    log = models.DecimalField(max_digits=12,decimal_places=10)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __unicode__(self):
        return self.name

    def get_address(self):
        full_address = "%s, %s, %s %s" %(self.street, self.city, self.state)
        return full_address


class Review(models.Model):
    foodie = models.ForeignKey(Foodie)
    subject = models.CharField(max_length=80, null=False)
    restaurant = models.ForeignKey(Restaurant)
    wouldGo = models.BooleanField(default=True)
    score = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    comment = models.CharField(max_length=800, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

def foodie_saved_receiver(sender, instance, created, *args, **kwargs):
    user = instance
    foodie = Foodie.objects.filter(user = user)
    if not foodie:
        new_foodie = Foodie()
        new_foodie.user = user
        new_foodie.save()
        print new_foodie

post_save.connect(foodie_saved_receiver,sender = User)

class Poll(models.Model):
    title = models.CharField(max_length=80, null=False)
    description = models.CharField(max_length=320, null=False)
    creator = models.ForeignKey(Foodie)
    added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=120, choices=POLLS_STATUS_CHOICES, default='open')
    Restaurants = models.ManyToManyField(Restaurant)


    def __unicode__(self):
        return self.title


class Vote(models.Model):
    foodie = models.ForeignKey(Foodie)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Restaurant)

class Circle(models.Model):
    name = models.CharField(max_length=140, null=False)
    description = models.CharField(max_length=140, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    lat = models.DecimalField(max_digits=12,decimal_places=10)
    log = models.DecimalField(max_digits=12,decimal_places=10)
    added = models.DateTimeField(auto_now_add=True)
    master = models.ForeignKey(Foodie, null=True, related_name='circle_masters')


    def __unicode__(self):
        return self.name

class CircleMembership(models.Model):
    foodie = models.ForeignKey(Foodie)
    circle = models.ForeignKey(Circle)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.circle+" - "+self.foodie
