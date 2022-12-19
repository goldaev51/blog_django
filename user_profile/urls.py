from django.urls import path

from . import views

app_name = 'user_profile'
urlpatterns = [
    path('user/<int:pk>', views.UserPublicProfile.as_view(), name='user-data'),
    path('my-profile/', views.show_user_profile, name='user-profile'),
    path('update-profile/', views.update_user_profile, name='update-profile'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
]
