from django.contrib import admin
from django.urls import path, include
from PaypalApp.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PaypalApp.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]
