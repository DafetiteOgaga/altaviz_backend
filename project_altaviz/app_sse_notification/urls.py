from django.urls import path
from . import views

app_name = "app_sse_notification"

urlpatterns = [
	# Create your urlpatterns here.
	# URL pattern to handle SSE notifications
    path('real-time/notifications/', views.sse_notification_view, name='sse_notifications'),
]
