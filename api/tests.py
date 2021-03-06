from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Foodie,Restaurant, Poll, Vote, ProfileImage, Circle, CircleMembership
from django.core.urlresolvers import reverse
from urlparse import urlparse
from django.conf import settings

# Create your tests here.

class UserTests(TestCase):
    def test_create_user(self):
        """
        Ensure we can create a new User object.
        """
        data = {'username': 'test_user', 'email':'test@test.com', 'password':'123qazwsx', 'confirm_pass':'123qazwsx', "new_pass":"", "new_confirm_pass":""}
        response = self.client.post('/api/users/', data, format='json')
        print (response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_user')

class CircleTests(TestCase):
    def setUp(self):
            self.user = User.objects.create(username= 'test_user', email='test@test.com', password='123qazwsx')
            self.token = Token.objects.get(user=self.user).key
            self.c = Client()
            self.other_foodie = User.objects.create(username= 'other_foodie', email='other_foodie@test.com', password='123qazwsx')

    def test_create_circle_with_no_foodies_or_admins(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
            data =  {"name": "test","description": "test test test","street": "147-45 84th ave","city": "briarwood","state": "NY"}
            response = self.client.post('/api/circles/', data, format='json', **header)
            print response
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(Circle.objects.count(), 1)
            self.assertEqual(Circle.objects.get().name, 'test')
            self.assertEqual(Circle.objects.get().master, self.user.foodie)

    def test_create_circle(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
            data =  {"name": "test","description": "test test test","street": "147-45 84th ave","city": "briarwood","state": "NY"}
            response = self.client.post('/api/circles/', data, format='json', **header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(Circle.objects.count(), 1)
            self.assertEqual(Circle.objects.get().name, 'test')
            self.assertEqual(Circle.objects.get().master, self.user.foodie)

            data =  {"foodie": 1,"circle": 1}
            response = self.client.post('/api/circle_memberships/', data, format='json', **header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(CircleMembership.objects.count(), 1)
            self.assertEqual(CircleMembership.objects.get().foodie, self.user.foodie)
            self.assertEqual(CircleMembership.objects.get().circle, Circle.objects.get())



class RestaurantNonAdminTests(TestCase):
        """
        Ensure user can create a new Restaurant object.
        """
        def setUp(self):
            self.user = User.objects.create(username= 'test_user', email='test@test.com', password='123qazwsx')
            self.token = Token.objects.get(user=self.user).key
            self.c = Client()

        def test_create_restaurant(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
            data =  {"name": "test_restaurant","description": "test test","street": "147-45 84th ave","city": "briarwood","state": "NY"}
            response = self.client.post('/api/restaurants/', data, format='json', **header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(User.objects.count(), 1)
            self.assertEqual(User.objects.get().username, 'test_user')

# class RestaurantNonAdminTests(TestCase):
#         """
#         Ensure non-admin cannot create a new Restaurant object.
#         """
#         def setUp(self):
#             self.user = User.objects.create(username= 'test_user', email='test@test.com', password='123qazwsx')
#             self.token = Token.objects.get(user=self.user).key
#             self.c = Client()
#
#         #non-admin should 403.
#         def test_create_restaurant(self):
#             header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
#             data =  {"name": "test_restaurant","description": "test test","street": "147-45 84th ave","city": "briarwood","state": "NY"}
#             response = self.client.post('/api/restaurants/', data, format='json', **header)
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "REST token-auth failed - "+str(response.status_code))
#             self.assertEqual(User.objects.count(), 1)
#             self.assertEqual(User.objects.get().username, 'test_user')

# class RestaurantAdminTests(TestCase):
#         """
#         Ensure admin can create a new Restaurant object.
#         """
#         def setUp(self):
#             #staff user
#             self.user = User.objects.create(username= 'admin_user', email='test@test.com', password='123qazwsx', is_staff=True)
#             self.token = Token.objects.get(user=self.user).key
#             self.c = Client()
#
#             #non-staff user
#             self.non_admin_user = User.objects.create(username= 'non_admin_user', email='test2@test.com', password='123qazwsx')
#             self.non_admin_user_token = Token.objects.get(user=self.non_admin_user).key
#             self.c2 = Client()
#
#         #non-staff should get 403.
#         def test_non_admin_403_create_restaurant(self):
#             header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.non_admin_user_token)}
#             data =  {"name": "test_restaurant","description": "test test","street": "147-45 84th ave","city": "briarwood","state": "NY"}
#             response = self.client.post('/api/restaurants/', data, format='json', **header)
#             self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "REST token-auth failed - "+str(response.status_code))
#
#         #staff users should get 201.
#         def test_create_restaurant(self):
#             header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
#             data =  {"name": "test_restaurant","description": "test test","street": "147-45 84th ave","city": "briarwood","state": "NY"}
#             response = self.client.post('/api/restaurants/', data, format='json', **header)
#             self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
#             self.assertEqual(Restaurant.objects.count(), 1)
#             self.assertEqual(Restaurant.objects.get().name, 'test_restaurant')

class PollTests(TestCase):
        """
        Ensure we can create a new Poll object.
        """
        def setUp(self):
            self.user = User.objects.create(username= 'test_user', email='test@test.com', password='123qazwsx')
            self.token = Token.objects.get(user=self.user).key
            self.c = Client()
            self.foodie = Foodie.objects.get(user=self.user)
            restaurant = Restaurant.objects.create(name="test_restaurant",description="test test",street= "147-45 84th ave",city="briarwood",state="NY", lat=0.11, log=0.11)
            self.restaurants = [restaurant.id]

        def test_create_poll(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
            data =  {"title": "test_poll","description": "test_poll","status": "open","creator": self.foodie.id,"Restaurants": self.restaurants}
            response = self.client.post('/api/polls/', data, format='json', **header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(Poll.objects.count(), 1)
            self.assertEqual(Poll.objects.get().title, 'test_poll')

class VoteTests(APITestCase):
        """
        Ensure we can create a new Poll object.
        """
        def setUp(self):
            self.user = User.objects.create(username= 'test_user', email='test@test.com', password='123qazwsx')
            self.token = Token.objects.get(user=self.user).key
            self.c = Client()
            self.foodie = Foodie.objects.get(user=self.user)

            self.user2 = User.objects.create(username= 'test_user_2', email='test2@test.com', password='123qazwsx')
            self.token2 = Token.objects.get(user=self.user2).key
            self.c2 = Client()
            self.foodie2 = Foodie.objects.get(user=self.user2)

            restaurant = Restaurant.objects.create(name="test_restaurant",description="test test",street= "147-45 84th ave",city="briarwood",state="NY", lat=0.11, log=0.11)
            restaurant2 = Restaurant.objects.create(name="test_restaurant_2",description="test test",street= "147-45 84th ave",city="briarwood",state="NY", lat=0.11, log=0.11)
            poll = Poll.objects.create(title="test_poll", description="test", creator=self.foodie, status="open")
            poll.save()
            poll.Restaurants.add(restaurant)
            poll.Restaurants.add(restaurant2)
            poll.save()
            self.poll= poll
            self.choice = restaurant
            self.choice2 = restaurant2
            vote_to_be_edited = Vote.objects.create(poll=self.poll,foodie=self.foodie2,choice= self.choice )
            vote_to_be_edited.save()
            self.vote_to_be_edited = vote_to_be_edited

        def test_create_vote(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
            data =  {"poll": self.poll.id, "choice": self.choice.id, "foodie_pk": self.foodie.id}
            response = self.client.post('/api/votes/', data, format='json', **header)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(Vote.objects.count(), 2)
            self.assertEqual(Vote.objects.filter(foodie=self.foodie)[0].poll, self.poll,"error is - "+ str(Vote.objects.filter(foodie=self.foodie)[0].poll))
            self.assertEqual(Vote.objects.filter(foodie=self.foodie)[0].choice, self.choice)
            self.assertEqual(Vote.objects.filter(foodie=self.foodie)[0].foodie, self.foodie)

        #only owner of the vote can edit the vote
        def test_edit_vote(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token2)}
            data =  {"poll": self.poll.id, "choice": self.choice2.id, "foodie_pk": self.foodie2.id}
            response = self.client.put('/api/votes/'+str( self.vote_to_be_edited.id)+"/", data, format='json', **header)
            self.assertEqual(response.status_code, status.HTTP_200_OK, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(Vote.objects.count(), 1)
            self.assertEqual(Vote.objects.get().poll, self.poll,"error is - "+ str(Vote.objects.get().poll))
            self.assertEqual(Vote.objects.get().choice, self.choice2)
            self.assertEqual(Vote.objects.get().foodie, self.foodie2)

        #only owner of the vote can edit the vote - will return 403 forbidden if put request is submitted by someone else
        def test_403_edit_vote(self):
            header = {'HTTP_AUTHORIZATION': 'Token {}'.format(self.token)}
            data =  {"poll": self.poll.id, "choice": self.choice2.id, "foodie_pk": self.foodie2.id}
            print(data)
            response = self.client.put('/api/votes/'+str( self.vote_to_be_edited.id)+"/", data, format='json', **header)
            print(response.status_code)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, "REST token-auth failed - "+str(response.status_code))
            self.assertEqual(Vote.objects.count(), 1)
            self.assertEqual(Vote.objects.get().poll, self.poll,"error is - "+ str(Vote.objects.get().poll))
            #should remain the same
            self.assertEqual(Vote.objects.get().choice, self.choice)
            self.assertEqual(Vote.objects.get().foodie, self.foodie2)





