from django.urls import path
from . import views

urlpatterns = [
	# Create your urlpatterns here.
	path('', view=views.home, name='home'),
	path('nothing/', view=views.placeholder, name='placeholder'),
	path('login-details/', view=views.getAllAccounts, name='getAllAccounts'),
	path('version/', view=views.versionNumber, name='versionNumber'),
]
