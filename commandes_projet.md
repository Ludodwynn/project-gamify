-Activer le venv :
source venv/bin/activate

(docker-compose down -v   # Arrête et supprime les conteneurs (et volumes si nécessaire))
(docker-compose build     # Rebuild les images)
(docker-compose up)


python manage.py makemigrations
python manage.py migrate

Si tu ne passes pas par Docker pour le développement, lance le serveur Django :
python manage.py runserver

tests :
python manage.py test nomDuModule.tests.nomDuFichierTest

accès API
http://localhost:8000/api/   + endpoints

JWT :
req - Authorization: Bearer <access_token>
{
    "username": "mon_utilisateur",
    "password": "mon_mot_de_passe"
}

res
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}




Journal de bord : 
Si on commente la logique de leveling up dans le save du model Character (module users), le test fonctionne, mais plus ceux du module users
EDIT 1: Il semblerait que je n'arrive pas à faire passer l'xp générée par l'ajout d'une activité, au character, dans les tests serializers du module tracking. (il y a de la logique présente dans le model Character du module users, dans le services.py du même module, mais aussi le model Activity du module tracking)
-L'XP n'est pas ajoutée au personnage : Malgré la création d'une activité, l'XP n'est pas ajoutée au personnage, ce qui signifie que la méthode save du modèle Activity ne met pas à jour correctement le personnage.
-Logique de mise à jour de l'XP : La logique de mise à jour de l'XP dans le modèle Activity doit être vérifiée et corrigée.
Revoir les logiques de mise à jour d'xp depuis le départ ?

La mise à jour d'xp fonctionne, mais les tests serializers du module tracking est toujours curieuse. Quand je commente les ligne de création d'activity dans le setup, ça ne fonctionne pas 0 != 300, mais quand je décommente, je pars à 360 != 300. Donc il y a un souci dans les test j'imagine. A revoir


26/02 :
Ok pour le module game.
Module tracking : petit souci sur les tests des serializers, mais rien de bien méchant.

09/03 :
Module tracking fixed pour le souci de test des serializers. C'était un souci de sauvegarde.
Les quatre modules sont terminés pour le premier jet, les tests sont terminés et tous OK pour l'instant. 
Essayer de voir pour gérer des erreurs personnalisées + tokens pour l'auth
Commencer à se diriger sur le frontend.




