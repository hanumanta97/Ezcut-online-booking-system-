from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index2", views.index2, name="index2"),
    path("backtobase", views.backtobase, name="backtobase"),
    path("buisness_list", views.buisness_list, name="buisness_list"),
    path("sign_in_form", views.sign_in_form, name="sign_in_form"),
    path("CreateUser", views.CreateUser, name="CreateUser"),
    path("checkUser", views.checkUser, name="checkUser"),
    path("images_reder", views.images_reder, name="images_reder"),
    path("buisness_list", views.buisness_list, name="buisness_list"),
    path('filtered-profiles/', views.filtered_profile_view, name='filtered_profile_view'),
    path("Createbuisness", views.Createbuisness, name="Createbuisness"),
    path("buisness_list", views.buisness_list, name="buisness_list"),
    path('signout/', views.signout, name='signout'),
    path('get_shops', views.get_shops, name='get_shops'),
    path('get_shop_datails', views.get_shop_datails, name='get_shop_datails'),
    path('get_review', views.get_review, name='get_review'),
]