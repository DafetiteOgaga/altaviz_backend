from django.urls import path
from . import views

app_name = "app_location"

urlpatterns = [
	# Create your urlpatterns here.
	# i prefferably used state and bank app for this instead
	path('locations/', view=views.locations, name='locations'),
	path('custodian-details-update/<int:pk>/<str:state>/<str:bank>/', view=views.bankRegionLocations, name='bankRegionLocations'),
	path('others-details-update/<int:pk>/<str:state>/', view=views.RegionLocations, name='RegionLocations'),
]
