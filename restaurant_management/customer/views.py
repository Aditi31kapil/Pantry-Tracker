from django.shortcuts import render,redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem,Category,OrderModel
import json

# Create your views here.
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request,'index.html')
    
class About(View):
    def get(self, request, *args, **kwargs):
        return render(request,'about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        
        #get every item from each category 
        Burger = MenuItem.objects.filter(category__name__contains='Burger')
        Pizza = MenuItem.objects.filter(category__name__contains='Pizza')
        Pasta = MenuItem.objects.filter(category__name__contains='Pasta')
        Fries = MenuItem.objects.filter(category__name__contains='Fries')


    #pass into context
        context = {
            'Burger': Burger,
            'Pizza' : Pizza,
            'Pasta' : Pasta,
            'Fries' : Fries,
    
            }

    # render the template
        return render(request, 'order.html', context)
    

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        order_items = {
            'items' : []
        }
        
        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk= int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,    
            }    
            order_items['items'].append(item_data)   

            price = 0
            item_ids = []
            
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])    

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            state=state,
            city=city,
            zip_code=zip_code,
            )


        order.items.add(*item_ids)  

        #After Everything is done, send Confirmation email to the user
        body = ('Thank you for yor order! Your Food is being made and will be delivered soon! \n'
                f'Your total: {price}\n'
                'Thank You again for your order! ')

        send_mail(
            "Thank you For Your Order!",
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )  
        context = {
            'items': order_items['items'],
            'price': price
        }    
        return redirect('order-confirmation', pk=order.pk)

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }  

        return render(request, 'order_confirmation.html', context)
    

    def post(self,request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self,request, pk, *args, **kwargs):
        return render(request, 'order_pay_confiramtion.html')
