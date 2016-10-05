from django.contrib.auth.models import User
from .models import Restaurant, Review, Foodie, Poll, Vote, ProfileImage, Circle,CircleMembership, CircleImage

from rest_framework import viewsets, response, permissions
from .serializers import UserSerializer, RestaurantSerializer, ReviewSerializer, FoodieSerializer, PollSerializer,VoteSerializer, ProfileImageUploadSerializer, CircleSerializer, CircleMembershipSerializer, CircleImageUploadSerializer

from .permissions import IsStaffOrTargetUser, IsOwnerOrStaffElseReadonly_Vote, IsPollOwnerOrStaffElseReadonly_Vote, IsImageOwnerOrStaffElseReadonly
from rest_framework.permissions import AllowAny

from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import LimitOffsetPagination
from django.db.models import Avg, Count


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'
                else IsStaffOrTargetUser()),

    def list(self, request, *args, **kwargs):
        if request.method == 'GET' and 'username_starts' in request.GET:
            print("filtering on username test")
            username_starts = request.GET.get('username_starts')
            if username_starts is not None and username_starts != '':
                queryset = User.objects.filter(username__startswith=(username_starts))
                serializer = UserSerializer(queryset, many=True)
                return response.Response(serializer.data)
        else:
            return super(UserViewSet, self).list(request)


    def retrieve(self, request, pk=None):
        if pk == 'i':
            return response.Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)

    def perform_update(self, serializer):
        serializer.save()
        return response.Response(serializer.data)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = (filters.DjangoFilterBackend,filters.OrderingFilter)
    pagination_class = LimitOffsetPagination
    ordering_fields = ('added', 'avg_review')
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Restaurant.objects.annotate(
            avg_review=Avg('review__score')
        )

    def retrieve(self, request, pk=None):
        restaurant = Restaurant.objects.get(id=pk)
        custom_data = {
            'restaurant': RestaurantSerializer(restaurant,context={'request':request}).data
        }
        avg_score = 0
        try:
            avg_score = format(restaurant.review_set.aggregate(Avg('score')).values()[0], '.2f')
        except:
            pass
        custom_data.update({
            'average_score' : avg_score
        })
        return response.Response(custom_data)


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


class FoodieViewSet(viewsets.ModelViewSet):
    queryset = Foodie.objects.all()
    serializer_class = FoodieSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        return (IsStaffOrTargetUser() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),


class ProfileImageViewSet(viewsets.ModelViewSet):
    queryset = ProfileImage.objects.all()
    serializer_class = ProfileImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        return (IsImageOwnerOrStaffElseReadonly() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),


    def perform_create(self, serializer):
        print("uploading image")
        print(self.request.data.get('datafile'))
        print(self.request.FILES)
        print(self.request.FILES['image'])
        serializer.save(owner=self.request.user.foodie,
                       datafile=self.request.FILES['image'])



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


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('foodie','poll','choice')
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        return (IsOwnerOrStaffElseReadonly_Vote() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),

class CircleImageViewSet(viewsets.ModelViewSet):
    queryset = CircleImage.objects.all()
    serializer_class = CircleImageUploadSerializer
    parser_classes = (MultiPartParser, FormParser,)
    # permission_classes = (permissions.IsAuthenticated,)

    # def get_permissions(self):
    #     return (IsImageOwnerOrStaffElseReadonly() if self.request.method not in permissions.SAFE_METHODS
    #             else permissions.IsAuthenticated()),


    def perform_create(self, serializer):
        print("uploading circle image")
        print(self.request.data.get('datafile'))
        print(self.request.FILES)
        print('---------')
        for key, value in self.request.FILES.iteritems():
            print(key)


        # print(self.request.FILES['circle_id'])
        # print(self.request.FILES['image'])
        circle = Circle.objects.get(id=int(self.request.data.get('circle_id')))
        serializer.save(circle=circle,
                       datafile=self.request.FILES['image'])

class CircleViewSet(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # permission_classes = (permissions.IsAuthenticated,)
    #
    # def get_permissions(self):
    #     return (IsOwnerOrStaffElseReadonly_Vote() if self.request.method not in permissions.SAFE_METHODS
    #             else permissions.IsAuthenticated()),
    def perform_update(self, serializer):
        serializer.save()
        return response.Response(serializer.data)

class CircleMembershipViewSet(viewsets.ModelViewSet):
    queryset = CircleMembership.objects.all()
    serializer_class = CircleMembershipSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        return (IsOwnerOrStaffElseReadonly_Vote() if self.request.method not in permissions.SAFE_METHODS
                else permissions.IsAuthenticated()),

    def list(self, request, *args, **kwargs):
        if request.method == 'GET' and 'circle_id' in request.GET:
            print("filtering on circle test")
            circle_id = request.GET.get('circle_id')
            circle = Circle.objects.filter(id=circle_id)
            if circle is not None and circle != '':
                queryset = CircleMembership.objects.filter(circle=circle)
                serializer = CircleMembershipSerializer(queryset, many=True, context={'request':request})
                return response.Response(serializer.data)

        else:
            return super(CircleMembershipViewSet, self).list(request)





