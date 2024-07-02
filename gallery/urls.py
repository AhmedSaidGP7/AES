from django.urls import path
from . import views

app_name = "gallery"
urlpatterns = [
    path('', views.index, name='index'),
    path('sell', views.sell_artwork, name="sell"),
    path('artwork/<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
    path('cart', views.view_cart, name='cart'),
    path('add_to_cart/<int:artwork_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:artwork_id>/', views.remove_from_cart, name='remove_from_cart'),


]