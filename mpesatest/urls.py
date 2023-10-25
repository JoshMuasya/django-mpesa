from django.urls import path
from .views import SafaricomProxyView, Customer2Business, TransactionStatus, MpesaConfirmation

urlpatterns = [
    path('safaricom-proxy/', SafaricomProxyView.as_view(), name='safaricom-proxy'),
    path('customer2business/', Customer2Business.as_view(), name='customer2business'),
    path('transactionstatus/', TransactionStatus.as_view(), name='transactionstatus'),
    path('mpesa-confirmation/', MpesaConfirmation.as_view(), name='mpesa-confirmation'),
    # path('payment-callback/', PaymentCallbackCreateView.as_view(), name='payment-callback-create'),
]