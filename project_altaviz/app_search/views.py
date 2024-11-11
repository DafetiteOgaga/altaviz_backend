from django.shortcuts import render
from rest_framework.decorators import api_view
from app_bank.models import Bank, State
from app_custodian.models import Branch
from app_location.models import Location
from app_fault.models import Fault
from app_fault.serializers import FaultReadSerializer
from app_inventory.models import RequestPart, RequestComponent
from app_inventory.serializers import RequestFaultComponentReadSerializer, RequestFaultPartReadSerializer
from app_users.models import User
from django.db.models import Q, QuerySet
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# Create your views here.
@api_view(['GET'])
def faultSearch(request):
	print(f'faultSearch payload: {request.query_params}')
	# Get the search term from the query params (single input field)
	search_term = None if request.query_params.get('search') == '' else request.query_params.get('search')
	confirm_resolve = None if request.query_params.get('confirm_resolve') == '' else request.query_params.get('confirm_resolve')
	verify_resolve = None if request.query_params.get('verify_resolve') == '' else request.query_params.get('verify_resolve')
	approved = None if request.query_params.get('approved') == '' else request.query_params.get('approved')
	rejected = None if request.query_params.get('rejected') == '' else request.query_params.get('rejected')
	start_date = None if request.query_params.get('start_date') == '' else request.query_params.get('start_date')
	end_date = None if request.query_params.get('end_date') == '' else request.query_params.get('end_date')
	department = None if request.query_params.get('department') == '' else request.query_params.get('department')

	print(f'Search term: {search_term}')
	print(f'confirm_resolve: {confirm_resolve}')
	print(f'verify_resolve: {verify_resolve}')
	print(f'approved: {approved}')
	print(f'rejected: {rejected}')
	print(f'start_date: {start_date}')
	print(f'end_date: {end_date}')
	print(f'department: {department}')
	try:
		search_term = int(search_term)
	except Exception as e:
		pass
	filteredFaults = []
	dataTypeIsInt = type(search_term) == int
	if type(search_term) == int:
		print(f'search_term: {search_term} is an integer')
	else:
		print(f'search_term: {search_term} is not an integer')
	print(f'dataType: {dataTypeIsInt}')

	if search_term:
		if dataTypeIsInt:
			print(f'search_term: {search_term}')
			filteredFaults = Fault.objects.select_related('title', 'location', 'assigned_to', 'supervised_by', 'managed_by').prefetch_related('partfault', 'componentfault').filter(id=search_term)
			print(f'filtered faults: {filteredFaults}')
		else:
			if department == 'supervisor' or department == 'help-desk':
				# Get all Fault records
				# faults = Fault.objects.prefetch_related('partfault', 'componentfault').all()
				faults = Fault.objects.select_related('title', 'location', 'assigned_to', 'supervised_by', 'managed_by').prefetch_related('partfault', 'componentfault').all()

				print(f'all faults total: {len(faults)}')
				# Apply the search across multiple fields if search_term is provided
				print(f'supervisor access: {department == "supervisor"}')
				if department == 'supervisor':
					print(f'accessing supervisor field ...')
					faults = faults.filter(
						Q(title__name__icontains=search_term) |
						Q(location__location__icontains=search_term) |
						Q(assigned_to__email__icontains=search_term) |
						Q(assigned_to__first_name__icontains=search_term) |
						Q(assigned_to__middle_name__icontains=search_term) |
						Q(assigned_to__last_name__icontains=search_term) |
						Q(assigned_to__role__icontains=search_term) |
						Q(assigned_to__region__name__icontains=search_term) |
						Q(assigned_to__state__name__icontains=search_term) |
						Q(assigned_to__username__icontains=search_term) |

						Q(managed_by__username__icontains=search_term) |
						Q(managed_by__email__icontains=search_term) |
						Q(managed_by__first_name__icontains=search_term) |
						Q(managed_by__middle_name__icontains=search_term) |
						Q(managed_by__last_name__icontains=search_term) |
						Q(managed_by__role__icontains=search_term) |
						Q(managed_by__region__name__icontains=search_term) |
						Q(managed_by__state__name__icontains=search_term) |
						Q(managed_by__username__icontains=search_term) |

						Q(supervised_by__username__icontains=search_term) |
						Q(supervised_by__email__icontains=search_term) |
						Q(supervised_by__first_name__icontains=search_term) |
						Q(supervised_by__middle_name__icontains=search_term) |
						Q(supervised_by__last_name__icontains=search_term) |
						Q(supervised_by__role__icontains=search_term) |
						Q(supervised_by__region__name__icontains=search_term) |
						Q(supervised_by__state__name__icontains=search_term) |
						Q(supervised_by__username__icontains=search_term)
					)
					print(f'supervisor searched faults total: {len(faults)}')
				else:
					faults = faults.filter(
						Q(title__name__icontains=search_term) |
						Q(location__location__icontains=search_term) |
						Q(assigned_to__email__icontains=search_term) |
						Q(assigned_to__first_name__icontains=search_term) |
						Q(assigned_to__middle_name__icontains=search_term) |
						Q(assigned_to__last_name__icontains=search_term) |
						Q(assigned_to__role__icontains=search_term) |
						Q(assigned_to__region__name__icontains=search_term) |
						Q(assigned_to__state__name__icontains=search_term) |
						Q(assigned_to__username__icontains=search_term) |

						Q(managed_by__username__icontains=search_term) |
						Q(managed_by__email__icontains=search_term) |
						Q(managed_by__first_name__icontains=search_term) |
						Q(managed_by__middle_name__icontains=search_term) |
						Q(managed_by__last_name__icontains=search_term) |
						Q(managed_by__role__icontains=search_term) |
						Q(managed_by__region__name__icontains=search_term) |
						Q(managed_by__state__name__icontains=search_term) |
						Q(managed_by__username__icontains=search_term)
					)
					print(f'helpdesk level searched faults total: {len(faults)}')

				# Filter for boolean values
				if confirm_resolve is not None:
					faults = faults.filter(confirm_resolve=confirm_resolve == 'true')
					print(f'confirm_resolve searched faults total: {len(faults)}')

				if verify_resolve is not None:
					faults = faults.filter(verify_resolve=verify_resolve == 'true', confirm_resolve=False)
					print(f'verify_resolve searched faults total: {len(faults)}')

				# Filter for date ranges (created_at)
				if start_date:
					start_from_date = parse_datetime(start_date)
					start_date_aware = timezone.make_aware(start_from_date, timezone.get_default_timezone())
					if start_from_date:
						faults = faults.filter(created_at__gte=start_date_aware)
						print(f'start_date searched faults total: {len(faults)}')

				if end_date:
					end_to_date = parse_datetime(end_date)
					end_date_aware = timezone.make_aware(end_to_date, timezone.get_default_timezone())
					if end_to_date:
						faults = faults.filter(created_at__lte=end_date_aware)
						print(f'end_date searched faults total: {len(faults)}')

				filteredFaults = faults

			elif department == 'human-resource':
				# Get all requests records
				allPartsRequests = RequestPart.objects.select_related('name', 'fault', 'user', 'approved_by').all()
				allComponentsRequests = RequestComponent.objects.select_related('name', 'fault', 'user', 'approved_by').all()

				print(f'allPartsRequests total: {len(allPartsRequests)}')
				print(f'allComponentsRequests total: {len(allComponentsRequests)}')

				# Apply the search across multiple fields if search_term is provided
				print(f'hr access: {department == "human-resource"}')
				allPartsRequests = allPartsRequests.filter(
					Q(name__name__icontains=search_term) |
					Q(fault__title__name__icontains=search_term) |
					Q(user__email__icontains=search_term) |
					Q(user__first_name__icontains=search_term) |
					Q(user__middle_name__icontains=search_term) |
					Q(user__last_name__icontains=search_term) |
					Q(user__role__icontains=search_term) |
					Q(user__region__name__icontains=search_term) |
					Q(user__state__name__icontains=search_term) |
					Q(user__username__icontains=search_term) |

					Q(approved_by__username__icontains=search_term) |
					Q(approved_by__email__icontains=search_term) |
					Q(approved_by__first_name__icontains=search_term) |
					Q(approved_by__middle_name__icontains=search_term) |
					Q(approved_by__last_name__icontains=search_term) |
					Q(approved_by__role__icontains=search_term) |
					Q(approved_by__region__name__icontains=search_term) |
					Q(approved_by__state__name__icontains=search_term) |
					Q(approved_by__username__icontains=search_term)
				)
				print(f'searched allPartsRequests total: {len(allPartsRequests)}')

				allComponentsRequests = allComponentsRequests.filter(
					Q(name__name__icontains=search_term) |
					Q(fault__title__name__icontains=search_term) |
					Q(user__email__icontains=search_term) |
					Q(user__first_name__icontains=search_term) |
					Q(user__middle_name__icontains=search_term) |
					Q(user__last_name__icontains=search_term) |
					Q(user__role__icontains=search_term) |
					Q(user__region__name__icontains=search_term) |
					Q(user__state__name__icontains=search_term) |
					Q(user__username__icontains=search_term) |

					Q(approved_by__username__icontains=search_term) |
					Q(approved_by__email__icontains=search_term) |
					Q(approved_by__first_name__icontains=search_term) |
					Q(approved_by__middle_name__icontains=search_term) |
					Q(approved_by__last_name__icontains=search_term) |
					Q(approved_by__role__icontains=search_term) |
					Q(approved_by__region__name__icontains=search_term) |
					Q(approved_by__state__name__icontains=search_term) |
					Q(approved_by__username__icontains=search_term)
				)
				print(f'searched allComponentsRequests total: {len(allComponentsRequests)}')
				################################################
				# Filter for boolean values
				if approved is not None:
					allPartsRequests = allPartsRequests.filter(approved=approved == 'true')
					allComponentsRequests = allComponentsRequests.filter(approved=approved == 'true')
					print(f'approved searched allPartsRequests total: {len(allPartsRequests)}')
					print(f'approved searched allComponentsRequests total: {len(allComponentsRequests)}')

				if rejected is not None:
					allPartsRequests = allPartsRequests.filter(rejected=rejected == 'true')
					allComponentsRequests = allComponentsRequests.filter(rejected=rejected == 'true')
					print(f'rejected searched allPartsRequests total: {len(allPartsRequests)}')
					print(f'rejected searched allComponentsRequests total: {len(allComponentsRequests)}')
				
				# Filter for date ranges (created_at)
				if start_date:
					start_from_date = parse_datetime(start_date)
					start_date_aware = timezone.make_aware(start_from_date, timezone.get_default_timezone())
					if start_from_date:
						allPartsRequests = allPartsRequests.filter(requested_at__gte=start_date_aware)
						allComponentsRequests = allComponentsRequests.filter(requested_at__gte=start_date_aware)
						print(f'start_date searched allPartsRequests total: {len(allPartsRequests)}')
						print(f'start_date searched allComponentsRequests total: {len(allComponentsRequests)}')

				if end_date:
					end_to_date = parse_datetime(end_date)
					end_date_aware = timezone.make_aware(end_to_date, timezone.get_default_timezone())
					if end_to_date:
						allPartsRequests = allPartsRequests.filter(requested_at__lte=end_date_aware)
						allComponentsRequests = allComponentsRequests.filter(requested_at__lte=end_date_aware)
						print(f'end_date searched allPartsRequests total: {len(allPartsRequests)}')
						print(f'end_date searched allComponentsRequests total: {len(allComponentsRequests)}')
				################################################
				# processed search results
				processedResults = list(allPartsRequests) + list(allComponentsRequests)
				# fetch faults associated with each requests
				faultsOfProcessedResults = [request.fault for request in processedResults]
				# remove duplicate faults but not 'None' faults
				filteredFaults = []
				for fault in faultsOfProcessedResults:
					# consider developing a default faute template for 'None' faults
					if fault == None: continue
					if fault is None or fault not in filteredFaults:
						filteredFaults.append(fault)

				# Convert list back to QuerySet for pagination
				filteredFaults = Fault.objects.filter(id__in=[fault.id for fault in filteredFaults]).prefetch_related('partfault', 'componentfault')

		####################### repeated code #####################
		userPaginator = PageNumberPagination()
		if department == 'human-resource':
			userPaginator.page_size = 5  # Number of items per page
		else:
			userPaginator.page_size = 10  # Number of items per page
		paginated_fault = userPaginator.paginate_queryset(filteredFaults, request)
		# Serialize and return filtered data as JSON
		serializer = FaultReadSerializer(instance=paginated_fault, many=True)
		print()
		print(f'final total: {len(filteredFaults)}')
		serialized_data = serializer.data
		for (item, faultRequests) in zip(serialized_data, filteredFaults):
			print()
			print('############ item #####################')
			print(f'item: {item["id"]}')
			print(f'fault details: {item}')
			# item['custodianFirstName'] = engineer.first_name
			# print()
			faultCompRequest = faultRequests.componentfault.all()
			print(f'faultCompRequest: {faultCompRequest}')
			print(f'length of faultCompRequest: {len(faultCompRequest)}')
			# print(f'count faultCompRequest: {len(faultCompRequest)}')
			faultCompRequestSerializer = RequestFaultComponentReadSerializer(instance=faultCompRequest, many=True).data
			# if faultCompRequestSerializer: print(f'faultCompRequestSerializer: {faultCompRequestSerializer}')
			# item['requestStatus'] = True if faultCompRequestSerializer.data else False
			item['requestComponent'] = faultCompRequestSerializer if faultCompRequestSerializer else False
			print()
			faultPartRequest = faultRequests.partfault.all()
			print(f'faultPartRequest: {faultPartRequest}')
			print(f'length of faultPartRequest: {len(faultPartRequest)}')
			# print(f'count faultPartRequest: {len(faultPartRequest)}')
			faultPartRequestSerializer = RequestFaultPartReadSerializer(instance=faultPartRequest, many=True).data
			# if faultPartRequestSerializer: print(f'faultPartRequestSerializer: {faultPartRequestSerializer}')
			item['requestPart'] = faultPartRequestSerializer if (faultPartRequestSerializer or faultPartRequestSerializer) else False
			item['requestStatus'] = bool(faultCompRequestSerializer) or bool(faultPartRequestSerializer)
		print('##################### end search ###########################')
		####################### repeated code #####################
	return userPaginator.get_paginated_response(serialized_data)

