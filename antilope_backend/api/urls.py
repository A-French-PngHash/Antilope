from django.urls import  path
from .views import *

urlpatterns = [

    path("users/create", create_user, name="create_user"),
    path("users/<int:primary>", user_detail, name="user_detail")
]