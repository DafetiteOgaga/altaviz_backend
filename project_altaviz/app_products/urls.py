from django.urls import path
from . import views

app_name = "app_products"

urlpatterns = [
	# Create your urlpatterns here.
	path('product/', view=views.product, name='product-list'),
    path('product/<int:pk>/', view=views.product, name='product-detail'),
]
