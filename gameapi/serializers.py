from django.forms import widgets
from rest_framework import serializers
from .models import *


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ('id', 'name', 'country')

