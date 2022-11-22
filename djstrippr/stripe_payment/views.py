import stripe

from .models import Item, Order, Tax
from django.db.models import Sum
from django.conf import settings
from django.views.generic import ListView, View
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.http.response import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt


class StripeHomePage(TemplateView):
    template_name = 'home.html'


class StripeItemView(DetailView):
    model = Item
    template_name = 'item.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class OrderItemsView(ListView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum_tax_rate = Tax.objects.aggregate(Sum('tax_rate'))
        context['tax_rate_value'] = sum_tax_rate['tax_rate__sum']
        return context


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)
        domain_url = 'http://localhost:8000/'
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': item.price_id,
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})

        return JsonResponse({'sessionId': checkout_session['id']})


class CreateCheckoutSessionOrderView(View):
    def get(self, request, *args, **kwargs):
        items_in_order = Order.objects.all()
        domain_url = 'http://localhost:8000/'
        line_items = []
        taxs_query = list(Tax.objects.values('tax_rate_id'))
        taxs = [tax['tax_rate_id'] for tax in taxs_query]
        for item in items_in_order:
            price = Item.objects.get(name=item.name)
            elem_dict_item = {
                'price': price.price_id,
                'quantity': item.quantity,
                'tax_rates': taxs
            }
            line_items.append(elem_dict_item)
        discount_value = items_in_order[0].discount
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                discounts=[
                    {
                        'coupon': discount_value.discount_stripe_id,
                    }
                ],
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
            )
        except Exception as e:
            return JsonResponse({'error': str(e)})

        return JsonResponse({'sessionId': checkout_session['id']})


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancel.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print('Payment was successful!')

    return HttpResponse(status=200)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1> Страница не найдена </h1>')
