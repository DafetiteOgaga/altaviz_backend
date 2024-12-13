from django.urls import path
from . import views

urlpatterns = [
    # create new user account and create new location/branch if needed
    path('user/', view=views.users, name='user'),
    path('user/<int:pk>/', view=views.users, name='userDetail'),

    # details update request by users
    path('user-details-update/<int:pk>/', view=views.userDetaileUpdate, name='userDetaileUpdate'),

    # notification for update request human-resource and approving/rejecting the request
    path('approve-user-details-update/<int:pk>/', view=views.approvedDetailsChange, name='approvedDetailsChange'),
    path('approve-user-details-update/<str:type>/<int:pk>/', view=views.approvedDetailsChange, name='approvedDetailsChange-type'),
    path('approve-user-details-update/<int:pk>/total/', view=views.totalApprovedDetailsChange, name='totalApprovedDetailsChange'),

    ## region engineers and their locations
    path('region-engineers/<int:pk>/', view=views.regionEngineers, name='regionEngineers'),

    # engineers notification and assignment of engineers to locations
    path('new-location-assignment/<int:pk>/', view=views.assignEngineerToLocation, name='assignEngineerToLocation'),
    path('new-location-assignment/<str:type>/<int:pk>/', view=views.assignEngineerToLocation, name='assignEngineerToLocation-type'),
    path('new-location-assignment/<int:pk>/total/', view=views.totalAssignEngineerToLocation, name='totalAssignEngineerToLocation'),

    # path('all-regions/<int:pk>/', view=views.getRegions, name='getRegions'),


	# # Create your urlpatterns here.
	# # authentication
	# path('login/', views.login_page, name='login'),
	# path('logout/', views.logout_page, name='logout'),
	# path('register/', views.register_page, name='register'),

	# # profile
	# path('profile/<int:pk>/', views.profile_page, name='profile'),
	# path('profile-update/<int:pk>/', views.profile_update, name='profile_update'),

    # # change and reset
	# path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('password_reset/', views.custom_password_reset, name='password_reset'),
    # path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset/failed/', views.password_reset_failed_view, name='password_reset_failed'),
    # path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

	# # search
	# path('search/', views.advanced_search, name='advanced_search'),
    # path('autocomplete/', views.autocomplete, name='autocomplete'),
]
