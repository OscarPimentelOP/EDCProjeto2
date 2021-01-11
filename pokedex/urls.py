"""pokedex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from pokeapp import views

urlpatterns = [
    path('', views.index),
    path('pokemon/get', views.pokemonapi),
    path('pokemon/get/', views.pokemonapi),
    path('pokemon/<int:poke_id>', views.pokemon),
    path('about', views.about),
    path('about/', views.about),
    path('builder/', views.builder),
    path('builder/details/', views.get_details),
    path('builder/details', views.get_details),
    path('teams/', views.teams),
    path('teams/create', views.create_team),
    path('teams/create/', views.create_team),
    path('teams/delete', views.delete_team),
    path('teams/delete/', views.delete_team)
]
