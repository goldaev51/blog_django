from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    path('registration/', views.RegistrationFormView.as_view(), name='registration'),

]
