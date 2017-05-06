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


@api_view(['GET'])
def get_user(request):
    #api check for a query parameter i.e.id.
    if 'user_id' in request.query_params:
        #If the query parameter is found ,the api fetches the user record else it fetches the record for all the users
        user=Users.objects.filter(id=request.query_params['user_id'])
        if len(user) > 0:
           return Response(UserSerializer(instance=user[0]).data, status=200)
        else:
            return Response({"error_message": "User not found!!"}, status=200)
    else:
           users = Users.objects.all()
           return Response(UserSerializer(instance=users,many=True).data, status=200)

@api_view(['POST'])
def login(request):
    username=None
    password=None


    if 'username' in request.data:
        username=request.data['username']

    if 'password' in request.data:
        password=request.data['password']

    #It check if username and password are present in the request or not and return an appropriate error message if the fields are not present.
    if not username or not password:
         return Response({"error_message": "Username or password not provided."}, status=200)

    user = Users.objects.filter(username=username).first()

    if user:
        # It checks for the password
        if not check_password(password, user.password):
            return Response({"error_message": "Username and password combination is not correct."}, status=200)
        else:
            #If the user is found the api creates an access token.
            token = AccessToken(user=user)
            token.create_token()
            print token.access_token
            token.save()

            return Response({"token": token.access_token}, status=200)
    else:
             return Response({"error_message": "Username or password is invalid."}, status=200)

