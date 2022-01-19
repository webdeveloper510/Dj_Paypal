from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    Email = models.CharField(max_length=255, default=''),
    Refrence_Id = models.IntegerField(blank=True, null=True)


class transactionsModel(models.Model):

    payout_item_id = models.CharField(max_length=100, default='')
    transaction_id = models.CharField(max_length=100, default='')
    transaction_status = models.CharField(max_length=100, default='')
    currency = models.CharField(max_length=100, default='')
    payout_fee = models.FloatField()
    payout_batch_id =  models.CharField(max_length=100, default='')
    # recipient_type = models.IntegerField()
    recieving_amount = models.FloatField()
    reciever_email = models.CharField(max_length=100, default='')
    recipient_wallet = models.CharField(max_length=100, default='')
    time_processed = models.CharField(max_length=100, default='')


class Meta:
    model = transactionsModel # model name
    fields = ('__all__')