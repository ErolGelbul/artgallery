from django.urls import path
from . import views 

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.profiles, name="profiles"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('account/', views.userAccount, name="account"),

    path('edit-account/', views.editAccount, name="edit-account"),
    
    path('create-skill/', views.create_skill, name="create-skill"),
    path('update-skill/<str:pk>/', views.update_skill, name="update-skill"),
    path('delete-skill/<str:pk>/', views.delete_skill, name="delete-skill"),

    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.view_message, name="message"),
    path('send-message/<str:pk>/', views.create_message, name="create-message"),
]