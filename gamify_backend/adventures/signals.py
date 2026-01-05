from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scene

@receiver(post_save, sender=Scene)
def update_previous_scene_next_scene(sender, instance, created, **kwargs):
    if created and instance.previous_scene:
        instance.previous_scene.next_scene = instance
        # Deactivate the signals to avoid an infinite loop
        Scene.objects.filter(pk=instance.previous_scene.pk).update(next_scene=instance)