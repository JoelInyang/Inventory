from django.urls import path
from . import views


urlpatterns = [
    
    ##Regular users urls
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('products/', views.ProductListView.as_view(), name='product-list'),    
    path('orders-create/', views.OrderCreateView.as_view(), name='order-create'),
    
    
    
    ##Admin urls
    path('admin-login/', views.AdminLoginView.as_view(), name='login'),
    path('products-create/', views.ProductCreateView.as_view(), name='product-create'),
    path('products-update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('products-delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-delete'),
    path('orders-update-status/<int:pk>/', views.OrderStatusUpdateView.as_view(), name='order-status-update'),


]