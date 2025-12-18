
# Créer un nouveau projet avec Django : 
python -m django startproject antilope

Crée un dossier antilope/antilope

# Créer une application dans le projet Django

On lance le fichier manage.py : 
python manage.py startapp api

Crée alors le dossier antilope/api

# Configurer la base de donnée

On définit les modèles dans models.py.
Puis `python manage.py makemigrations`
Puis 
Puis `python manage.py migrate`
pour créer les fichiers de migration (construire la bdd)


python manage.py runserver