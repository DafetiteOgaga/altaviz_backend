from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_users.models import User
from .models import Deliveries
from .serializers import ReadUserDeliveriresSerializer

# Create your views here.
@api_view(['GET'])
def deliveries(request, pk=None):
    print(f'pk: {pk}')
    user = User.objects.get(pk=pk)
    print(f'user: {user}')
    deliveries = Deliveries.objects.filter(user=user).first()
    print(f'deliveries: {deliveries}')
    if deliveries == None:
        print(f'No deliveries found for: {user.first_name}.')
        return Response({'msg': f'No deliveries found for: {user.first_name}.'}, status=status.HTTP_200_OK)
    deliverySerializer = ReadUserDeliveriresSerializer(instance=deliveries).data
    print(f'deliverySerializer data: {deliverySerializer}')
    return Response(deliverySerializer, status=status.HTTP_200_OK)
