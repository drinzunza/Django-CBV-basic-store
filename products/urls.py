from django.urls import path
from .views import ProductListView, ProductDetailView, LikeProductView, CategoryListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('categories', CategoryListView.as_view(), name='categories'),
    path('/category/<str:category>/', ProductListView.as_view(), name='product_list_by_category'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('like/<int:product_id>/', LikeProductView.as_view(), name='like_product')
]
