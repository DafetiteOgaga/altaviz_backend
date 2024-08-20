from django.urls import path
from . import views

app_name = "app_inventory"

urlpatterns = [
	# Create your urlpatterns here.
	path('components/', view=views.components, name='component_list'),
	path('components/<int:pk>/', view=views.components, name='component_details'),

	path('component-name/', view=views.componentName, name='componentName'),
	path('component-name/<int:pk>/', view=views.componentName, name='componentName-details'),

	path('parts/', view=views.parts, name='part_list'),
	path('parts/<int:pk>/', view=views.parts, name='part_details'),

	path('part-name/', view=views.partName, name='partName'),
	path('part-name/<int:pk>/', view=views.partName, name='partName-details'),
]