@api_view(['GET'])
def requestSearch(request):
	print(f'request: {request}')
	print(f'requestSearch payload: {request.query_params}')
	# Get the search term from the query params (single input field)
	search_term = None if request.query_params.get('search') == '' else request.query_params.get('search')
	# confirm_resolve = None if request.query_params.get('confirm_resolve') == '' else request.query_params.get('confirm_resolve')
	# verify_resolve = None if request.query_params.get('verify_resolve') == '' else request.query_params.get('verify_resolve')
	approved = None if request.query_params.get('approved') == '' else request.query_params.get('approved')
	rejected = None if request.query_params.get('rejected') == '' else request.query_params.get('rejected')
	start_date = None if request.query_params.get('start_date') == '' else request.query_params.get('start_date')
	end_date = None if request.query_params.get('end_date') == '' else request.query_params.get('end_date')
	department = None if request.query_params.get('department') == '' else request.query_params.get('department')

	print(f'Search term: {search_term}')
	# print(f'confirm_resolve: {confirm_resolve}')
	# print(f'verify_resolve: {verify_resolve}')
	print(f'approved: {approved}')
	print(f'rejected: {rejected}')
	print(f'start_date: {start_date}')
	print(f'end_date: {end_date}')
	print(f'department: {department}')
	try:
		search_term = int(search_term)
	except Exception as e:
		pass
	filteredFaults = []
	dataTypeIsInt = type(search_term) == int
	if type(search_term) == int:
		print(f'search_term: {search_term} is an integer')
	else:
		print(f'search_term: {search_term} is not an integer')
	print(f'dataType: {dataTypeIsInt}')

	if search_term:
		if dataTypeIsInt:
			print(f'search_term: {search_term}')
			partsRequest = RequestPart.objects.filter(id=search_term)
			componentsRequest = RequestComponent.objects.filter(id=search_term)
			print(f'filtered partsRequest: {partsRequest}')
			print(f'filtered componentsRequest: {componentsRequest}')
			serializedPartRequest = RequestFaultPartReadSerializer(instance=partsRequest, many=True).data
			serializedComponentRequest = RequestFaultComponentReadSerializer(instance=componentsRequest, many=True).data
			finalFilteredRequests = serializedPartRequest + serializedComponentRequest
		else:
			# if department == 'human-resource':
				# Get all requests records
			allPartsRequests = RequestPart.objects.select_related('name', 'fault', 'user', 'approved_by').all()
			allComponentsRequests = RequestComponent.objects.select_related('name', 'fault', 'user', 'approved_by').all()

			print(f'allPartsRequests total: {len(allPartsRequests)}')
			print(f'allComponentsRequests total: {len(allComponentsRequests)}')

			# Apply the search across multiple fields if search_term is provided
			print(f'hr access: {department == "human-resource"}')
			allPartsRequests = allPartsRequests.filter(
				Q(name__name__icontains=search_term) |
				Q(fault__title__name__icontains=search_term) |
				Q(user__email__icontains=search_term) |
				Q(user__first_name__icontains=search_term) |
				Q(user__middle_name__icontains=search_term) |
				Q(user__last_name__icontains=search_term) |
				Q(user__role__icontains=search_term) |
				Q(user__region__name__icontains=search_term) |
				Q(user__state__name__icontains=search_term) |
				Q(user__username__icontains=search_term) |

				Q(approved_by__username__icontains=search_term) |
				Q(approved_by__email__icontains=search_term) |
				Q(approved_by__first_name__icontains=search_term) |
				Q(approved_by__middle_name__icontains=search_term) |
				Q(approved_by__last_name__icontains=search_term) |
				Q(approved_by__role__icontains=search_term) |
				Q(approved_by__region__name__icontains=search_term) |
				Q(approved_by__state__name__icontains=search_term) |
				Q(approved_by__username__icontains=search_term)
			)
			print(f'searched allPartsRequests total: {len(allPartsRequests)}')

			allComponentsRequests = allComponentsRequests.filter(
				Q(name__name__icontains=search_term) |
				Q(fault__title__name__icontains=search_term) |
				Q(user__email__icontains=search_term) |
				Q(user__first_name__icontains=search_term) |
				Q(user__middle_name__icontains=search_term) |
				Q(user__last_name__icontains=search_term) |
				Q(user__role__icontains=search_term) |
				Q(user__region__name__icontains=search_term) |
				Q(user__state__name__icontains=search_term) |
				Q(user__username__icontains=search_term) |

				Q(approved_by__username__icontains=search_term) |
				Q(approved_by__email__icontains=search_term) |
				Q(approved_by__first_name__icontains=search_term) |
				Q(approved_by__middle_name__icontains=search_term) |
				Q(approved_by__last_name__icontains=search_term) |
				Q(approved_by__role__icontains=search_term) |
				Q(approved_by__region__name__icontains=search_term) |
				Q(approved_by__state__name__icontains=search_term) |
				Q(approved_by__username__icontains=search_term)
			)
			print(f'searched allComponentsRequests total: {len(allComponentsRequests)}')
			################################################
			# Filter for boolean values
			if approved is not None:
				allPartsRequests = allPartsRequests.filter(approved=approved == 'true')
				allComponentsRequests = allComponentsRequests.filter(approved=approved == 'true')
				print(f'approved searched allPartsRequests total: {len(allPartsRequests)}')
				print(f'approved searched allComponentsRequests total: {len(allComponentsRequests)}')

			if rejected is not None:
				allPartsRequests = allPartsRequests.filter(rejected=rejected == 'true')
				allComponentsRequests = allComponentsRequests.filter(rejected=rejected == 'true')
				print(f'rejected searched allPartsRequests total: {len(allPartsRequests)}')
				print(f'rejected searched allComponentsRequests total: {len(allComponentsRequests)}')
			
			# Filter for date ranges (created_at)
			if start_date:
				start_from_date = parse_datetime(start_date)
				start_date_aware = timezone.make_aware(start_from_date, timezone.get_default_timezone())
				if start_from_date:
					allPartsRequests = allPartsRequests.filter(requested_at__gte=start_date_aware)
					allComponentsRequests = allComponentsRequests.filter(requested_at__gte=start_date_aware)
					print(f'start_date searched allPartsRequests total: {len(allPartsRequests)}')
					print(f'start_date searched allComponentsRequests total: {len(allComponentsRequests)}')

			if end_date:
				end_to_date = parse_datetime(end_date)
				end_date_aware = timezone.make_aware(end_to_date, timezone.get_default_timezone())
				if end_to_date:
					allPartsRequests = allPartsRequests.filter(requested_at__lte=end_date_aware)
					allComponentsRequests = allComponentsRequests.filter(requested_at__lte=end_date_aware)
					print(f'end_date searched allPartsRequests total: {len(allPartsRequests)}')
					print(f'end_date searched allComponentsRequests total: {len(allComponentsRequests)}')
			################################################
			# processed search results
			# processedResults = list(allPartsRequests) + list(allComponentsRequests)
			serializedPartsRequests = RequestFaultPartReadSerializer(instance=allPartsRequests, many=True).data
			serializedComponentsRequests = RequestFaultComponentReadSerializer(instance=allComponentsRequests, many=True).data
			finalFilteredRequests = serializedPartsRequests + serializedComponentsRequests
			# # fetch faults associated with each requests
			# faultsOfProcessedResults = [request.fault for request in processedResults]
			# # remove duplicate faults but not 'None' faults
			# filteredFaults = []
			# for fault in faultsOfProcessedResults:
			# 	# consider developing a default faute template for 'None' faults
			# 	if fault == None: continue
			# 	if fault is None or fault not in filteredFaults:
			# 		filteredFaults.append(fault)

			# # Convert list back to QuerySet for pagination
			# filteredFaults = Fault.objects.filter(id__in=[fault.id for fault in filteredFaults]).prefetch_related('partfault', 'componentfault')

		####################### repeated code #####################
		userPaginator = PageNumberPagination()
		if department == 'human-resource':
			userPaginator.page_size = 5  # Number of items per page
		else:
			userPaginator.page_size = 10  # Number of items per page
		paginated_requests = userPaginator.paginate_queryset(finalFilteredRequests, request)
		print(f'final total: {len(finalFilteredRequests)}')
	return userPaginator.get_paginated_response(paginated_requests)


