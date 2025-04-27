from django.urls import path
from .views import register, logins, profile, logoutt, post_profile_password, post_profile_avatar, get_images

urlpatterns = [
    path('sign-up/', register, name='register'),
    path('sign-in/', logins, name='login'),
    path('sign-out/', logoutt, name='logout'),
    path('profile/', profile, name='profile'),
    path('sign-in/profile/', profile, name='profiles'),
    path('profile/password/', post_profile_password, name='password'),
    path('profile/avatar/', post_profile_avatar, name='avatar'),
    # path ('profile/<str:filename>', get_images, name='filename')
]