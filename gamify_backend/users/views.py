from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import User, Character
from .serializers import UserSerializer, CharacterSerializer

User = get_user_model()

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

class UserDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Always return the authenticated user
        return self.request.user

    def perform_destroy(self, instance):
        # Deactivate user instead of deleting it
        instance.is_active = False
        instance.save()

class CharacterListView(generics.ListCreateAPIView):
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only returns characters from the authenticated user
        return Character.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically associate the character to the authenticated user
        serializer.save(user=self.request.user)

class CharacterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only returns characters from the authenticated user
        return Character.objects.filter(user=self.request.user)