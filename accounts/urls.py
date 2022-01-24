from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="Login"),
    path('logout', views.logout, name="logout"),
]
