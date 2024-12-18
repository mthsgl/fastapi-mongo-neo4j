# API MongoDB et Neo4j

## Installation 

1) Récupérer les fichiers dans un dossier
2) Ouvrir un terminal dans le dossier puis pour installer l'environnement virtuel taper :
   ` python -m venv env-arangodb-fastapi `
3) Accéder à l'environnement : `.\env-arangodb-fastapi\Scripts\Activate.ps1`
4) Installer toutes les dépendances : `pip install -r requirements.txt`
5) Lancer l'API : `python -m uvicorn main:app --reload`
6) Accéder au swagger : http://127.0.0.1:8000/docs 
