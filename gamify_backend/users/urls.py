from django.urls import path
from .views import UserDetailView, UserDeleteView, CharacterListView, CharacterDetailView

urlpatterns = [
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
    path('users/me/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('characters/', CharacterListView.as_view(), name='character-list'),
    path('characters/<int:pk>/', CharacterDetailView.as_view(), name='character-detail'),
]