from django.shortcuts import render

from rest_framework import generics, permissions
from .models import Adventure, AdventureProgress, Scene, SceneChoice
from .serializers import AdventureProgressCreateSerializer, AdventureProgressSerializer, AdventureSerializer, SceneChoiceSerializer, SceneSerializer

class AdventureListView(generics.ListCreateAPIView):
    queryset = Adventure.objects.filter(is_published=True)
    serializer_class = AdventureSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    

class AdventureDetailView(generics.RetrieveAPIView):
    queryset = Adventure.objects.all()
    serializer_class = AdventureSerializer
    permission_classes = [permissions.AllowAny]


class SceneListView(generics.ListAPIView):
    serializer_class = SceneSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        adventure_pk = self.kwargs.get('adventure_pk')
        return Scene.objects.filter(adventure__pk=adventure_pk)
    

class SceneDetailView(generics.RetrieveAPIView):
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer
    permission_classes = [permissions.AllowAny]


class SceneChoiceListView(generics.ListAPIView):
    serializer_class = SceneChoiceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        scene_pk = self.kwargs.get('scene_pk')
        return SceneChoice.objects.filter(scene__pk=scene_pk)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['character'] = self.request.user.characters.first() if self.request.user.is_authenticated else None
        return context
    

class AdventureProgressListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return AdventureProgress.objects.filter(character__user=self.request.user, character__pk=character_pk)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AdventureProgressCreateSerializer
        return AdventureProgressSerializer

    def perform_create(self, serializer):
        character_pk = self.kwargs.get('character_pk')
        character = self.request.user.characters.get(pk=character_pk)
        serializer.save(character=character)

class AdventureProgressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AdventureProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return AdventureProgress.objects.filter(character__user=self.request.user, character__pk=character_pk)
