from django.urls import path

from .views import order, order_id, payment

urlpatterns = [
    path('orders/', order, name='order'),
    path('order/<int:id>/', order_id, name='order_id'),
    path('payment/<int:id>/', payment, name='payment'),
]