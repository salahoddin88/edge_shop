from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart', views.AddToCart.as_view(), name="AddToCart"),
    path('my-cart', views.MyCart.as_view(), name="MyCart"),
    path('checkout', views.Checkout.as_view(), name="Checkout")
]
