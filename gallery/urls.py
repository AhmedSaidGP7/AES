from django.urls import path
from . import views

app_name = "gallery"
urlpatterns = [
    path('', views.index, name='index'),
    path('sell', views.sell_artwork, name="sell"),
    path('artwork/<int:artwork_id>/', views.artwork_detail, name='artwork_detail'),
]