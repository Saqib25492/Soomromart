from django.shortcuts import render,redirect
from django.contrib import messages
from ecommerceapp.models import Contact, Product
from math import ceil


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

