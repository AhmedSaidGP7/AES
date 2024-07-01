from django.urls import path
from . import views

app_name = "college"
urlpatterns = [
    path('', views.index, name='index'),   
    path('courses', views.courses, name='courses'),
    path('faculty_members', views.staff, name='staff'),
    path('contact/', views.contact, name='contact'),

]