# coding: utf-8

from random import randint
from django.shortcuts import render
from django.core.urlresolvers import reverse as r
from django.utils.encoding import smart_str


from api.views import PermissionTokenLoginRequiredMixin
from people.serializer import AuthTokenSerializer


from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser,
                      parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    model = Token

    def post(self, request, backend='auth'):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'auth-token': token.key})
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)