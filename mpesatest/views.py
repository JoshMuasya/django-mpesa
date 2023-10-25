import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework import generics
from .models import PaymentCallback, TransactionCallback, Business2Customer
from .serializers import PaymentCallbackSerializer, TransactionSerializer, Business2Customer

class SafaricomProxyView(APIView):
    def get(self, request):
        consumer_key = 'uEfNJ27BkrVG4lG8EDQ6O0byekGneTHY'
        consumer_secret = 'GOJwVnfSjPu4NYCS'
        safaricom_api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

        headers = {
            'Content-Type': 'application/json',
        }

        auth = (consumer_key, consumer_secret)

        try: 
            response = requests.get(safaricom_api_url, headers=headers, auth=auth)
            response_json = response.json()
            token = response_json.get('access_token')
            return Response({'token': token}, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({'error': 'An error occured while proxying the request.'}, status=500)
        

class Customer2Business(APIView):
    def get(self, request):
        from .views import SafaricomProxyView

        safaricom_proxy = SafaricomProxyView()

        data = {
            "BusinessShortCode": 174379,
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMxMDIzMTgxNDU1",
            "Timestamp": "20231023181455",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 1,
            "PartyA": 254798040353,
            "PartyB": 174379,
            "PhoneNumber": 254798040353,
            "CallBackURL": "http://127.0.0.1:8000/mpesa-confirmation/",
            "AccountReference": "CompanyXLTD",
            "TransactionDesc": "Payment of X"
        }

        response = safaricom_proxy.get(request)

        if response.status_code == 200:
            token = response.data.get('token')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

            lipampesa = requests.post(url, json=data, headers=headers)

            if lipampesa.status_code == 200:
                response_data = lipampesa.json()

                lipa_response = PaymentCallback(**response_data)
                lipa_response.save()

                serializer = PaymentCallbackSerializer(lipa_response)

                return Response({'lipa': serializer.data}, status=200)
            else:
                return Response({'error': 'Failed to make the POST request'}, status=lipampesa.status_code)


class TransactionStatus(APIView): 
    def get(self, request):
        from .views import SafaricomProxyView

        safaricom_proxy = SafaricomProxyView()

        response = safaricom_proxy.get(request)

        data = {
            "Initiator": "testapi",
            "SecurityCredential": "E8D/6ewVfxKBrqe2m09c2de7JkKIcLW0Pw3XGi45MrLtKQ4De/RB2AAZDuxNRs5EQ50Vra3bf0huUhOKxgfOG0K9RiJOhxNOXcNIO8umEcw4z3k4VzkdpxT6xM3HaEcJu8FL7UY9rWEdpnZLgxm/NX9Ri7ROfllIflehyag5sf0TO3DdlBAJpC2hSBcaY7ziL+UylWRNNMb9/t5lzR3jWgoHxSfac9WKSBCE7hZcImVScCXiYka3TSlpMpIlJq+JB0FQxD8/CdSHBUfYJmH/u4kP74kGGR+3RD5aNeJ6wK/E730tazlKVWZN9MWjwl9nBRSPBLJ9xYZJTJSo23g0Yg==",
            "CommandID": "TransactionStatusQuery",
            "TransactionID": "OEI2AK4Q16",
            "PartyA": 600999,
            "IdentifierType": 4,
            "ResultURL": "https://mydomain.com/TransactionStatus/result/",
            "QueueTimeOutURL": "https://mydomain.com/TransactionStatus/queue/",
            "Remarks": "re",
            "Occassion": "null"
        }

        if response.status_code == 200:
            token = response.data.get('token')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"

            transactions = requests.post(url, json=data, headers=headers)

            if transactions.status_code == 200:
                response_data = transactions.json()

                transaction_code = TransactionCallback(**response_data)
                transaction_code.save()

                serializer = TransactionSerializer(transaction_code)

                return Response({'status': serializer.data}, status=200)
            else:
                return Response({'error': 'Failed to make the POST request'}, status=transactions.status_code)


class Business2Customer(APIView): 
    def get(self, request):
        from .views import SafaricomProxyView

        safaricom_proxy = SafaricomProxyView()

        response = safaricom_proxy.get(request)

        data = {
            "OriginatorConversationID": "5e75c04a-9d70-4cf7-a6fe-a312dfd54619",
            "InitiatorName": "testapi",
            "SecurityCredential": "M8t0OhzFNH71aL5ZnR3k4UoYSMX9rREd6FhaH0LUTzvFvB7T1Aa/wtV+EKJm0XpitA0yo0EvEI1iq/7MRan5CZrkjcqHUuvTXa6XdWVxFXxnUF7GSb1TXPhCKiaoyBVqTMUj4l95Wif2zhtrewG188Hh/nxo0yN8jg+UYkHwY2yTnPlgVUSv197BTxvxbrLkRAOV0MgcH2QDYFUmpccMoMIQ0TryRqggpXZrR+ZtC/UcO+i92n4ttylCxzpAIkudlAZW6bPW7YEpImUeRThx4Wcd9j34XjSlbhojefkBkS0roUOdjfZXfdFUZ2PcLmKg27+4afpRXgnOc7uJOPyIkQ==",
            "CommandID": "BusinessPayment",
            "Amount": 10,
            "PartyA": 600986,
            "PartyB": 254798040353,
            "Remarks": "Test remarks",
            "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
            "ResultURL": "https://mydomain.com/b2c/result",
            "occasion": "null"
        }

        if response.status_code == 200:
            token = response.data.get('token')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest"

            business2Customer = requests.post(url, json=data, headers=headers)

            if business2Customer.status_code == 200:
                response_data = business2Customer.json()

                business = Business2Customer(**response_data)
                business.save()

                serializer = Business2Customer(business)

                return Response({'status': serializer.data}, status=200)
            else:
                return Response({'error': 'Failed to make the POST request'}, status=business.status_code)
            

class MpesaConfirmation(APIView):
    def post(self, request):
        data = request.data
        response_data = {
            "ResultCode": 0,
            "ResultDesc": "Confirmation Received Successfully"
        }

        with open("M_pesaConfirmation.txt", "a") as log:
            log.write(json.dumps(data, indent=4))

        return Response(response_data, status=data.status_code)

