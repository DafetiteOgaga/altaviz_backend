from django.urls import path
from . import views

app_name = "app_inventory"

urlpatterns = [
	# Create your urlpatterns here.
	path('components/', view=views.components, name='component_list'),
	path('components/<int:pk>/', view=views.components, name='component_details'),

	path('component-name/', view=views.componentName, name='componentName'),
	path('component-name/<int:pk>/', view=views.componentName, name='componentName-details'),

	path('parts/', view=views.parts, name='part_list'),
	path('parts/<int:pk>/', view=views.parts, name='part_details'),

	path('part-name/', view=views.partName, name='partName'),
	path('part-name/<int:pk>/', view=views.partName, name='partName-details'),

	path('request-component/', view=views.requestComponent, name='requestComponent'),
	path('request-component/<int:pk>/', view=views.requestComponent, name='requestComponent'),
	path('request-component/<str:type>/<int:pk>/', view=views.requestComponent, name='requestComponent-type'),
	path('approved-request-component/<int:pk>/', view=views.approvedRequestComponent, name='approvedRequestComponent'),
	path('request-component/<int:pk>/total/', view=views.totalPendingRequestComponent, name='totalPendingRequestComponent'),
	path('request-component/<int:pk>/delete/', view=views.deleteCompRequest, name='deleteCompRequest'),

	path('request-part/', view=views.requestPart, name='requestPart'),
	path('request-part/<int:pk>/', view=views.requestPart, name='requestPart'),
	path('request-part/<str:type>/<int:pk>/', view=views.requestPart, name='requestPart-type'),
	path('approved-request-part/<int:pk>/', view=views.approvedRequestPart, name='approvedRequestPart'),
	path('request-part/<int:pk>/total/', view=views.totalPendingRequestPart, name='totalPendingRequestPart'),
	path('request-part/<int:pk>/delete/', view=views.deletePartRequest, name='deletePartRequest'),

	path('post-part/<int:pk>/', view=views.unapprovedPart, name='unapprovedPart'),
	path('post-part/<str:type>/<int:pk>/', view=views.unapprovedPart, name='unapprovedPart-type'),
	path('post-part/<int:pk>/delete/', view=views.deleteUnapprovedPart, name='deleteUnapprovedPart'),
	path('post-part/<int:pk>/total/', view=views.totalUnapproved, name='totalUnapproved'),
	path('approved-part/<int:pk>/', view=views.approvedParts, name='approvedParts'),

	# helpdesk and engineers
	path('user-request/<int:pk>/', view=views.regionUserRequests, name='regionUserRequests'),
	path('user-request/<str:type>/<int:pk>/', view=views.regionUserRequests, name='regionUserRequests-type'),
	path('user-request/<int:pk>/total/', view=views.totalRegionUserRequests, name='totalRegionUserRequests'),
	path('regional-unconfirmed-faults/<int:pk>/', view=views.unconfirmedRegionResolutions, name='unconfirmedResolutionsHelpDesk'),
	path('regional-unconfirmed-faults/<str:type>/<int:pk>/', view=views.unconfirmedRegionResolutions, name='unconfirmedResolutionsHelpDesk-type'),
	path('regional-unconfirmed-faults/<int:pk>/total/', view=views.totalUnconfirmedRegionResolutions, name='totalUnconfirmedResolutionsHelpDesk'),
	path('all-faults-requests/<int:pk>/', view=views.faultsWithRequests, name='faultsWithRequests'),
	path('all-faults-requests/<int:pk>/total/', view=views.totalFaultsWithRequests, name='totalFaultsWithRequests'),

	# human-resource
	path('all-request-faults/<int:pk>/', view=views.allUserRequests, name='allUserRequests'),
	path('all-request-faults/<str:type>/<int:pk>/', view=views.allUserRequests, name='allUserRequests-type'),
	path('all-request-faults/<int:pk>/total/', view=views.totalAllUserRequests, name='totalAllUserRequests'),

	path('request-status/<int:pk>/', view=views.requestStatus, name='requestStatus'),
	# path('parts-status/', view=views.partsStatus, name='partsStatus'),

	path('workshop-request/<str:type>/<int:pk>/', view=views.unapprovedWorkshopRequests, name='unapprovedWorkshopRequests-type'),

	path('all-request-only/<str:type>/<int:pk>/', view=views.allRequestsOnly, name='allRequestsOnly-type'),
	path('all-request-only/<int:pk>/total/', view=views.totalAllRequestsOnly, name='totalAllRequestsOnly'),

	path('workshop-component-request/<int:pk>/', view=views.workshopRequests, name='workshopRequests'),
	path('workshop-component-request/<str:type>/<int:pk>/', view=views.workshopRequests, name='workshopRequests-type'),
	path('workshop-component-request/<int:pk>/total/', view=views.totalWorkshopRequests, name='totalWorkshopRequests'),
]
