from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='products'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('cart/add/<int:pk>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/remove/<int:pk>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/delete/<int:pk>/', views.CartDeleteView.as_view(), name='cart_delete'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
]