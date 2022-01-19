
from django.urls import path
from .views import SubmitPayoutRequest
urlpatterns = [
    path('', SubmitPayoutRequest, name='payout')

]
