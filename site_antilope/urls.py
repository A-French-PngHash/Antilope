from django.urls import  path
from .views import api_create_user, api_get_tiles_data, api_upload_gpx, index, main

urlpatterns = [
    path("", index, name = "index"),
    path("home", main, name= "home"),
    path("users", api_create_user, name="create_user"),
    path("tile", api_get_tiles_data, name="get_tiles"),
    path("gpx", api_upload_gpx, name="upload_gpx")
]