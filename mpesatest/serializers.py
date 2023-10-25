from rest_framework import serializers
from .models import PaymentCallback, TransactionCallback, Business2Customer

class PaymentCallbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentCallback
        fields = '__all__'

    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCallback
        fields = '__all__'


class Business2Customer(serializers.ModelSerializer):
    class Meta:
        model = Business2Customer
        fields = '__all__'


class MpesaConfirmation(serializers.ModelSerializer):
    ResultCode = serializers.IntegerField()
    ResultDesc = serializers.CharField()