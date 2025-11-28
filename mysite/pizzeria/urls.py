from .views import pizza_detail
from django.urls import path
from . import views
from django.urls import re_path
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='home'),
    path('menu/', views.menu_view, name='menu'),

    # 🔥 Детальная страница пиццы
    re_path(r"^pizza/(?P<slug>[\w-]+)/$", views.pizza_detail, name="pizza_detail"),

    # 🔥 Добавление в корзину (с кириллицей)
    re_path(r"^cart/add/(?P<slug>[\w-]+)/$", views.add_to_cart, name="add_to_cart"),

    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('account/', views.account, name='account'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("account/orders/", views.user_orders, name="user_orders"),


]