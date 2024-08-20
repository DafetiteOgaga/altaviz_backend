from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
@api_view(['get'])
def departments(request):
    users = Department.objects.all()
    serializer = DepartmentSerializer(users, many=True)
    return Response(serializer.data)