from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from app_location.serializers import LocationSerializer, LocationNoRegionSerializer
from django.db.models import Prefetch
from app_custodian.serializers import BranchListSerializer
from app_users.models import Region
from app_users.serializers import RegionAloneSerializer

# Create your views here.
@api_view(['GET'])
def statesView(request):
    regions = Region.objects.prefetch_related(
        'regionstates',                           # Reverse ForeignKey: Region to State
        'regionstates__statelocations',          # region to location
    )
    serializedRegions = RegionAloneSerializer(instance=regions, many=True).data
    for rIndex, region in enumerate(regions):
        print(f'{region.name}')
        states = region.regionstates.all()
        serializedStates = StateNoRegionSerializer(instance=states, many=True).data
        serializedRegions[rIndex]['states'] = serializedStates
        for sIndex, state in enumerate(states):
            print(f'    {state.name}')
            locations = state.statelocations.all()
            serializedLocations = LocationNoRegionSerializer(instance=locations, many=True).data
            serializedRegions[rIndex]['states'][sIndex]['locations'] = serializedLocations
            print(f'        locations: {[location.location for location in locations]}')
            # for location in locations:
            #     print(f'        {location.location}')
    return Response(serializedRegions, status=status.HTTP_200_OK)
    # return Response({'good'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def banksView(request):
    regions = Region.objects.prefetch_related(
        'regionstates',                           # Reverse ForeignKey: Region to State
        'regionstates__banksList',                # ManyToMany: State to Bank
        'regionstates__banksList__banklocations', # Forward ForeignKey: Bank to Location
        'regionstates__banksList__banklocations__locationbranches'  # Reverse ForeignKey: Location to Branch
    )
    # regions = Region.objects.all().prefetch_related('regionstates')
    serializedRegions = RegionAloneSerializer(instance=regions, many=True).data
    for rIndex, region in enumerate(regions):
        print(f'region: {region.name}')
        states = region.regionstates.all()
        serializedStates = StateNoRegionSerializer(instance=states, many=True).data
        serializedRegions[rIndex]['states'] = serializedStates
        # print(f'    states: {[region.name for region in states]}')
        for sIndex, state in enumerate(states):
            banks = state.banksList.all()
            print(f'    state: {state.name}')
            seriaizedBanks = BankSerializer(instance=banks, many=True).data
            serializedRegions[rIndex]['states'][sIndex]['banks'] = seriaizedBanks
            # print(f'    {state}: banks: {[bank.name for bank in banks]}')
            for bIndex, bank in enumerate(banks):
                print(f'        bank: {bank.name}')
                locations = bank.banklocations.all()
                serializedLocations = LocationNoRegionSerializer(instance=locations, many=True).data
                serializedRegions[rIndex]['states'][sIndex]['banks'][bIndex]['locations'] = serializedLocations
                # print(f'        {bank}: {[location.location for location in locations]}')
                for lIndex, location in enumerate(locations):
                    print(f'            location: {location}')
                    # print(f'            {[location.location for location in locations]}')
                    branches = location.locationbranches.all()
                    print(f'                branches: {[branch.name for branch in branches]}')
                    serializedBranches = BranchListSerializer(instance=branches, many=True).data
                    serializedRegions[rIndex]['states'][sIndex]['banks'][bIndex]['locations'][lIndex]['branches'] = serializedBranches
                    # for branch in branches:
                    #     print(f'                {branch.name}')

    return Response(serializedRegions, status=status.HTTP_200_OK)
    # return Response({'good'}, status=status.HTTP_200_OK)
