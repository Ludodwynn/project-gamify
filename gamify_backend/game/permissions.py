from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin to modify skills.
    """
    def has_permission(self, request, view):
        # Autorise les requêtes en lecture pour tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Autorise les requêtes en écriture uniquement pour les administrateurs
        return request.user and request.user.is_staff