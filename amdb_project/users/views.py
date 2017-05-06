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

# This function checks if the user is logged in through a valid access token.
@api_view(['GET'])
def check_token(request):
    access_token = request.META['HTTP_TOKEN']
    token_exists=AccessToken.objects.filter(access_token=access_token,is_valid=True).first()

    if token_exists:
        current_user = token_exists.user
        return current_user
    else:
         return None


@api_view(['POST'])
def create_movie(request):
    # It checks whether the user is logged in
    current_user = check_token(request)
    new_genre = "comedy"
    genre=Genres.objects.create(name=new_genre)
    genre.save()

    if current_user:
        try:
            if 'name' in request.data:
                name = request.data['name']
            else:
                return Response({'error_message ': 'Please enter name of the movie. Movie name is not provided.'},status=200)

            if 'duration_in_minutes' in request.data:
                duration_in_minutes = int(request.data['duration_in_minutes'])
            else:
                return Response({'error_message':'The duration of the movie is not provided. Please provide it.'},status=200)

            if 'release_date' in request.data:
                release_date = datetime.strptime(request.data['release_date'], '%Y-%m-%d')
            else:
                return Response({'error_message':'The release date of the movie is not provided. Please provide it'},status=200)

            if 'censor_board_rating' in request.data:
                censor_board_rating = request.data['censor_board_rating']
            else:
                return Response({'error_message': 'The censor-board rating of the movie is not provided. Please provide it'},status=200)

            if 'poster_picture_url' in request.data:
                poster_picture_url = request.data['poster_picture_url']
            else:
                return Response({'error_message': 'The URL of the poster of the movie is not provided.Please provide it'},status=200)

            if 'genre_name' in request.data:
                genre_names = request.data['genre_name']
            else:
                return Response({'error_message': 'No genre is provided for the film. Please provide it'},status=200)

        except ValueError:
            return Response({'error_message': 'Please fill all the fields!!!'},status=200)


        #This make sure the name field is not an empty string.
        if len(name) == 0:
            return Response({'error_message': 'Name cannot be empty'},status=200)

        # This makes sure duration_in_minutes is present and is not zero or negative.
        if duration_in_minutes < 1:
            return Response({"error_message": "Invalid duration. The duration of the movie cannot be zero or negative."},status=200)

        movie_exist = Movie.objects.filter(name=name).first()

        if movie_exist:
            return Response({'error_message': 'Movie is already present'},status=200)

        genre_names = genre_names.split(',')

        genres = []

        for i in genre_names:
            genre_given = Genres.objects.filter(name=i).first()

            if genre_given:
                genres.append(genre_given)

            else:
                return Response({"error_message": "Invalid Genre !"},status=200)

        if len(genres) < 1:
            return Response({"error_message": "The movie must have atleast one genre"},status=200)

        # This creates a new movie record
        new_movie = Movie.objects.create(name=name, duration_in_minutes=duration_in_minutes, release_date=release_date, censor_board_rating=censor_board_rating, poster_picture_url=poster_picture_url, user_id=current_user)
        new_movie.save()

        for genre in genres:
            Movie_Genre.objects.create(movie=new_movie, genre=genre)
        return Response(MovieSerializer(instance=new_movie).data,status=200)

    # If the user is not logged in, the api respond with an error message.
    return Response({"error_message": "You are not authorized to perform this action ..... Please login first!!!"},status=400)


