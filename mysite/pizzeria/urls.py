from django.urls import path

from .views import index, menu_view, pizza_detail, order_view, contacts


urlpatterns = [
    path('', index, name='home'),
    path('menu/', menu_view, name='menu'),
    path('pizza/<path:slug>/', pizza_detail, name='pizza_detail'),

    # заказ
    path('pizza/<slug:slug>/order/', order_view, name='order_pizza'),

    # контакты
    path('contacts/', contacts, name='contacts'),
]