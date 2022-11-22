from django.urls import path
from django.conf.urls import handler404
from .views import *

urlpatterns = [
    path('', StripeHomePage.as_view(), name='home'),
    path('item/<int:pk>', StripeItemView.as_view(), name='view-item'),
    path('buy/<int:pk>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('order/', OrderItemsView.as_view(), name='items-order'),
    path('buy/order/', CreateCheckoutSessionOrderView.as_view(), name='create-checkout-session-order'),
    path('config/', stripe_config),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancelled/', CancelledView.as_view(), name='canceled'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
]

handler404 = page_not_found
