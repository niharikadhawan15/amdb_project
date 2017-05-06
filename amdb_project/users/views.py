# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from users.models import Users
from rest_framework.decorators import api_view
from datetime import datetime
from rest_framework.response import Response
from users.serializers import UserSerializer,MovieSerializer,ReviewSerializer
from users.models import AccessToken
from users.models import Movie,Genres,Movie_Genre,Review
from django.contrib.auth.hashers import make_password,check_password
import json

@api_view(["POST"])
def user_create(request):
    name=request.data['name']
    username=request.data['username']
    password=request.data['password']
    short_bio=request.data['short_bio']
    email=request.data['email']
    location=request.data['location']


# To make sure the name field is present and is not an empty string
    if name is None or len(name)<1:
        # If fields are invalid, the api responds with an appropriate error message
        return Response({'error_message':'name should not be empty'},status=400)

# To make sure the password field is present and is at least 6 characters long
    if password is None or len(password)<6:
        # If fields are invalid, the api responds with an appropriate error message
        return Response({'error_message': "Password field has to be atleast 6 characters long"},status=400)

    if location is None or len(location) < 1:
        # If fields are invalid, the api responds with an appropriate error message
        return Response({'error_message': 'please enter your location'}, status=400)

# TO make sure the username field is present and is unique
    does_username_exist=Users.objects.filter(username=username)
    print HttpResponse(111)

   # If fields are invalid, the api responds with an appropriate error message
    if len(does_username_exist)>0:
        return Response({"error_message": "username already exits !! Please choose a unique username"}, status=400)


# create a new record in the database for the user when the validations are met
    new_user=Users.objects.create(name=name,password=make_password(password),short_bio=short_bio,username=username,email=email,location=location)
    new_user.save()
    print does_username_exist
    return Response({'id':new_user.id,'name':new_user.name,'username':new_user.username,'short_bio':new_user.short_bio,'email':new_user.email,'location':new_user.location},status=200)


