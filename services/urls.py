from django.urls import path

from .views import Links

app_name = 'services'

urlpatterns = [
    path('links/', Links.as_view(), name="links"),

]