-Activer le venv :
source venv/bin/activate

(docker-compose down -v   # Arrête et supprime les conteneurs (et volumes si nécessaire))
(docker-compose build     # Rebuild les images)
(docker-compose up)


python manage.py makemigrations
python manage.py migrate

Si tu ne passes pas par Docker pour le développement, lance le serveur Django :
python manage.py runserver

accès API
http://localhost:8000/api/   + endpoints