@api_view(['GET'])
def movie_list(request):
    movie_id = []
    # The api uses the value of query parameter q to find movies of the same name.
    if 'q' in request.query_params:
        #The api method uses the value of query parameter to find movies of the same name present in the database.
        query = request.query_params['q']

        #name_icontains manages full match, partial match and case sensitive matches.
        movie = Movie.objects.filter(name__icontains=query)

        if movie:
            for i in range(len(movie)):
                movie_id.append(movie[i].id)

        genre_query = query
        genre_id = Genres.objects.filter(name__icontains=genre_query).first()
        movie_genre = Movie_Genre.objects.filter(genre=genre_id)

        for i in range(len(movie_genre)):
            movie_id.append(Movie.objects.filter(id=movie_genre[i].movie_id).first().id)

        movie = set(movie_id)
        movie_id = list(movie)

        if len(movie_id):
            for i in range(len(movie_id)):
                movie_id[i] = MovieSerializer(instance=Movie.objects.filter(id=movie_id[i]).first()).data
            return Response(movie_id, status=200)

        return Response({'error_message ':'No such Movies found .....Please try again!!!'}, status=400)

    #If the query parameter is not found, the api fetches all the movies present in the database
    elif len(['q']) in request.query_params==0:
        movies = Movie.objects.all()
        return Response(MovieSerializer(instance=movies, many=True).data, status=200)

    else:
        print (111)
        return HttpResponse(json.dumps(movie_id))


@api_view(['POST'])
def movie_review(request):
    # It checks if the user is logged in through a valid access token or not...
    current_user = check_token(request)

    # to check if the user is logged in
    if current_user:
        try:

            if 'movie_name' in request.data:
                name = request.data['movie_name']
            else:
                return Response({'error_message': 'Movie name not provided.Please provide it.'},status=200)

            if 'rating' in request.data:
                user_rating = request.data['rating']
            else:
                return Response({'error_message':'Rating field is empty. Please provide rating.'},status=200)

            if 'review' in request.data:
                if len(request.data['review']):
                    review = request.data['review']
                else:
                    return Response({'error_message':'Review is not provided.Kindly provide it'},status=200)

            else:
                return Response({'error_message': 'Review is not provided.Kindly provide it'},status=200)

        except ValueError:

            return Response({'error_message':'Invalid Request.Make sure all fields are filled'},status=200)

        if len(name) == 0:
            return Response({'error_message':'Name cannot be empty.Please provide it...'},status=200)

        movie_id = Movie.objects.filter(name=name).first()

        if movie_id:
            try:
                #It makes sure that the rating is a valid decimal less than 5.
                user_rating = float(user_rating)
            except ValueError:
                return Response({"error_message": "rating must be a Decimal munber that lies between 0 and 5."}, status=400)

            if 0>user_rating or user_rating>5:
                return Response({'error_message': 'The movie rating should be less than 5'}, status=200)

            #This makes sure that the user has not already reviewed the movie
            already_reviewed = Review.objects.filter(user=current_user, movie=movie_id).first()

            if already_reviewed:
                return Response({'error_message': 'This movie is already reviewed by you...'}, status=200)

            else:

                #If all validations are met then a new review for the movie is created.
                movie_review = Review.objects.create(movie=movie_id, rating= user_rating, review=review, user=current_user)
                movie_review.save()
                overall_rating=0

                #It updates the overall_rating column with the average rating after the new review is created.
                average_rating = Review.objects.filter(movie=movie_id)

                for i in average_rating:
                    overall_rating += i.rating

                overall_rating /= len(average_rating)

                Movie.objects.filter(id=movie_id.id).update(overall_rating=overall_rating)
                return Response({"success": "The movie has been reviewed"}, status=200)

        else:
            return Response({'error_description ': 'No such movie is in our records '}, status=200)

    #If the user is not logged in, the api responds with a status code 400 and an appropriate message.
    return Response({'error_description ': 'You are not authorized to perform this action ..... Please login first!!!'}, status=400)




@api_view(['POST'])
def user_logout (request):
    token = request.META['HTTP_TOKEN']

    access_token = AccessToken.objects.filter(access_token=token, is_valid=True).first()

    if access_token:
        # It sets the is_valid to the value False(0).
        access_token.is_valid=False
        access_token.save()
        return Response({'message ': 'User logged out successfully'}, status=200)

    #If the access token is found then it replies with an appropriate error message .
    return Response({'error_message ': 'The user could not be found'}, status=400)
