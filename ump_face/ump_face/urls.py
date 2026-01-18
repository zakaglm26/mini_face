"""
URL configuration for ump_face project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ump_app import views
from django.views.generic import RedirectView
urlpatterns = [
    # Administration Django
    path('admin/', admin.site.urls, name='admin'),
    
    # Redirection de la racine vers login
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    
    # Page de connexion
    path('login/', views.login, name='login'),
    
    # Page d'inscription ← NOUVELLE ROUTE
    path('register/', views.register, name='register'),
    
    # Page d'accueil (protégée)
    path('welcome/', views.welcome, name='welcome'),

    # Page de profil utilisateur (protégée)
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'), 
    
    # Page de modification du profil (protégée)
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Ajouter des amis (protégée)
    path('friends/add/<int:user_id>/', views.add_friend, name='add_friend'),  

    # Supprimer des amis (protégée)
    
    # Recherche d'utilisateurs (protégée)
    path('search/', views.search_users, name='search_users'),  

    # Déconnexion
    path('logout/', views.logout, name='logout'),


]
