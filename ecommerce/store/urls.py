from django.urls import path

from . import views
from .views import searchProduct

urlpatterns = [
	path('', views.store, name="store"),
	path('search/', searchProduct, name="search"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"), 
	path('logout/', views.logoutUser, name="logout"),


	path('contact/', views.contact, name="contact"),
	path('categories/', views.categories, name="categories"),
	path('about/', views.about, name="about"),
	path('new_product/', views.new_product, name="new_product"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]