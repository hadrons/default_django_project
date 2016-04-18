# coding: utf-8

from rest_framework import serializers
from .models import Person


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['id','email','name','cellular','gender','groups',]


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            if Person.objects.filter(email=email).exists():
                user = Person.objects.get(email=email)
            
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)
                attrs['user'] = user

                return attrs
            else:
                msg = 'Invalid Credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = "Invalid Parameters."
            raise serializers.ValidationError(msg)
