from django.contrib import admin
from django.urls import path, include
from PaypalApp.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PaypalApp.urls', namespace='PaypalApp'))
]
