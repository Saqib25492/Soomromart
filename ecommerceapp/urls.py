from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('checkout', views.checkout, name='checkout'),
    path('payment/<int:id>', views.payment, name='payment'),
    path('thanks/<int:id1>', views.thanks, name='thanks'),
]
