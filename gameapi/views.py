from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


def index(request):
    return HttpResponse("Hello :)")


# @api_view(['GET', 'POST'])
# def league_list(request):
#     if request.method == 'GET':
#         leagues = League.objects.all()
#         serializer = LeagueSerializer(leagues, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = LeagueSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.data, status=400)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def league_detail(request, pk):
#     try:
#         league = League.objects.get(pk=pk)
#     except League.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = LeagueSerializer(league)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = LeagueSerializer(league, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     elif request.method == 'DELETE':
#         league.delete()
#         return HttpResponse(status=status.HTTP_204_NO_CONTENT)
#

class LeagueList(APIView):
    def get(self, request):
        leagues = League.objects.all()
        serializer = LeagueSerializer(leagues, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = LeagueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.data, status=400)


class LeagueDetail(APIView):
    def get_object(self, pk):
        try:
            return League.objects.get(pk=pk)
        except League.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        league = self.get_object(pk)
        serializer = LeagueSerializer(league)
        return Response(serializer.data)

    def put(self, request, pk):
        league = self.get_object(pk)
        data = JSONParser().parse(request)
        serializer = LeagueSerializer(league, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        league = self.get_object(pk)
        league.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
