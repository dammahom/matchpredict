from django.conf.urls import url, include
from . import views
from .models import *
from rest_framework import routers, permissions, serializers, viewsets
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
# router.register(r'leagues', views.league_list)

urlpatterns = [
    url(r'^index', views.index),

    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^leagues/$', views.LeagueList.as_view()),
    url(r'^leagues/(?P<pk>[0-9]+)/$', views.LeagueDetail.as_view()),
]
