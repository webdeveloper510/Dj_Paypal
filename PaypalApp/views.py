from curses.ascii import HT
import http
from shlex import quote
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from paypal.standard.forms import PayPalPaymentsForm
import csv
import io
from django.conf import settings
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError
from paypalhttp.serializers.json_serializer import Json
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsGetRequest
from .models import transactionsModel
import numpy as np


def GetClient(request):

    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET

    environment = SandboxEnvironment(
        client_id=client_id, client_secret=client_secret)
    client = PayPalHttpClient(environment)
    return client


def PayoutBody(request, io_string):

    mydict = list()
    for data in csv.reader(io_string, delimiter=',', quotechar="|"):

        dict = {"recipient_type": 'EMAIL', "amount": {
            "value": data[2], "currency": "USD"},
            "note": "Thanks for your patronage!",
            "sender_item_id": "201403140001",
            "receiver": data[0]}
        mydict.append(dict)
    body = {

        "sender_batch_header": {
            "sender_batch_id": "15240864949",
            "email_subject": "This email is related to simulation"
        },
        "items": mydict


    }

    return body


def MakePayoutRequest(request, body):

    request = PayoutsPostRequest()
    request.request_body(body)
    return request


def GetPayoutBody(request, response, client):

    payout_item_id = response.result.batch_header.payout_batch_id
    requestt = PayoutsGetRequest(payout_item_id)
    payout_response = client.execute(requestt)
    response = payout_response.result
    return response


def SubmitPayoutRequest(request):

    client = GetClient(request)

    if request.method != 'POST':
        return render(request, "payment/file.html")
    else:
        csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a Csv File')
        return redirect('/')

    ########### read csv ###############################
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    ########### read csv ###############################

    body = PayoutBody(request, io_string)  # call to make the request body
    # call to MakePayout customised function
    request = MakePayoutRequest(request, body)

    try:

        # Make Api call to get Paypout Batch Id
        response = client.execute(request)
        # Get Response from   Batch Id
        PayoutResponse = GetPayoutBody(request, response, client)

        for payout_data in PayoutResponse['items']:
            # Submit Transactions data into the database
            CreateTransactions(payout_data)

        return redirect('/')
    except IOError as ioe:
        print(ioe)
        if isinstance(ioe, HttpError):
            print(ioe.status_code)
        else:
            print(ioe)


def CreateTransactions(payout_data):  # Match Payout rows to the DB table

    _, created = transactionsModel.objects.update_or_create(
        payout_item_id=payout_data['payout_item_id'],
        # transaction_id=payout_data['transaction_id'],
        transaction_status=payout_data['transaction_status'],
        currency=payout_data['payout_item_fee']['currency'],
        payout_fee=payout_data['payout_item_fee']['value'],
        payout_batch_id=payout_data['payout_batch_id'],
        recieving_amount=payout_data['payout_item']['amount']['value'],
        reciever_email=payout_data['payout_item']['receiver'],
        recipient_wallet=payout_data['payout_item']['recipient_wallet'],
        time_processed=payout_data['time_processed']
    )
