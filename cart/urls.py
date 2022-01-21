from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart', views.AddToCart.as_view(), name="AddToCart"),
]
