from rest_framework import generics, permissions
from .models import Skill, CharacterSkill, Equipment, CharacterEquipment, Enemy
from .serializers import SkillSerializer, CharacterSkillSerializer, EquipmentSerializer, CharacterEquipmentSerializer, EnemySerializer

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]


class SkillDetailView(generics.RetrieveAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.AllowAny]   


class CharacterSkillListView(generics.ListCreateAPIView):
    serializer_class = CharacterSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return CharacterSkill.objects.filter(character__user=self.request.user, character__pk=character_pk)

    def perform_create(self, serializer):
        character_pk = self.kwargs.get('character_pk')
        character = self.request.user.characters.get(pk=character_pk)
        skill_id = self.request.data.get('skill')
        skill = Skill.objects.get(pk=skill_id)
        serializer.save(character=character, skill=skill)


class CharacterSkillDetailView(generics.RetrieveAPIView):
    serializer_class = CharacterSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return CharacterSkill.objects.filter(character__user=self.request.user, character__pk=character_pk)
    

class EquipmentListView(generics.ListAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.AllowAny]


class EquipmentDetailView(generics.RetrieveAPIView):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.AllowAny]


class CharacterEquipmentListView(generics.ListCreateAPIView):
    serializer_class = CharacterEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return CharacterEquipment.objects.filter(character__user=self.request.user, character__pk=character_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['character'] = self.request.user.characters.get(pk=self.kwargs.get('character_pk'))
        return context

    def perform_create(self, serializer):
        character_pk = self.kwargs.get('character_pk')
        character = self.request.user.characters.get(pk=character_pk)
        serializer.save(character=character)

class CharacterEquipmentDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = CharacterEquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return CharacterEquipment.objects.filter(character__user=self.request.user, character__pk=character_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['character'] = self.request.user.characters.get(pk=self.kwargs.get('character_pk'))
        return context
    

class EnemyListView(generics.ListAPIView):
    queryset = Enemy.objects.all()
    serializer_class = EnemySerializer
    permission_classes = [permissions.AllowAny]

class EnemyDetailView(generics.RetrieveAPIView):
    queryset = Enemy.objects.all()
    serializer_class = EnemySerializer
    permission_classes = [permissions.AllowAny]