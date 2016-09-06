from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Restaurant, Review,Foodie, Poll, Vote

import googlemaps
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(allow_blank=False, write_only=True)
    foodie_id = serializers.URLField(source='foodie.id', allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','is_staff','confirm_pass','foodie_id')
        write_only_fields = ('password','confirm_pass')
        read_only_fields = ('id','is_staff','foodie')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, data):

        user = User.objects.filter(username=data['username'])
        user2 = User.objects.filter(email=data['email'])
        password1 = data['password']
        password2 = data['confirm_pass']
        if user:
            raise serializers.ValidationError("Username exist")
        elif user2:
            raise serializers.ValidationError("Email already registered")
        elif password1 and password1 != password2:
            raise serializers.ValidationError("Passwords don't match")
        else:
            data['username'] = data['username'].lower()
            data['email'] = data['email'].lower()
            return data

class UserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_pass = serializers.CharField()

    def validate_email(self, email):
        existing = User.objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered")
        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_pass'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")
        if data.get('password') != data.get('confirm_pass'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data

class RestaurantSerializer(serializers.ModelSerializer):
    lat = None
    log = None
    avg_review = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    class Meta:
        model = Restaurant
        fields = ('id','url', 'name', 'description', 'street','city','state','avg_review')
        read_only_fields = ('id','url','review_average','avg_review')

    def create(self, validated_data):
        restaurant = Restaurant.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            street=validated_data['street'],
            city=validated_data['city'],
            state=validated_data['state'],
            lat= self.lat,
            log=self.log,
        )

        restaurant.save()

        return restaurant

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        gmaps = googlemaps.Client(key='AIzaSyBY34yk3QSyUtWPfIgBw3mFVVV2XSp6SQw')
        try:
            address = str(data['street'].encode('ascii','ignore')) +  str(data['city'].encode('ascii','ignore')) +  str(data['state'].encode('ascii','ignore'))
        except:
            address = data['street']
        # Geocoding an address
        if not isinstance(address, str):
            geocode_result = gmaps.geocode(address.encode('ascii','ignore'))
        else:
            geocode_result = gmaps.geocode(address)

        if not geocode_result:
            raise serializers.ValidationError("invalid address & location not found")
        else:
            result = geocode_result[0]
            self.log = result['geometry']['location']['lng']
            self.lat = result['geometry']['location']['lat']
        return data

class FoodieSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer('user', read_only=True)
    class Meta:
        model = Foodie
        fields = ('id','url','user')
        read_only_fields = ('id','url')

class ReviewSerializer(serializers.ModelSerializer):
    foodie = FoodieSerializer('foodie', read_only=True)
    foodie_pk = serializers.IntegerField(write_only=True)
    class Meta:
        model = Review
        fields = ('id','url','foodie','foodie_pk', 'subject','restaurant','wouldGo','score','comment','added')
        read_only_fields = ('id','url','added')

    def create(self, validated_data):

        review = Review.objects.create(
            foodie=validated_data['foodie_pk'],
            subject=validated_data['subject'],
            restaurant=validated_data['restaurant'],
            wouldGo=validated_data['wouldGo'],
            score=validated_data['score'],
            comment=validated_data['comment'],
        )
        review.save()
        return review

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if isinstance(data["wouldGo"], (bool)):
            pass
        elif data["wouldGo"].lower() == 'false':
            data["wouldGo"]=False
        elif data["wouldGo"].lower() == 'true':
            data["wouldGo"]=True
        else:
            raise serializers.ValidationError("incorrect Boolean value for wouldGo")

        foodie = Foodie.objects.get(id=data["foodie_pk"])
        if not Foodie.objects.get(id=data["foodie_pk"]):
            raise serializers.ValidationError("No such foodie exists")
        else:
            data['foodie_pk']=foodie
        return data


class PollSerializer(serializers.ModelSerializer):
    restaurants = RestaurantSerializer(many=True, read_only=True)
    class Meta:
        model = Poll
        # fields = ('id','url','creator','status','restaurants','added')
        read_only_fields = ('id','url','added')
class VoteSerializer(serializers.ModelSerializer):
    foodie = FoodieSerializer('foodie', read_only=True)
    foodie_pk = serializers.IntegerField(write_only=True)
    class Meta:
        model = Vote
        fields = ('id','url','foodie_pk','choice','foodie','poll')
        read_only_fields = ('id','url')

    def create(self, validated_data):
        foodie = Foodie.objects.get(id=validated_data["foodie_pk"])
        if not Foodie.objects.get(id=validated_data["foodie_pk"]):
            raise serializers.ValidationError("No such foodie exists")
        elif len(Vote.objects.filter(foodie=foodie, poll=validated_data["poll"])) > 0:
            raise serializers.ValidationError("foodie has voted for this poll already")
        else:
            validated_data['foodie_pk']=foodie

        vote = Vote.objects.create(
            foodie=validated_data['foodie_pk'],
            choice=validated_data['choice'],
            poll=validated_data['poll'],
        )
        vote.save()
        return vote

    def update(self, instance, validated_data):
        instance.foodie = validated_data.get('foodie', instance.foodie)
        instance.choice = validated_data.get('choice', instance.choice)
        instance.poll = validated_data.get('poll', instance.poll)
        instance.save()
        return instance

