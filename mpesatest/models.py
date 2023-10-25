from django.db import models

class PaymentCallback(models.Model):
    MerchantRequestID = models.CharField(max_length=255)
    CheckoutRequestID = models.CharField(max_length=255)
    ResponseCode = models.CharField(max_length=10)
    ResponseDescription = models.CharField(max_length=255)
    CustomerMessage = models.TextField()


class TransactionCallback(models.Model):
    OriginatorConversationID = models.CharField(max_length=255)
    ConversationID = models.CharField(max_length=255)
    ResponseCode = models.CharField(max_length=10)
    ResponseDescription = models.CharField(max_length=255)


class Business2Customer(models.Model):
    OriginatorConversationID = models.CharField(max_length=255)
    ConversationID = models.CharField(max_length=255)
    ResponseCode = models.CharField(max_length=10)
    ResponseDescription = models.CharField(max_length=255)