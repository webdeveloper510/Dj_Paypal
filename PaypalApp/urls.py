
from django.urls import path
from .views import CompletePayoutRequest
urlpatterns = [
    path('', CompletePayoutRequest, name='payout')

]
