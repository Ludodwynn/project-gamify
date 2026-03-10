from django.urls import path
from .views import (
    SkillListView, SkillDetailView,
    CharacterSkillListView, CharacterSkillDetailView,
    EquipmentListView, EquipmentDetailView,
    CharacterEquipmentListView, CharacterEquipmentDetailView,
    EnemyListView, EnemyDetailView,
)

urlpatterns = [
    # URLs pour Skill
    path('skills/', SkillListView.as_view(), name='skill-list'),
    path('skills/<int:pk>/', SkillDetailView.as_view(), name='skill-detail'),

    # URLs pour CharacterSkill
    path('characters/<int:character_pk>/skills/', CharacterSkillListView.as_view(), name='character-skill-list'),
    path('characters/<int:character_pk>/skills/<int:pk>/', CharacterSkillDetailView.as_view(), name='character-skill-detail'),

    # URLs pour Equipment
    path('equipments/', EquipmentListView.as_view(), name='equipment-list'),
    path('equipments/<int:pk>/', EquipmentDetailView.as_view(), name='equipment-detail'),

    # URLs pour CharacterEquipment
    path('characters/<int:character_pk>/equipments/', CharacterEquipmentListView.as_view(), name='character-equipment-list'),
    path('characters/<int:character_pk>/equipments/<int:pk>/', CharacterEquipmentDetailView.as_view(), name='character-equipment-detail'),

    # URLs pour Enemy
    path('enemies/', EnemyListView.as_view(), name='enemy-list'),
    path('enemies/<int:pk>/', EnemyDetailView.as_view(), name='enemy-detail'),
]