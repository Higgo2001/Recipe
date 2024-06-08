# accounts/urls.py

from django.urls import path
from .views import register_view, login_view, logout_view#,insert_recipe

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('insert_recipe_view/', insert_recipe, name='insert_recipe'),

]
