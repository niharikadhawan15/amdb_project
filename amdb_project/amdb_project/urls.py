"""amdb_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from users.views import user_create,get_user,login,create_movie ,movie_list,movie_review,user_logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'user/create',user_create),
    url(r'user/',get_user),
    url(r'login',login),
    url(r'^create/movie',create_movie),
    url(r'^movie/list',movie_list),
    url(r'^movie/review',movie_review),
    url(r'^logout',user_logout)
]
