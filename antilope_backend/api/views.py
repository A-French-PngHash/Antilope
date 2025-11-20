from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer

# Create your views here.
# Logic for api endpoint

@api_view(['GET'])
def get_user(request):
    #print(request.)
    users = User.objects.all()
    print(users)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
    return Response(
        UserSerializer({'name' : "pedro","surname":"alonzo", "age" : 23}).data)

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
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,  status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)