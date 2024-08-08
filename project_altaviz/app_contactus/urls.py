from django.urls import path
from . import views

app_name = 'app_contactus'

urlpatterns = [
	# Create your urlpatterns here.
	path('contact-us/', view=views.contact_us, name='contact-us'),
]
