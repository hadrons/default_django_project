#coding: utf-8

from api.views import PermissionTokenLoginRequiredMixin
from people.models import Person
from people.serializer import PersonSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PersonViewSet(APIView):
    serializer_class = PersonSerializer

    def get(self, request, format=None):
        serializer = self.serializer_class(Person.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"409 Conflict"}, status=status.HTTP_409_CONFLICT)

class PersonUpdateView(APIView):
    
    def get(self, request, pk, format=None):
        user = Person.objects.get(pk=pk)
        serializer = PersonSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk=None):
        user = Person.objects.get(pk=pk)
        serializer = PersonSerializer(data=request.data,instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)