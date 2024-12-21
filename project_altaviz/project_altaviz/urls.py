"""
URL configuration for project_altaviz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_chatroom.urls')),     # For app_chatroom configuration
    path('', include('app_sse_notification.urls')),     # For app_sse_notification configuration
    path('', include('app_deliveries.urls')),     # For app_deliveries configuration
    path('', include('app_search.urls')),     # For app_search configuration
    path('', include('app_auth.urls')),     # For app_auth configuration
    path('', include('app_custodian.urls')),     # For app_custodian configuration
    path('', include('app_location.urls')),     # For app_location configuration
    path('', include('app_inventory.urls')),     # For app_inventory configuration
    path('', include('app_bank.urls')),     # For app_bank configuration
    path('', include('app_fault.urls')),     # For app_fault configuration
    path('', include('app_products.urls')),     # For app_products configuration
    path('', include('app_contactus.urls')),     # For app_contactus configuration
    path('', include('app_users.urls')),     # For app_users configuration
    path('', include('app_altaviz.urls')),     # For app_altaviz configuration
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:  # Only serve media files in development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)