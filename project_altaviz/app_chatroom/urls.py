from django.urls import path
from . import views

app_name = "app_chatroom"

urlpatterns = [
	# Create your urlpatterns here.
	# u - user and c - contact
	path('chat-user/<int:cpk>/<int:upk>/', view=views.chatUser, name='chatUser'),
]
