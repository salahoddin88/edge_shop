from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserView)
router.register('product-category', views.ProductCategoryView)
router.register('products', views.ProductView),
router.register('orders', views.OrderView)


urlpatterns = [
    path('login', views.LoginView.as_view()),
    path('carts', views.CartView.as_view()),
    path('carts/<int:cartId>', views.CartView.as_view()),
    path('checkout', views.Checkout.as_view()),
    path('', include(router.urls))
]
