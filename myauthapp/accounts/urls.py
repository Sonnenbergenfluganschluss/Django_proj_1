from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.home, name='home'),
     path('/process_birthday/', views.process_birthday, name='process_birthday'),
     path('/process_city/', views.process_city, name='process_city'),
     path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('accounts/register/', views.register, name='register'),
     path('accounts/profile/', views.profile, name='profile'),
     path('accounts/password_reset/', 
          auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), 
          name='password_reset'),
     path('accounts/password_reset/done/', 
          auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), 
          name='password_reset_done'),
     path('accounts/reset/<uidb64>/<token>/', 
          auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), 
          name='password_reset_confirm'),
     path('accounts/reset/done/', 
          auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
          name='password_reset_complete'),

]