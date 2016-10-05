from django.conf.urls import include, url
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import CircleViewSet, UserViewSet, RestaurantViewSet, ReviewViewSet, FoodieViewSet, PollViewSet, VoteViewSet, ProfileImageViewSet, CircleMembershipViewSet, CircleImageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'foodies', FoodieViewSet)
router.register(r'polls', PollViewSet)
router.register(r'votes', VoteViewSet)
router.register(r'upload_image',ProfileImageViewSet)
router.register(r'circles',CircleViewSet)
router.register(r'circle_memberships',CircleMembershipViewSet)
router.register(r'circle_image',CircleImageViewSet)


urlpatterns = router.urls

urlpatterns += [
    url(r'^obtain-auth-token/$', csrf_exempt(obtain_auth_token)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
