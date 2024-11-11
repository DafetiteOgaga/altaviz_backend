from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from app_bank.models import State
from app_location.models import Location
from app_users.serializers import UserUpdateDetailsSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db import transaction
from rest_framework.pagination import PageNumberPagination

# Create your views here.
@api_view(['GET',])
def branches(request, pk=None):
	print(f'branch payload: {request.data}')
	if pk:
		bankBranches = Branch.objects.filter(bank=request.data['branch'])
		print(f'bank branches: {bankBranches}')
		serializer = BranchSerializer(bankBranches, many=True)
		print(f'bank branch object list serialized: {serializer.data}')
		return Response(serializer.data, status=status.HTTP_200_OK)
	branches = Branch.objects.all()
	print(f'branch object list: {branches}')
	serializer = BranchSerializer(branches, many=True)
	print(f'branch object list serialized: {serializer.data}')
	return Response(serializer.data, status=status.HTTP_200_OK)