###########################
@api_view(['GET'])
def queryDB(request):
	queryText = None if request.query_params.get('query') == '' else request.query_params.get('query')
	queryType = None if request.query_params.get('qtype') == '' else request.query_params.get('qtype')
	queryRegion = None if (request.query_params.get('qregion') == '' or request.query_params.get('qregion') == 'undefined') else request.query_params.get('qregion')
	queryState = None if (request.query_params.get('qstate') == '' or request.query_params.get('qstate') == 'undefined') else request.query_params.get('qstate')
	queryBank = None if (request.query_params.get('qbank') == '' or request.query_params.get('qbank') == 'undefined') else request.query_params.get('qbank')
	queryLocation = None if (request.query_params.get('qlocation') == '' or request.query_params.get('qlocation') == 'undefined') else request.query_params.get('qlocation')

	print(f'queryText: {queryText}')
	print(f'queryType: {queryType}')
	print(f'queryRegion: {queryRegion}')
	print(f'queryState: {queryState}')
	print(f'queryBank: {queryBank}')
	print(f'queryLocation: {queryLocation}')
	resultCount = 0
	if queryType == 'email':
		resultCount = User.objects.filter(email=queryText).count()
	if queryType == 'username':
		resultCount = User.objects.filter(username=queryText).count()
	if queryType == 'newBank':
		bank = Bank.objects.filter(name=queryText).first()
		if bank:
			print(f'bank match: {bank.name}')
			bankStates = bank.states.all()
			print(f'found {queryText} in {[state.name for state in bankStates]}')
			print(f'in {queryRegion} found {queryText} in {[state.name for state in bankStates if state.region and state.region.name == queryRegion]}')
			bankInState = [state.name for state in bankStates if state.region and state.region.name == queryRegion and state.name == queryState]
			print(f'bank, state, and region match: {bankInState}')
			resultCount = int(bool(bankInState))
		# resultCount = Bank.objects.filter(name=queryText).count()
	if queryType == 'newLocation':
		location = Location.objects.filter(location=queryText)
		resultCount = int(bool(list(location)))
		print(f'result count:{resultCount}')
		# if location:

	if queryType == 'newBranch':
		branches = Branch.objects.filter(name=queryText)
		print(f'branches: {branches}')
		if branches:
			# branches = [branch for branch in branches]
			print(f'{queryText} found in: {[branch.location.location for branch in branches]}')
			locBranch = [branch.location for branch in branches if branch.location.location == queryLocation]
			if locBranch:
				locBranch = locBranch[0]
				print(f'location: {locBranch}')
				# print(f'location-bank: {locBranch[0].bank.all()}')
				print(f'location match: {locBranch.location}')
				banks = [bank for bank in locBranch.bank.all()]
				print(f'banks in {queryLocation}: {[bank.name for bank in banks]}')
				bank = [bank for bank in locBranch.bank.all() if bank.name == queryBank]
				if bank:
					bank = bank[0]
					print(f'bank match: {bank.name}')
					statesBranch = [state for state in bank.states.all()]
					print(f'{queryText}, {queryLocation} and {queryBank} also found in {[state.name for state in statesBranch]}')
					stateBranch = [state for state in statesBranch if state.name == queryState and state.region.name == queryRegion]
					if stateBranch:
						stateBranchFound = stateBranch[0]
						print(f'state and region match: {stateBranchFound}')
						resultCount = int(bool(stateBranch))
						print(f'result count:{resultCount}')
		# resultCount = Branch.objects.filter(name=queryText).count()

	responseData = {"response": resultCount}
	print(f'response count for {queryType}: {responseData}')
	return Response(responseData)
