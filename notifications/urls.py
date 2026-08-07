from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:pk>/mark-read/', views.mark_notification, name='mark_notification'),
    path('<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]
