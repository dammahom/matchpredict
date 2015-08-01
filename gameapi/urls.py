from django.conf.urls import url, include
from . import views
from .models import *
from rest_framework import routers, permissions, serializers, viewsets
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League


class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['leagues']
    queryset = League.objects.all()
    serializer_class = League


router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)
router.register(r'leagues', LeagueViewSet)

urlpatterns = [
    url(r'^index', views.index),

    url(r'^', include(router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
