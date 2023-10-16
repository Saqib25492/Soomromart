from django.shortcuts import render,redirect
from django.contrib import messages
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate, Transaction_details
from math import ceil
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):

    # This will be discussed when we work on different styling mentioned in index.html
    
    # products = Product.objects.all()
    # products_Category = Product.objects.values('category')
    # category = [item['category'] for item in products_Category]
    # category = list(set(category))
    # context = {
    #     'Products' : products,
    #     'Category' : category,
    # }
    
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    # print(cats)
    for cat in cats:
        prod = Product.objects.filter(category = cat).values()
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))    
        allprods.append([prod, range(1,nSlides), nSlides])
    # print(allprods)
    Params = {
         'allProds' : allprods}
    
    return render(request, "index.html",Params)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        phone = request.POST.get('phone')
        
        contact = Contact.objects.create(name = name, email = email, desc = desc, phonenumber = phone)
        contact.save()
        messages.info(request, 'we will get back to you soon!!!')
        return redirect('/contact')
    
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

@login_required(login_url='login')
def checkout(request):
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amt', '')
        
        email = request.POST.get('email', '')
        adrress1 = request.POST.get('adrress1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        
        Order = Orders.objects.create(items_json = items_json, name = name, amount=amount, email=email, address1=adrress1, address2=address2, city=city, state=state, zip_code=zip_code, phone=phone)
        Order.save()
        update = OrderUpdate(order_id = Order.order_id, update_desc = "Order has been placed")
        update.save()
        id = Order.order_id
        # oid = str(id) + "shopycart"
        return redirect(f'/payment/{id}')
        # thank = True

        # id = Order.order_id
        # oid = str(id) + "shopycart"
        # param_dict = {
        #     'MID': Keys.MID,
        #     'ORDER_ID': oid,
        #     'TXN_AMOUNT': str(amount),
        #     'CUST_ID': email,
        #     'INDUSTRY_TYPE_ID': 'Retail',
        #     'CHANNEL_ID': 'WEB',
        #     'CALLBACK_URL': 'http://127.0.0.1:8000/'
        # }
    return render(request, 'checkout.html')
## Payment Integration


def payment(request, id):
    order_id = OrderUpdate.objects.filter(order_id = id).first()
    print(f'ID: {order_id.order_id}')
    
    if request.method == 'POST':
        id1 = request.POST.get('id', order_id.order_id)
        name = request.POST.get('name')
        cardnum = request.POST.get('cardnum')
        date = request.POST.get('date')
        cvv = request.POST.get('cvv')
        print(id1)
        transaction = Transaction_details.objects.create(name=name, card_number = cardnum, valid = date, cvv = cvv)
        transaction.save()
        
        return redirect(f'/thanks/{id1}')
    
    
    return render(request, 'payment.html', {'order':order_id})

    
 
        

def thanks(request, id1):
    order = OrderUpdate.objects.filter(order_id=id1).first()
    return render(request, 'thanks.html', {'order':order})
