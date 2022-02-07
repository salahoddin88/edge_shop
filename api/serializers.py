from dataclasses import field
from rest_framework import serializers
from django.contrib.auth.models import User
from order.models import Order
from product.models import ProductCategory, Product
from cart.models import Cart


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'email'
        ]
        extra_kwargs = {
            'password' : {'write_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


    def update(self, instance, validated_data):
        # Note: override this for user update
        print(instance)
        print(validated_data)
        return instance


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'product_category',
            'name',
            'price',
            'description',
            'cover_image'
        ]
        depth = 1


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'