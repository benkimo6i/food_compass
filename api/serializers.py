from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Circle, Restaurant, Review



import googlemaps
from datetime import datetime


class UserSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(allow_blank=False, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','is_staff','confirm_pass')
        write_only_fields = ('password','confirm_pass')
        read_only_fields = ('id','is_staff')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        print(data)
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
        return data

class UserSerializer(serializers.ModelSerializer):
    confirm_pass = serializers.CharField(allow_blank=False, write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','is_staff','confirm_pass')
        write_only_fields = ('password','confirm_pass')
        read_only_fields = ('id','is_staff')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, data):
        print(data)
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
    class Meta:
        model = Restaurant
        fields = ('id','url', 'name', 'description', 'street','city','state')
        read_only_fields = ('id','url',)

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
        print("validate restaurant - 0")
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
        print("validate restaurant - 1")
        return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id','url', 'subject','restaurant','wouldGo','score','comment')
        read_only_fields = ('id','url')

class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('id', 'name')

    def create(self, validated_data):

        print("creating cirle - 0")
        circle = Circle.objects.create(
            name=validated_data['name'],
            location=validated_data['location'],
        )
        print("creating cirle - 1")
        circle.save()

        return circle

