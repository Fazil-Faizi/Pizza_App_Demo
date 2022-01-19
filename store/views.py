from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckoutForm, ContactForm
from django.db.models import Max

def home(request):
    return render(request, 'store/home.html')

def contacts(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            try:
                send_mail(name, message, email, ['pizza@peak.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, f'We received your Message! ')
            return redirect('store:pizza-contacts')
    return render(request, "store/contacts.html", {'form': form})


def about(request):
    return render(request, 'store/about.html')

def menu(request):
    foods=Food.objects.all()
    context={'foods' : foods}
    return render(request, 'store/menu.html', context)

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "store/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                payment_option = form.cleaned_data.get('payment_option')
                order.save()

                if payment_option == 'S':
                    return redirect('store:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('store:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('store:checkout')

        except ObjectDoesNotExist:
            return redirect("store:order-summary")

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "store/payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        currentOrderId = Order.objects.aggregate(Max('order_number'))
        Id = currentOrderId.get('order_number__max')
        orderId=int(Id)+1


        # create the payment
        payment = Payment()
        payment.order_number = orderId
        payment.user = self.request.user
        payment.amount = order.get_total()
        payment.save()

        # assign the payment to the order

        order.payment = payment
        order.order_number=orderId
        order.save()
        return redirect("store:order-final")



def OrderFinalView(request):

    user = request.user
    order = Order.objects.get(user=user, ordered=False)
    order_foods=order.foods.all()
    order_foods.update(ordered=True)
    for food in order_foods:
        food.save()

    order.ordered = True
    order.paid = True
    order.save()

    context = {
    'user': user,
    'order': order
    }

    return render(request, 'store/order_final.html', context)





@login_required
def add_to_cart(request, slug):
    food= get_object_or_404(Food, slug=slug)
    order_food, created = OrderFood.objects.get_or_create(
        food=food,
        user=request.user,
        ordered=False
    )
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]

        if order.foods.filter(food__slug=food.slug).exists():
            order_food.quantity+=1
            order_food.save()
        else:
            order.foods.add(order_food)
    else:
        order=Order.objects.create(user=request.user)
        order.foods.add(order_food)
    return redirect("store:pizza-menu")




class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):

        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object': order
            }
            return render(self.request, 'store/order_summary.html', context)
        except ObjectDoesNotExist:
            order=Order.objects.create(user=self.request.user)
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={
                'object': order
            }
            return render(self.request, 'store/order_summary.html', context)

@login_required
def remove_from_cart(request, slug):
    food=get_object_or_404(Food, slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order=order_qs[0]

        if order.foods.filter(food__slug=slug).exists():
            order_food=OrderFood.objects.filter(
                food=food,
                user=request.user,
                ordered=False
            )[0]
            order_food.quantity -=1
            order_food.save()

            if order_food.quantity<=0:
                order_food.delete()
            return redirect("store:order-summary")
    else:
        return redirect("store:order-summary",slug=slug)


@login_required
def add_from_cart(request, slug):
    food= get_object_or_404(Food, slug=slug)
    order_food, created = OrderFood.objects.get_or_create(
        food=food,
        user=request.user,
        ordered=False
    )
    order_qs=Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order=order_qs[0]

        if order.foods.filter(food__slug=food.slug).exists():
            order_food.quantity+=1
            order_food.save()
        else:
            order.foods.add(order_food)
    return redirect("store:order-summary")
