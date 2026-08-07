from django.urls import path
from . import views

<<<<<<< HEAD
urlpatterns = [

    path(
        "",
        views.notification_list,
        name="notification_list"
    ),

    path(
        "<int:pk>/read/",
        views.mark_as_read,
        name="mark_notification"
    ),

    path(
        "<int:pk>/delete/",
        views.delete_notification,
        name="delete_notification"
    ),

=======
app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:pk>/mark-read/', views.mark_notification, name='mark_notification'),
    path('<int:pk>/delete/', views.delete_notification, name='delete_notification'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
>>>>>>> samir
]