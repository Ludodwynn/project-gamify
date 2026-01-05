from django.urls import path

from . import views


urlpatterns = [
    path('users/', views.index, name='all-users'),
    path('users/<slug:user_slug>', views.user_details, name='user-detail')
]