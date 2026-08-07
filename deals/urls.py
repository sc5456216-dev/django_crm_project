from django.urls import path
from . import views

urlpatterns = [
    path('', views.deal_list, name='deal_list'),
    path('pipeline/', views.deal_pipeline, name='deal_pipeline'),
    path('create/', views.deal_create, name='deal_create'),
    path('<int:pk>/', views.deal_detail, name='deal_detail'),
    path('<int:pk>/update/', views.deal_update, name='deal_update'),
    path('<int:pk>/delete/', views.deal_delete, name='deal_delete'),
    path('<int:pk>/change-stage/', views.deal_change_stage, name='deal_change_stage'),
]
