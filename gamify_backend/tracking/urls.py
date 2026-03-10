from django.urls import path
from .views import ActivityListView, ActivityDetailView, ActivityTypeListView

urlpatterns = [
    path('activity-types/', ActivityTypeListView.as_view(), name='activity-type-list'),
    path('characters/<int:character_pk>/activities/', ActivityListView.as_view(), name='activity-list'),
    path('characters/<int:character_pk>/activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
]