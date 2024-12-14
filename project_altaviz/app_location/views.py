from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app_custodian.serializers import BranchListSerializer
from .models import *
from .serializers import *
from app_users.models import Region, User
from app_bank.models import State

# Create your views here.
@api_view(['GET',])
def locations(request):
    locations = Location.objects.all()
    print(f'location object list: {locations}')
    serializer = LocationSerializer(locations, many=True)
    # print(f'Location object list serialized: {serializer.data}')
    [print(i, '\n') for i in serializer.data]
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def bankRegionLocations(request, pk=None, state=None, bank=None):
    print(f'pk: {pk}')
    print(f'state: {state}')
    print(f'bank: {bank}')
    locationList = []
    region = Region.objects.prefetch_related('regionstates__banksList__banklocations__locationbranches').get(pk=pk)
    print(f'region: {region.name}')
    states = [state for state in region.regionstates.all()]
    for stateName in states:
        print(f'    ##### state match: {stateName.name == state}')
        if stateName.name != state: continue
        print(f'    {stateName}')
        stateEntry = {
            'state': stateName.name,
            'banks': []
        }
        banks = [bank for bank in stateName.banksList.all()]
        for bankName in banks:
            print(f'        ##### bank match: {bankName.name == bank}')
            if bankName.name != bank: continue
            print(f'        {bankName}')
            locations = [location for location in bankName.banklocations.all()]
            bankEntry = {
                'bank': bankName.name,
                'locations': []
            }
            # bankEntry['locations'] = LocationAloneSerializer(instance=locations, many=True).data
            for location in locations:
                print(f'            {location}')
                branches = [branch for branch in location.locationbranches.all()]
                print(f'                branches: {[branch.name for branch in branches]}')
                location_data = {
                    'location': location.location,
                    'id': location.id,
                    'branches': BranchListSerializer(instance=branches, many=True).data
                }
                bankEntry['locations'].append(location_data)
            stateEntry['banks'].append(bankEntry)
            if bankName.name == bank: break
        locationList.append(stateEntry)
        if stateName.name == state: break
    return Response(locationList, status=status.HTTP_200_OK)

@api_view(['GET',])
def RegionLocations(request, pk=None, state=None):
    print(f'pk: {pk}')
    print(f'state: {state}')
    # user = User.objects.get(pk=pk)
    # print(f'user obj and role: {user} is a {user.role} expert')
    locationList = []
    region = Region.objects.prefetch_related('regionstates__statelocations').get(pk=pk)
    print(f'region: {region.name}')
    states = [state for state in region.regionstates.all()]
    for stateName in states:
        if stateName.name != state: continue
        print(f'    {stateName}')
        locations = [location for location in stateName.statelocations.all()]
        stateEntry = {
            'state': stateName.name,
            'locations': LocationAloneSerializer(instance=locations, many=True).data
        }
        print(f'        locations: {[location.location for location in locations]}')
        locationList.append(stateEntry)
        if stateName.name == state: break
    return Response(locationList, status=status.HTTP_200_OK)
