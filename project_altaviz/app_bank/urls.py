from django.urls import path
from . import views

app_name = "app_bank"

urlpatterns = [
	# Create your urlpatterns here.
	path('banks/', view=views.banksView, name='banks'),
	path('banks-branch/', view=views.banksBranchView, name='banks-branch'),
	path('states/', view=views.statesView, name='states'),
]
