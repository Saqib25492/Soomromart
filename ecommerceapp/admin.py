from django.contrib import admin
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate, Transaction_details
# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(Transaction_details)