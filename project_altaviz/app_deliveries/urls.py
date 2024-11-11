from django.urls import path
from . import views

app_name = "app_deliveries"

urlpatterns = [
	# Create your urlpatterns here.
	path('deliveries/<int:pk>/', view=views.deliveries, name='deliveries'),
]
