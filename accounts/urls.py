from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),

    path('register/', views.register,name='register'),

    path('success',views.success,name="success"),

    path('logout',views.logout,name="logout"),

    path('delete/<int:user_id>',views.delete,name="delete"),

    path('edit/<int:user_id>/', views.edit, name='edit'),


    
]