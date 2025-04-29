from django.urls import path

from . import views

urlpatterns = [
  path('check_notifications', views.check_notifications, name='check_notifications'),
  path('get_mails', views.get_mails, name='get_mails'),
  path('delete_msg', views.delete_msg, name='delete_msg'),
]