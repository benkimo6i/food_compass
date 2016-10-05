from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Restaurant, Review,Foodie, Poll, Vote, ProfileImage, Circle, CircleMembership, CircleImage

from rest_framework.fields import CurrentUserDefault

import googlemaps


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(allow_blank=False, write_only=True)
    confirm_pass = serializers.CharField(allow_blank=False, write_only=True)
    new_pass = serializers.CharField(allow_blank=True, write_only=True)
    new_confirm_pass = serializers.CharField(allow_blank=True, write_only=True)
    foodie_id = serializers.URLField(source='foodie.id', allow_blank=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email','is_staff','confirm_pass','foodie_id', 'new_pass', 'new_confirm_pass')
        write_only_fields = ('password','confirm_pass', 'new_pass', 'new_confirm_pass')
        read_only_fields = ('id','is_staff','foodie')

    def create(self, validated_data):
        user = User.objects.filter(username=validated_data['username'])
        user2 = User.objects.filter(email=validated_data['email'])
        password1 = validated_data['password']
        password2 = validated_data['confirm_pass']
        if user:
            raise serializers.ValidationError("Username exist")
        elif user2:
            raise serializers.ValidationError("Email already registered")
        elif password1 and password1 != password2:
            raise serializers.ValidationError("Passwords don't match")
        else:
            validated_data['username'] = validated_data['username'].lower()
            validated_data['email'] = validated_data['email'].lower()

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        print("calling update/patch serializer method")

        if 'username' in validated_data:
                if validated_data['username'] != instance.username:
                    user = User.objects.filter(username=validated_data['username'])
                    if user:
                        raise serializers.ValidationError("Username exist")
        if 'email' in validated_data:
            if validated_data['email'] != instance.email:
                print("email ")
                email = User.objects.filter(email=validated_data['email'])
                if email:
                    print("email 1")
                    raise serializers.ValidationError("Email exist")

        if validated_data.viewkeys() >= {'password','new_pass','new_confirm_pass'}:
            if validated_data["password"] or validated_data["new_pass"] or validated_data["new_confirm_pass"]:
                if (validated_data["password"] and validated_data["new_pass"] and validated_data["new_confirm_pass"]):
                    if instance.check_password(validated_data["password"]):
                        if validated_data["new_pass"] == validated_data["new_confirm_pass"]:
                            instance.set_password(validated_data["new_pass"])
                        else:
                            raise serializers.ValidationError("new password and new confirmation password do not match")
                    else:
                        raise serializers.ValidationError("Current password incorrect")
        elif validated_data.viewkeys() & {'password','new_pass','new_confirm_pass'}:
            raise serializers.ValidationError("Missing required password field(s)")

        for attr, value in validated_data.items():
            if attr != "password" and attr != "new_pass" and attr != "new_confirm_pass":
                setattr(instance, attr, value)
            else:
                pass
        instance.save()

        return instance

    # def validate(self, data):
    #     user = User.objects.filter(username=data['username'])
    #     user2 = User.objects.filter(email=data['email'])
    #
    #     if user:
    #         raise serializers.ValidationError("Username exist")
    #     elif user2:
    #         raise serializers.ValidationError("Email already registered")
    #     else:
    #         data['username'] = data['username'].lower()
    #         data['email'] = data['email'].lower()
    #         return data

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
        fields = ('id','url', 'name', 'description', 'street','city','state','avg_review','lat', 'log'  )
        read_only_fields = ('id','url','review_average','avg_review', 'lat', 'log')

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

class ProfileImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        read_only_fields = ('added','updated','owner', 'url', 'datafile')
    def create(self, validated_data):
        try:
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                if ProfileImage.objects.filter(owner=user.foodie.id) > 0:
                    print("deleting image object")
                    ProfileImage.objects.filter(owner=user.foodie.id).delete()
        except:
            pass
        return ProfileImage.objects.create(**validated_data)

class FoodieSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer('user', read_only=True)
    profileimage_set = ProfileImageUploadSerializer(many=True, read_only=True)
    class Meta:
        model = Foodie
        fields = ('id','url','user','profileimage_set')
        read_only_fields = ('id','url')


class ReviewSerializer(serializers.ModelSerializer):
    foodie = FoodieSerializer('foodie', read_only=True)
    foodie_pk = serializers.IntegerField(write_only=True)
    restaurant_name = serializers.ReadOnlyField(source="restaurant.name")
    #restaurant = serializers.SlugRelatedField(slug_field='name', queryset=Restaurant.objects.all())
    #restaurant = serializers.StringRelatedField()
    class Meta:
        model = Review
        fields = ('id','url','foodie','foodie_pk','restaurant_name', 'subject','restaurant','wouldGo','score','comment','added')
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

class CircleImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CircleImage
        read_only_fields = ('added','updated','circle', 'url', 'datafile')
    def create(self, validated_data):
        print(validated_data)
        images = CircleImage.objects.filter(circle = validated_data['circle'])
        if len(images) > 0:
            CircleImage.objects.filter(circle = validated_data['circle']).delete()
        return CircleImage.objects.create(**validated_data)


class CircleSerializer(serializers.ModelSerializer):
    lat = None
    log = None
    master = FoodieSerializer(read_only=True)
    circleimage_set = CircleImageUploadSerializer(many=True, read_only=True)
    # foodies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Circle
        fields = ('id','url','name','description','street','city','state','master', 'lat','log','circleimage_set')
        read_only_fields = ('id','url','added', 'master', 'lat','log')

    def create(self, validated_data):
        master = self.context['request'].user.foodie
        circle = Circle.objects.create(
            name = validated_data['name'],
            description = validated_data['description'],
            street = validated_data['street'],
            city = validated_data['city'],
            state = validated_data['state'],
            lat= self.lat,
            log=self.log,
            master = master
        )
        circle.save()
        return circle

    def update(self, instance, validated_data):
        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        print("calling update/patch serializer method")
        print(validated_data)

        if u'name' in validated_data:
                if validated_data['name'] != instance.name:
                    circle = Circle.objects.filter(name=validated_data['name'])
                    if circle:
                        raise serializers.ValidationError("circle exist")
                        return instance
                    else:
                        print("setting new circle name")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            if self.lat and self.log:
                instance.lat = self.lat
                instance.log = self.log
        instance.save()
        print(instance)
        return instance

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if all (k in data for k in ("street","city","state")):
            print("starting gmap service")
            gmaps = googlemaps.Client(key='AIzaSyBY34yk3QSyUtWPfIgBw3mFVVV2XSp6SQw')
            print("starting gmap service 2")
            try:
                address = str(data['street'].encode('ascii','ignore')) +  str(data['city'].encode('ascii','ignore')) +  str(data['state'].encode('ascii','ignore'))
            except:
                address = data['street']
            print("starting gmap service 3")
            # Geocoding an address
            if not isinstance(address, str):
                geocode_result = gmaps.geocode(address.encode('ascii','ignore'))
            else:
                geocode_result = gmaps.geocode(address)
            print("starting gmap service 4")
            if not geocode_result:
                raise serializers.ValidationError("invalid address & location not found")
            else:
                result = geocode_result[0]
                self.log = result['geometry']['location']['lng']
                self.lat = result['geometry']['location']['lat']
                print("finished gmap service")

        return data



class CircleMembershipSerializer(serializers.ModelSerializer):
    circle_name = serializers.ReadOnlyField(source="circle.name")
    foodie_info = FoodieSerializer(source="foodie",read_only=True)
    class Meta:
        model = CircleMembership
        fields = ('foodie','circle','circle_name','foodie_info')
        read_only_fields = ('id','url', 'added')
