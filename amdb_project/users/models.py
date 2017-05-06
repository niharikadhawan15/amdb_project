# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

# Create your models here.

class Users(models.Model):

    name=models.CharField(max_length=200,null=False,blank=False)
    username=models.CharField(max_length=100,unique=True)
    password=models.CharField(max_length=200)
    short_bio=models.CharField(max_length=240)
    email=models.EmailField(max_length=200,null=True)
    location=models.CharField(max_length=200,default='india')
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)


class AccessToken(models.Model):
    user=models.ForeignKey(Users)
    access_token=models.CharField(max_length=255)
    last_request_on=models.DateField(auto_now=True)
    is_valid=models.BooleanField(default=True)

    def create_token(self):
        self.access_token=uuid.uuid4()


class Movie(models.Model):
    name=models.CharField(max_length=255)
    duration_in_minutes=models.IntegerField()
    release_date=models.DateTimeField()
    overall_rating=models.DecimalField(decimal_places=2,max_digits=4,default=0)
    censor_board_rating=models.CharField(max_length=5)
    poster_picture_url=models.CharField(max_length=255)
    user_id=models.ForeignKey(Users)


class Genres(models.Model):
    name=models.CharField(max_length=255)


class Movie_Genre(models.Model):
    movie=models.ForeignKey(Movie)
    genre=models.ForeignKey(Genres)


class Review(models.Model):
    movie = models.ForeignKey(Movie)
    user = models.ForeignKey(Users)
    rating = models.DecimalField(decimal_places=2, max_digits=3, default=0)
    review = models.CharField(max_length=300)