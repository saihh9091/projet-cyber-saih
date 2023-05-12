# Projet Hossein Saihi
Ce script Python permet d'effectuer une recherche approfondie d'informations sur un domaine spécifique. Il utilise diverses techniques telles que la résolution DNS, l'analyse NMAP, le scrapping de données, le dorking et la recherche d'adresses e-mail associées au domaine. Le script est conçu pour aider les utilisateurs à obtenir des informations pertinentes sur un domaine donné et analysé ses vulnérabilités potentielles.

### Fonctionnalités du script
Le script comprend les principales fonctionnalités suivantes :

- Résolution de l'URL en adresse IP : Le script utilise la résolution DNS pour convertir l'URL cible en adresse IP correspondante.

- Analyse NMAP : Le script exécute une analyse NMAP sur l'URL cible pour obtenir des informations sur les ports, les services et les versions des logiciels en cours d'exécution.

- Scrapping de données sur LinkedIn : Le script effectue une recherche sur Google pour trouver des profils LinkedIn associés au nom de domaine cible. Il extrait les résultats de recherche contenant le titre et le lien vers les profils LinkedIn.

- Recherche d'adresses e-mail : Le script utilise différentes sources (Google, Bing, Baidu) pour rechercher des adresses e-mail liées au domaine cible. Il extrait les adresses e-mail trouvées et les affiche à l'écran.

- Envoi du rapport complet par e-mail : Le script permet à l'utilisateur de spécifier une adresse e-mail où le rapport complet sera envoyé. Le rapport inclut les résultats des différentes recherches effectuées et est envoyé en tant que pièce jointe dans un e-mail.



### Déploiement

Pour déployer ce projet

```bash
  git clone https://github.com/hossein-saihi
  cd hossein-saihi
  chmod +x installation.sh 
  ./installation.sh 

```

### Utilisation

```bash
   python3 main.py
```
### Dépendances

Voici la liste des dépendances PIP (https://pypi.org/)
- subprocess (https://pypi.org/project/subprocess.run/)
- socket (https://pypi.org/project/sockets/)
- emailfinder (https://pypi.org/project/emailfinder/)
- colorama (https://pypi.org/project/colorama/)
- requests (https://pypi.org/project/requests/)
- bs4 (https://pypi.org/project/beautifulsoup4/)

