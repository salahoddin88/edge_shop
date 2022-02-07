from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from cart.models import Cart
from order.models import Order, OrderDetail
from payment.models import Payment
from product.models import ProductCategory
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import razorpay

@method_decorator(login_required, name="dispatch")
class AddToCart(View):
    
    def post(self, request):
        quantity = request.POST.get('quantity')
        product_id = request.POST.get('product_id')
        cart, created = Cart.objects.get_or_create(product_id=product_id, user_id=request.user.id)
        if created:
            cart.quantity = quantity
        else:
            cart.quantity = int(quantity) + int(cart.quantity)
        cart.save()
        # try:
        #     cart = Cart.objects.get(product_id=product_id, user_id=request.user.id)
        #     cart.quantity = int(quantity) + int(cart.quantity)
        #     cart.save()
        # except Cart.DoesNotExist:
        #     Cart.objects.create(
        #         quantity=quantity,
        #         product_id=product_id,
        #         user=request.user
        #     )
        return redirect('ProductDetails', product_id=product_id)


@method_decorator(login_required, name="dispatch")
class MyCart(View):

    template_name = 'my-cart.html'

    def get(self, request):
        navigationProductCategories = ProductCategory.objects.filter(status=True)
        carts = Cart.objects.filter(user=request.user)
        cartData = {}
        subTotal = 0
        shippingCost = 50
        total = 0
        for key, cart in enumerate(carts):
            productTotal = int(cart.product.price) * int(cart.quantity)
            subTotal += productTotal
            cartData[key] = {
                'product_image' : cart.product.cover_image,
                'product_name' : cart.product.name,
                'product_price' : cart.product.price,
                'quantity' : cart.quantity,
                'product_total' : productTotal,
                'cart_id' : cart.id
            }
        
        
        total = subTotal + shippingCost
        context = {
            'navigationProductCategories' : navigationProductCategories,
            'carts' : list(cartData.values()),
            'subTotal' : subTotal,
            'shippingCost' : shippingCost,
            'total' : total
        }
        return render(request, self.template_name, context)


    def post(self, request):
        
        cart_id_list = request.POST.getlist('cart_id')
        quantity_list = request.POST.getlist('quantity')
        
        for index, cart_id in enumerate(cart_id_list):
            try:
                cartObject = Cart.objects.get(id=cart_id)
                if int(quantity_list[index]) == 0:
                    cartObject.delete()
                else:
                    cartObject.quantity = quantity_list[index]
                    cartObject.save()
            except Cart.DoesNotExist:
                pass

        return redirect('MyCart')
        

# @method_decorator(login_required, name="dispatch")
# class Checkout(View):
#     template_name = 'checkout.html'

#     def get(self, request):
#         navigationProductCategories = ProductCategory.objects.filter(status=True)
#         carts = Cart.objects.filter(user=request.user)
#         cartData = {}
#         subTotal = 0
#         shippingCost = 50
#         total = 0
#         for key, cart in enumerate(carts):
#             productTotal = int(cart.product.price) * int(cart.quantity)
#             subTotal += productTotal
#             cartData[key] = {
#                 'product_name' : cart.product.name,
#                 'product_total' : productTotal,
#             }
        
#         total = subTotal + shippingCost
#         context = {
#             'navigationProductCategories' : navigationProductCategories,
#             'carts' : list(cartData.values()),
#             'subTotal' : subTotal,
#             'shippingCost' : shippingCost,
#             'total' : total
#         }
#         return render(request, self.template_name, context)



@method_decorator(login_required, name='dispatch')
class Checkout(View):
    template_name = 'checkout.html'

    def get(self, request):
        navigationProductCategories = ProductCategory.objects.filter(status=True)
        cartProducts = Cart.objects.filter(user=request.user)
        carts = {}
        subTotal = 0
        total = 0
        shippingCost = 50
        for key, cartProduct in enumerate(cartProducts):
            productTotal = int(cartProduct.quantity) * int(cartProduct.product.price)
            total += productTotal
            subTotal += productTotal
            carts[key] = {
                'product_name': cartProduct.product.name,
                'productTotal': productTotal,
            }

        total = shippingCost + subTotal
        cartData = list(carts.values())
        context = {
            'navigationProductCategories': navigationProductCategories,
            'carts': cartData,
            'subTotal': subTotal,
            'shippingCost': shippingCost,
            'total': total,
        }
        return render(request, self.template_name, context)

    def post(self, request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        cartProducts = Cart.objects.filter(user=request.user)
        subTotal = 0
        total = 0
        shippingCost = 50
        for key, cartProduct in enumerate(cartProducts):
            productTotal = int(cartProduct.quantity) * int(cartProduct.product.price)
            total += productTotal
            subTotal += productTotal
        total = (shippingCost + subTotal) * 100

        client = razorpay.Client(auth=("rzp_test_DBRMtVnE1JvCM2", "vPRNJ7R1gJKlXvPUriFXqfHC"))
        receipt = f'order_rcptid{request.user.id}'
        data = {"amount": total, "currency": "INR", "receipt": receipt}
        payment = client.order.create(data=data)
        
        if payment.get('id'):
            context = {
                'order_id': payment['id'],
                'amount': payment['amount'],
                'first_name' : first_name,
                'last_name' : last_name,
                'address' : address,
            }
            return render(request, 'capture-payment.html', context)



class PaymentSuccess(View):
    def post(self, request):
        razorpay_payment_id  = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        cartProducts = Cart.objects.filter(user=request.user)

        if cartProducts:
            order = Order.objects.create(
                user = request.user,
                name=f'{first_name} {last_name}',
                address = address,
                razor_pay_order_id=razorpay_order_id,
                date_time=datetime.now()

            )
            for cartProduct in cartProducts:
                OrderDetail.objects.create(
                    order=order,
                    product=cartProduct.product,
                    quantity=cartProduct.quantity,
                    price=cartProduct.product.price,
                )
            cartProducts.delete()
        
        return JsonResponse({'status':'success'})



@csrf_exempt
def RazorpayWebhook(request):
    requestBody = json.load(request.body.decode('utf-8'))
    payload = requestBody['payload']
    if payload['payment']:
        order_id = payload['payment']['entity']['order_id']
        try:
            order = Order.objects.get(razor_pay_order_id=order_id)
            payment = Payment.objects.get_or_create(order=order)
            payment.payment_id=payload['payment']['entity']['id']
            payment.payment_status=payload['payment']['entity']['status']
            payment.payment_method=payload['payment']['entity']['method']
            payment.created_at=payload['payment']['entity']['created_at']
            payment.amount=payload['payment']['entity']['amount']
            payment.save()
            order.payment_status=True
            order.save()
            return JsonResponse({'status':'success'})
        except:
            return JsonResponse({'status':'failed'})


def ThankYou(request):
    return HttpResponse('<h1>Thank You, Your order has been placed! </h1>')