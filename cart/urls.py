from django.urls import path
from .views import CartListView, AddToCartView, ClearCartView, RemoveFromCartView

urlpatterns = [
    path('', CartListView.as_view(), name='cart_detail'),
    path('add/<int:pk>/', AddToCartView.as_view(), name='add_to_cart'),  # Captures product ID as 'pk'
    path('clear/', ClearCartView.as_view(), name='clear_cart'),
    path('remove/<str:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),

]
