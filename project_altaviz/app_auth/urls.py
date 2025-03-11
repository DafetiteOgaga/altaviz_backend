from django.urls import path
from . import views

app_name = "app_auth"

urlpatterns = [
	# Create your urlpatterns here.
	path('login/', view=views.loginView, name='loginView'),
    path('logout/', view=views.logoutView, name='logoutView'),
    path('change-password/<int:pk>/', view=views.changePassword, name='changePassword'),
    path('reset-password-request/', view=views.resetPasswordRequest, name='resetPasswordRequest'),
    path('reset-password-done/<uid>/<token>/', view=views.resetPasswordDone, name='resetPasswordDone'),
    path('api/get-csrf-token/', view=views.get_csrf_token, name='get_csrf_token'),
    path('test-api/', view=views.testApi, name='testAPI'),
    path('check-auth/', view=views.checkAuth, name='checkAuth'),
]
