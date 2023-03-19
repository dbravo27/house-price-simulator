from django.urls import path
from . import views

app_name = 'house_price_app'

urlpatterns = [
    path('', views.input_form_view, name='input_form'),
    path('calculate_estimate/', views.calculate_estimate, name='calculate_estimate'),
]

