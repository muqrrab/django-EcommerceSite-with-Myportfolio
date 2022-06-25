from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.index, name="Home"),
    path('products/', views.allproducts, name="AllProducts"),
    path('products/<str:cat>', views.catproducts, name="CatProduct"),
    path('product/<str:pname>', views.productview, name="Productview"),
    path('checkout/', views.checkout, name="Checkout"),
    path('cart/', views.cart, name="cart"),
    path('search/', views.search, name="search"),
    path('quickview/<str:pname>', views.quickview, name="quickview"),
    path('db', views.dashboard, name="db"),
    # path('about/', views.about, name="About"),
    # path('contact/', views.contact, name="Contact"),
    # path('tracker/', views.index, name="Tracker"),
    # checking ajax
    path('update_item/', views.updateItem, name="update_item"),
    path('header_cart', views.header_cart),
    path('cart_page', views.cart_page),
    path('process_order/', views.processOrder, name='process_order'),

]
