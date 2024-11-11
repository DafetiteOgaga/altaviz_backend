from django.urls import path
from . import views

app_name = "app_fault"

urlpatterns = [
	# Create your urlpatterns here.
	path('fault/', view=views.fault, name='fault'),
	path('fault-detail/<int:pk>/', view=views.faultDetail, name='faultDetail'),
	path('fault-name/', view=views.faultName, name='faultName'),

	# custodian
	path('unresolved-faults/<int:pk>/', view=views.custodianUnresolvedFaults, name='custodianUnresolvedFaults'),
	path('pending-faults/<int:pk>/', view=views.custodianPendingFaults, name='custodianPendingFaults'),
	path('pending-faults/<str:type>/<int:pk>/', view=views.custodianPendingFaults, name='custodianPendingFaults-type'),
	path('pending-faults/<int:pk>/total/', view=views.totalCustodianPendingFaults, name='totalCustodianPendingFaults'),
	path('unconfirmed-faults/<int:pk>/', view=views.custodianUnconfirmedResolutions, name='custodianUnconfirmedResolutions'),
	path('unconfirmed-faults/<str:type>/<int:pk>/', view=views.custodianUnconfirmedResolutions, name='custodianUnconfirmedResolutions-type'),
	path('unconfirmed-faults/<int:pk>/total/', view=views.totalCustodianUnconfirmedResolutions, name='totalCustodianUnconfirmedResolutions'),
	path('fault/<int:pk>/delete/', view=views.deleteFault, name='deleteFault'),

	# engineer
	path('engineer-unresolved-faults/<int:pk>/', view=views.engineerUnresolvedFaults, name='engineerUnresolvedFaults'),
	path('engineer-pending-faults/<int:pk>/', view=views.engineerPendingFaults, name='engineerPendingFaults'),
	path('engineer-pending-faults/<str:type>/<int:pk>/', view=views.engineerPendingFaults, name='engineerPendingFaults-type'),
	path('engineer-pending-faults/<int:pk>/total/', view=views.totalEngineerPendingFaults, name='totalEngineerPendingFaults'),
	path('engineer-unconfirmed-faults/<int:pk>/', view=views.engineerUnconfirmedFaults, name='engineerUnconfirmedFaults'),
	path('engineer-unconfirmed-faults/<str:type>/<int:pk>/', view=views.engineerUnconfirmedFaults, name='engineerUnconfirmedFaults-type'),
	path('engineer-unconfirmed-faults/<int:pk>/total/', view=views.totalEngineerUnconfirmedFaults, name='engineerUnconfirmedFaults'),

	# supervisor and helpdesk
	path('region-pending-faults/<int:pk>/', view=views.regionFaults, name='regionFaults'),
	path('region-pending-faults/<str:type>/<int:pk>/', view=views.regionFaults, name='regionFaults-type'),
	path('region-pending-faults/<int:pk>/total/', view=views.totalRegionFaults, name='totalRegionFaults'),

	# human-resource
	path('all-pending-faults-wRequests/<int:pk>/', view=views.allFaultsWRequests, name='allFaultsWRequests'),
	path('all-pending-faults-wRequests/<str:type>/<int:pk>/', view=views.allFaultsWRequests, name='allFaultsWRequests-type'),
	path('all-pending-faults-wRequests/<int:pk>/total/', view=views.totalAllFaultsWRequests, name='totalAllFaultsWRequests'),

	# path('fault-search/', view=views.faultSearch, name='faultSearch'),
]
