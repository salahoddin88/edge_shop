from django.shortcuts import render
import razorpay
from rest_framework import viewsets, views, filters, authentication, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from order.models import Order, OrderDetail
from . import serializers
from django.contrib.auth.models import User
from product.models import ProductCategory, Product
from cart.models import Cart
from datetime import datetime


class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserView(viewsets.ModelViewSet):
    serializer_class = serializers.UsersSerializer
    queryset = User.objects.filter(is_superuser=False, is_staff=False)


class ProductCategoryView(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = serializers.ProductCategorySerializer
    queryset = ProductCategory.objects.filter(status=True)


class ProductView(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.filter(status=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ('product_category__id', )
    ordering_fields = ['price']



class CartView(views.APIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.CartSerializer

    def get(self, request):
        queryset = Cart.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            quantity = serializer.validated_data.get('quantity')
            product = serializer.validated_data.get('product')
            cart, _ = Cart.objects.get_or_create(product=product, user=request.user)
            cart.quantity = quantity
            if int(quantity) == 0:
                cart.delete()
            else:
                cart.save()
            return Response({'status' : 'success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cartId=None):
        if cartId:
            try:
                Cart.objects.get(id=cartId).delete()
                return Response({'status' : 'success'})
            except Cart.DoesNotExist:
                return Response({'details' : 'No found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'details' : 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
        

class Checkout(views.APIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cartProducts = Cart.objects.filter(user=request.user)
            subTotal = 0
            total = 0
            shippingCost = 50
            for key, cartProduct in enumerate(cartProducts):
                productTotal = int(cartProduct.quantity) * int(cartProduct.product.price)
                total += productTotal
                subTotal += productTotal

            total = shippingCost + subTotal
            client = razorpay.Client(auth=("rzp_test_DBRMtVnE1JvCM2", "vPRNJ7R1gJKlXvPUriFXqfHC"))
            receipt = f'order_rcptid{request.user.id}'
            data = {"amount": total, "currency": "INR", "receipt": receipt}
            payment = client.order.create(data=data)
            context = {
                'order_id' : payment['id'],
                'subTotal': subTotal,
                'shippingCost': shippingCost,
                'total': total,
            }

            return Response({'status' : 'success', 'data' : context})

        except Exception as e:
            return Response({'details' : str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        
        return Response({'status':'success'})


class OrderView(viewsets.ViewSet):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()

    def list(self, request):
        queryset = Order.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request):
        #NOTE : Need to write individual order details
        pass
