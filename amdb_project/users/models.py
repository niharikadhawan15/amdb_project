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

