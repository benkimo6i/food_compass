from django.contrib.auth.models import User
from rest_framework import viewsets, response, permissions
from .serializers import UserSerializer, RestaurantSerializer, ReviewSerializer, FoodieSerializer, PollSerializer,VoteSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from .permissions import IsStaffOrTargetUser, IsOwnerOrStaffElseReadonly_Vote, IsPollOwnerOrStaffElseReadonly_Vote
from django.http import JsonResponse
from rest_framework import filters

from .models import Restaurant, Review, Foodie, Poll, Vote

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from django.db.models import Avg, Count

from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

auth = Oauth1Authenticator(
    consumer_key='94p7bLJKx469uLZ6XR_YtQ',
    consumer_secret='67Jo2OFim22BvxzERZ9Fp_N2Ass',
    token='DdWAe4A1oTBYqNcu6BJ9N7M_Vs6WSN9f',
    token_secret='hqrDp8pHHQPHR6-U3HcEitCqaoQ'
)

client = Client(auth)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter)
    pagination_class = LimitOffsetPagination
    ordering_fields = ('added', 'avg_review')
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        return (IsAdminUser() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),
    def get_queryset(self):
        return Restaurant.objects.annotate(
            avg_review=Avg('review__score')
        )

    def retrieve(self, request, pk=None):
        restaurant = Restaurant.objects.get(id=pk)
        custom_data = {
            'restaurant': RestaurantSerializer(restaurant,context={'request':request}).data
        }
        custom_data.update({
            'average_score' : format(restaurant.review_set.aggregate(Avg('score')).values()[0], '.2f')
        })

        return response.Response(custom_data)

    # def retrieve(self, request, pk=None):
    #     custom_data = {
    #         'list_of_items': ItemSerializer(self.get_queryset(),many=true).data  # this is the default result you are getting today
    #     }
    #     custom_data.update({
    #         'quote_of_the_day': # code to compute Quote of the day
    #         'number_of_times': # code to compute number of times
    #     })
    #     return Response(custom_data)
    #
    #     restaurant = Restaurant.objects.get(id=pk)
    #     average_score = restaurant.review_set.aggregate(Avg('score')).values()[0]
    #     print average_score
    #     return super(RestaurantViewSet, self).retrieve(request, pk)

class ReviewViewSet(viewsets.ModelViewSet):
    #/api/reviews/?ordering=score&limit=1&offset=0
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter)
    filter_fields = ('subject','restaurant','foodie')
    pagination_class = LimitOffsetPagination
    ordering_fields = ('subject', 'added', 'score')
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        return (IsOwnerOrStaffElseReadonly_Vote() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),
    #
    # def get_permissions(self):
    #     # allow non-authenticated user to create via POST
    #     return (IsAdminUser() if self.request.method == 'POST'
    #             else permissions.IsAuthenticated()),
    #
    # def get_permissions(self):
    #     # allow non-authenticated user to create via POST
    #     if self.request.method == 'POST':
    #         return IsAdminUser()
    #     else:
    #         return

class FoodieViewSet(viewsets.ModelViewSet):
    queryset = Foodie.objects.all()
    serializer_class = FoodieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        return (IsPollOwnerOrStaffElseReadonly_Vote() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),

    def retrieve(self, request, pk=None):
         poll = Poll.objects.get(id=pk)
         custom_data = {
             'poll': PollSerializer(poll,context={'request':request}).data
         }
         selections=[]
         for restaurant in poll.Restaurants.all():
             selections.append(restaurant)
         selection_vote_counts = {}
         for selection in selections:
            selection_vote_counts[str(selection.name)] = poll.vote_set.filter(choice=selection.id).aggregate(Count('id')).values()[0]
         custom_data.update({
             'vote_counts' : selection_vote_counts
         })

         return response.Response(custom_data)

    # filter_fields = ('subject','restaurant','foodie')

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('foodie','poll','choice')
    #
    permission_classes = (permissions.IsAuthenticated,)
    def get_permissions(self):
        return (IsOwnerOrStaffElseReadonly_Vote() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),

    # filter_fields = ('subject','restaurant','foodie')




