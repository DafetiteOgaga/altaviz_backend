from django.urls import path
from . import views

app_name = "app_search"

urlpatterns = [
	# Create your urlpatterns here.
	path('fault-search/', view=views.faultSearch, name='faultSearch'),
	path('request-search/', view=views.requestSearch, name='faultSearch'),
	path('field-search/', view=views.queryDB, name='queryDB'),
	path('email-check/', view=views.queryDB, name='queryDB'),
	path('username-check/', view=views.queryDB, name='queryDB'),
	path('newBank-check/', view=views.queryDB, name='queryDB'),
	path('newLocation-check/', view=views.queryDB, name='queryDB'),
	path('newBranch-check/', view=views.queryDB, name='queryDB'),
]
