from rest_framework import generics, permissions
from .models import Activity, ActivityType
from .serializers import ActivitySerializer, ActivityTypeSerializer

class ActivityTypeListView(generics.ListAPIView):
    queryset = ActivityType.objects.all()
    serializer_class = ActivityTypeSerializer
    permission_classes = [permissions.AllowAny]  # Everybody can see the list

class ActivityListView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return Activity.objects.filter(character__user=self.request.user, character__pk=character_pk)

    def perform_create(self, serializer):
        character_pk = self.kwargs.get('character_pk')
        character = self.request.user.characters.get(pk=character_pk)
        serializer.save(character=character)
        
class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        character_pk = self.kwargs.get('character_pk')
        return Activity.objects.filter(character__user=self.request.user, character__pk=character_pk)
