from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET', 'POST'])
def home(request):
    return Response({"home": "welcome home from django server. This information is from the backend server"}, status=status.HTTP_200_OK)

# @api_view(['GET', 'POST'])
# def menu_list(request):
#     if request.method == 'GET':
#         menus = Menu.objects.all()
#         serializer = MenuSerializer(menus, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = MenuSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def menu_detail(request, pk):
#     try:
#         menu = Menu.objects.get(pk=pk)
#     except Menu.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = MenuSerializer(menu)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = MenuSerializer(menu, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         menu.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# Create your views here.
