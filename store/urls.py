
from django.urls import path
#from . import views
from .views import(
    menu,
    add_to_cart,
    remove_from_cart,
    OrderSummaryView,
    CheckoutView,
    PaymentView,
    OrderFinalView,
    add_from_cart,
    home,
    contacts,
    about

)


app_name='store'

urlpatterns = [
    path('', home, name='pizza-home'),
    path('pizza_menu/', menu, name='pizza-menu'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add-to-cart/<slug>/', add_to_cart , name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart , name='remove-from-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-from-cart/<slug>/', add_from_cart , name='add-from-cart'),
    path('pizza_contacts/', contacts, name='pizza-contacts'),
    path('pizza_about/', about, name='pizza-about'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('order-final/', OrderFinalView, name='order-final'),


]
