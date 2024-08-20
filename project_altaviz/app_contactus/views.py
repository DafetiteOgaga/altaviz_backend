from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST'])
def contact_us(request):
    # if request.method == 'GET':
        # contacts = ContactUser.objects.all()
        # serializer = ContactUserSerializer(contacts, many=True)
        # return Response(serializer.data)
    if request.method == 'POST':
        print('payload:', request.data)
        # return Response({
        #     'message': 'success. payload recieved',
        #     'yes': 'done.'
        #     })
        serializer = ContactUserSerializer(data=request.data)
        print(f'serializer: {serializer}')
        print(f'serializer.is_valid: {serializer.is_valid()}')
        print(f'serializer.errors: {serializer.errors}')
        if serializer.is_valid():
            serializer.save()
            
            contacts = ContactUs.objects.all()
            print('###################### content (post) ##########################')
            [print(f'{i+1}. {obj.message} by: {obj.name} with email: {obj.email}') for i, obj, in enumerate(contacts)]
            print('###################### end content (post) ##########################')
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    contacts = ContactUs.objects.all()
    print('###################### content (get) ##########################')
    [print(f'{i+1}. {obj.message} by: {obj.name} with email: {obj.email}') for i, obj, in enumerate(contacts)]
    print('###################### end content (get) ##########################')
    serializer = ContactUserSerializer(contacts, many=True)
    return Response(serializer.data)
    # return Response({"home": "welcome home from django server. This information is from the backend server"}, status=status.HTTP_200_OK)
