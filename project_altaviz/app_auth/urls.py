from django.urls import path
from . import views

app_name = "app_auth"

urlpatterns = [
	# Create your urlpatterns here.
	path('login/', view=views.loginView, name='loginView'),
    path('logout/', view=views.logoutView, name='logoutView'),
    path('change-password/<int:pk>/', view=views.changePassword, name='changePassword'),
    path('check-auth/', view=views.checkAuth, name='checkAuth'),
]
