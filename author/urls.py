from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),

    path('login/', views.LoginView.as_view(), name='user_login'),
    # path('profile/', views.profile, name='profile'),

    path('user_logout/', views.user_logout, name='user_logout'),

    path('profile/edit_profile/change_pass/',
         views.change_pass, name='change_pass'),
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    path('chseck/', views.checkmail, name='check'),
    path('profile/<str:username>/', views.profile, name='profile'),
]
