from django.urls import path

from .views import *


urlpatterns = [
    # http://127.0.0.1:8000/user-management/users-list/
    path('users-list/', get_users_list, name='get users list'),

    # http://127.0.0.1:8000/user-management/add-user/
    path('add-user/', add_user, name='add user'),

    # http://127.0.0.1:8000/user-management/show-user/1/
    path('show-user/<str:identifier>/', show_user, name='show user'),

    # http://127.0.0.1:8000/user-management/edit-user/1/
    path('edit-user/<str:identifier>/', edit_user, name='edit user'),

    # http://127.0.0.1:8000/user-management/delete-user/1/
    path('delete-user/<str:identifier>/', delete_user, name='delete user'),
]
