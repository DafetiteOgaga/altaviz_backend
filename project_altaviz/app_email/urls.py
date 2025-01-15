from django.urls import path
from . import views

app_name = "app_email"

urlpatterns = [
	# Create your urlpatterns here.
	# path('send-email/',views.send_email, name='send_email'),
	path('send-email/<int:pk>/',views.sendEmailToClient, name='send_email'),
]
