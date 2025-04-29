from django.urls import path

from . import views

urlpatterns = [
    path("set_appointment", views.set_appointment, name="set_appointment"),
    path("get_shoptemplates", views.get_shoptemplates, name="get_shoptemplates"),
    path("conformation", views.conformation, name="conformation"),
    path("settel_appointment", views.settel_appointment, name="settel_appointment"),
]