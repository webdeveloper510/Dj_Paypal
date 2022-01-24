
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CompletePayoutRequest, GetPayoutTransactions,RemovePayout

app_name = 'PaypalApp'

urlpatterns = [
    path('', CompletePayoutRequest, name='payout'),
    path('GetPayouts/', GetPayoutTransactions, name='GetPayouts'),
    path('DelPayout/<str:pk>', RemovePayout, name='DelPayouts'),

]
