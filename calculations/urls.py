from django.urls import path,include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.landing_page, name='landing_page'),  # Landing page
    path('calculate/', views.calculate, name='calculate'),
    # Other routes
    path('download-pdf/', views.download_pdf, name='download_pdf'),
]
