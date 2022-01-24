from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name="HomePage"),
    path('product-listing', views.ProductListing.as_view(), name="ProductListing"),
    path('product-listing/<int:product_category_id>', views.ProductListing.as_view(), name="ProductListing"),
    path('product-details/<int:product_id>', views.ProductDetails.as_view(), name="ProductDetails")
]
