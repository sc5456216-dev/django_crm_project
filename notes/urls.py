from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('add/', views.note_create, name='note_create'),
    path('<int:pk>/update/', views.note_update, name='note_update'),
    path('<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('dashboard-create/', views.dashboard_note_create, name='dashboard_note_create'),
]
