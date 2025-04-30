from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('receipes/', views.receipes, name='receipes'),
    path('update/<int:id>/', views.update_receipe, name='update_receipe'),
    path('delete/<int:id>/', views.delete_receipe, name='delete_receipe'),
]
