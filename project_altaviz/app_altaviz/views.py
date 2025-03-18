from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from app_bank.models import *
from app_bank.serializers import *
from app_location.models import Location
from app_users.serializers import UserReadHandlersSerializer
from .serializers import *
from django.contrib.auth import authenticate, login, logout, get_user_model
User = get_user_model()

# Create your views here.
@api_view(['GET'])
def home(request):
    return Response({"home": "welcome home from django server. This information is from the backend server"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def placeholder(request):
    return Response({"placeholder": "This is a placeholder API endpoint."}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllAccounts(request):
    users = User.objects.filter(is_superuser=False)
    usersSerializer = UserReadHandlersSerializer(users, many=True).data
    return Response(usersSerializer, status=status.HTTP_200_OK)

@api_view(['GET'])
def versionNumber(request):
    versionDict = {'version': 'v20250318.2331'}
    print("versionDict: ", versionDict)
    return Response(versionDict, status=status.HTTP_200_OK)
