from django.urls import path
from . import views

app_name= 'klub_alarm'

urlpatterns = [
    path('', views.alarm_test_page, name='alarm_test'),
    path('trigger/', views.trigger_alarm, name='trigger_alarm'),
]