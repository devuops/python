## les choix d'architecture:
- utilisation de sqllite comme base de donnée
- utilisation de panda pour importer de csv ( pratique)
- utilisation de SQLMODEL (en surcharge de SQLLACHEMY)

## pour le lancemenet :
````python
pip install -r requirements.txt
python main.py
````
dés que l'application est lancé, le swagger est disponible sous:
`````http request
http://127.0.0.1:8000/docs
`````
## ajout de test d'intégration
voir le fichier test_main.http


#Utilisation de pycharm comme IDE pour le developpement.