from django import forms

PAYMENT_CHOICES= (
    ('S','Stripe'),
    ('P','Paypal')
)

class CheckoutForm(forms.Form):
    payment_option=forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class ContactForm(forms.Form):
    email = forms.EmailField(max_length=100,
                            widget= forms.EmailInput
                           (attrs={'placeholder':'Enter your email'}))
    name = forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Enter your Full Name..'}))
    message = forms.CharField(max_length=100,
                           widget= forms.Textarea
                           (attrs={'placeholder':'Enter your Message here..'}))
