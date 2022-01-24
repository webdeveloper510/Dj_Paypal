from curses.ascii import HT
import email
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
from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
from paypalpayoutssdk.payouts import PayoutsGetRequest
from .models import transactionsModel
from django.core import serializers
import json
import re


def GetClient():

    client_id = settings.PAYPAL_CLIENT_ID
    client_secret = settings.PAYPAL_CLIENT_SECRET

    if settings.PAYPAL_TEST:
        environment = SandboxEnvironment(
            client_id=client_id, client_secret=client_secret)
    else:
        environment = LiveEnvironment(
            client_id=client_id, client_secret=client_secret)

    client = PayPalHttpClient(environment)

    return client


def PayoutBody(request, io_string):

    mydict = list()
    recipient_type = ''

    for data in csv.reader(io_string, delimiter=',', quotechar="|"):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, data[0])):
            recipient_type = "EMAIL"
            receiver = data[0]
        else:
            recipient_type = "PHONE"
            receiver = data[0]
        dict = {
            # Make a list of dictionary to store the dynamic  variable into the json
            "recipient_type": recipient_type, "amount":
            {
                "value": data[2],
                "currency": data[1]
            },
            "note": "Thanks for your patronage!",
            "sender_item_id": "201403140001",
            "receiver": receiver
        }
        mydict.append(dict)
    body = {
        "sender_batch_header": {
            "sender_batch_id": "15240864949",
            "email_subject": "This email is related to simulation"
        },
        "items": mydict    # Call List of dictionary
    }

    return body


def MakePayoutRequest(body):
    request = PayoutsPostRequest()  # Make Payout POST request
    request.request_body(body)
    return request


def GetPayout(response, client):

    # Get Payout Batch id from response
    payout_item_id = response.result.batch_header.payout_batch_id

    ###### Make a request from Batch Id ###########
    requestt = PayoutsGetRequest(payout_item_id)

    payout_response = client.execute(requestt)  # execute request
    response = payout_response.result  # Payout Response from Payout Batch id
    return response


def CompletePayoutRequest(request):
    client = GetClient()
    PayoutId = list()

    if request.method != 'POST':
        list_id = request.session.get('ids')
        if list_id is None:
            allRecords = []
        else:
            allRecords = transactionsModel.objects.filter(
                id__in=list_id).values()
        context = {
            'allRecords': allRecords
        }
        # request.session['ids'] = []
        return render(request, "Payment/file.html", context)
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

    body = PayoutBody(request, io_string)

    # call to make the request body
    # call to MakePayout customised function

    PayOutRequest = MakePayoutRequest(body)

    try:
        # Make Api call to get Paypout Batch Id
        response = client.execute(PayOutRequest)
        # Get Response from   Batch Id
        Payout = GetPayout(response, client)

        for payout_data in Payout['items']:
            # Submit Transactions data into the database
            id = CreateTransactions(request, payout_data)
            PayoutId.append(id)
        request.session['ids'] = PayoutId
        messages.success(request, ("Transaction created"))

        return redirect('/')
    except IOError as ioe:
        print(ioe)
        if isinstance(ioe, HttpError):
            print(ioe.status_code)
        else:
            print(ioe)


def CreateTransactions(request, payout_data):  # Match Payout rows to the DB table

    created = transactionsModel(
        payout_item_id=payout_data['payout_item_id'],
        # transaction_id=payout_data['transaction_id'],
        transaction_status=payout_data['transaction_status'],
        currency=payout_data['payout_item_fee']['currency'],
        payout_fee=payout_data['payout_item_fee']['value'],
        payout_batch_id=payout_data['payout_batch_id'],
        recieving_amount=payout_data['payout_item']['amount']['value'],
        reciever=payout_data['payout_item']['receiver'],
        recipient_wallet=payout_data['payout_item']['recipient_wallet'],
        time_processed=payout_data['time_processed'],
        recipient_type=payout_data['payout_item']['recipient_type']
    )
    created.save()
    id = created.pk
    return id


def GetPayoutTransactions(request):
    Payouts = transactionsModel.objects.filter().values()
    context = {
        "Payoutsdata": Payouts
    }
    return render(request, 'Payment/PayoutTransactions.html', context)
