"""
URL configuration for vpn_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from services.views import VPNEmulator

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),
    path('services/', include('services.urls')),

    path('<str:user_site_name>/<path:original_url>/v', VPNEmulator.as_view(), name="vpnemulator"),
    path('<str:user_site_name>/v', VPNEmulator.as_view(), name="vpnemulator_name")
]
