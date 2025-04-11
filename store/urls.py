# bookstore_project/store/urls.py

from django.urls import path
from store import views

# Define an app namespace
app_name = 'store'

urlpatterns = [
    # Book list page (Homepage)
    path('', views.book_list_view, name='book_list'),

    # Add to cart URL
    path('add_to_cart/<int:book_pk>/', views.add_to_cart_view, name='add_to_cart'),

    # Cart detail page
    path('cart/', views.cart_view, name='cart'),

    # Remove from cart URL
    path('remove_from_cart/<int:book_pk>/', views.remove_from_cart_view, name='remove_from_cart'),

    # Clear cart URL
    path('clear_cart/', views.clear_cart_view, name='clear_cart'),

    # Login page
    path('login/', views.login_view, name='login'),

    # Logout URL
    path('logout/', views.logout_view, name='logout'),
]
