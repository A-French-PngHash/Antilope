from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer, TileDataRequestSerializer, UploadActivityForm
from .services.db import *
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'index.html', context=locals())

@login_required
def main(request):
    return render(request, 'home.html', context = locals())

@api_view(['GET'])
def user_detail(request, primary):
    # primary -> id of the user
    try:
        user = User.objects.get(id=primary)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def api_create_user(request):    
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({"id" : user.id})

@api_view(['GET'])
def api_get_tiles_data(request):
    serializer = TileDataRequestSerializer(data= request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    tiles = get_tile_data_inside(data["topleft"], data["bottomright"], data["group"])
    return Response(tiles)

@api_view(['POST'])
def api_upload_gpx(request):
    form = UploadActivityForm(request.POST, request.FILES)
    if form.is_valid():
        print(request.FILES["gpx_file"])
        return Response({})
    else:
        return  Response(status=status.HTTP_400_BAD_REQUEST)