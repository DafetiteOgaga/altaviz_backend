from django.urls import path
from . import views

app_name = "app_custodian"

urlpatterns = [
	# Create your urlpatterns here.
	path('branches/', view=views.branches, name='branches'),
	path('branches/<int:pk>/', view=views.branches, name='bankBranches'),
	# path('request-change-details/', view=views.requestChangeDetails, name='requestChangeDetails'),
	# path('custodian-update-notifications/', view=views.updateCustodianNotification, name='updateCustodianNotification'),
	# path('custodian-update-notifications/<int:pk>/', view=views.updateCustodianNotification, name='updateCustodianNotification'),
	# path('custodian-update-notifications/<int:pk>/total/', view=views.totalUpdateCustodianNotification, name='totalUpdateCustodianNotification')
]
