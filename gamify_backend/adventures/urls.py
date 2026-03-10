from django.urls import path
from .views import (
    AdventureListView, AdventureDetailView,
    SceneListView, SceneDetailView,
    SceneChoiceListView,
    AdventureProgressListView, AdventureProgressDetailView,
)

urlpatterns = [
    path('adventures/', AdventureListView.as_view(), name='adventure-list'),
    path('adventures/<int:pk>/', AdventureDetailView.as_view(), name='adventure-detail'),
    path('adventures/<int:adventure_pk>/scenes/', SceneListView.as_view(), name='scene-list'),
    path('adventures/<int:adventure_pk>/scenes/<int:pk>/', SceneDetailView.as_view(), name='scene-detail'),
    path('scenes/<int:scene_pk>/choices/', SceneChoiceListView.as_view(), name='scene-choice-list'),
    path('characters/<int:character_pk>/adventure-progress/', AdventureProgressListView.as_view(), name='adventure-progress-list'),
    path('characters/<int:character_pk>/adventure-progress/<int:pk>/', AdventureProgressDetailView.as_view(), name='adventure-progress-detail'),
]