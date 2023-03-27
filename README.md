# Tournoi-Echecs
Application pour gérer les tournois d'échecs hors ligne

# Objectifs:
 - Créer un programme qui suit le modèle de conception modèle-vue-contrôleur MVC (tournoi, tour, match et joueur)
 - Utilisez des outils tels que flake8, Black ou Isort comme wrapper de code qui vérifie le code selon PEP8.
 - Un programme où les règlements des tournois suisses doivent être strictement suivis et un programme qui pourrait :
 - Créer un tournoi, joueurs
 - Un match entre joueurs à chaque tour
 - Enregistrer les données dans des fichiers .json , ils doivent être mis à jour à chaque fois qu'une modification est apportée
aux données afin d'éviter toute perte
 - utiliser un menu principal pour effectuer des actions
 
 Générer des rapports :
● liste de tous les joueurs par ordre alphabétique ;
● liste de tous les tournois ;
● nom et dates d’un tournoi donné ;
● liste des joueurs du tournoi par ordre alphabétique ;
● liste de tous les tours du tournoi et de tous les matchs du tour.

# GÉNÉRATION DES PAIRES
● Au début du premier tour, les joueurs sont mélangés de façon aléatoire.
● Chaque tour est généré dynamiquement en fonction des résultats des joueurs dans
le tournoi en cours.
○ Les joueurs sont triés en fonction de leur nombre total de points dans le
tournoi.
○ Les joueurs sont associés dans l’ordre (le joueur 1 avec le joueur 2, le joueur 3
avec le joueur 4 et ainsi de suite.)
si le joueur 1 a déjà joué contre le joueur 2,
il est plutôt associé au joueur 3.
● les points de tous les joueurs sont mis à jour après chaque tour et le
processus de triage et d’association est répété jusqu'à ce que le tournoi soit terminé.
● Un tirage au sort des joueurs définira qui joue en blanc et qui joue en noir ; il n'est

### Installation

Prérequis :
- Une version de Python v3.10 sera nécessaire afin de pouvoir utiliser le script.
- Un environnement virtuel venv
- Une version de Git v2.38

Depuis votre terminal ou Git Bash utilisez la commande : \
`python -V` afin de connaître la version installée sur votre système \
`python -m venv --help` afin de vérifier que vous disposer du module venv \
sinon vous pouvez le télécharger sur https://www.python.org/downloads/ \
`git --version` : pour vérifier la version de git installée sur votre système \
sinon vous pouvez la télécharger sur https://git-scm.com/downloads/ \
***Rappel : les commandes ci-dessus ne sont valables qu'avec le module venv*** 

Duplication du dépôt distant en local depuis le terminal ou l'invite de commande : \
`git clone https://github.com/Olivier91972/Tournoi-Echecs` 

Création de l'environnement virtuel "venv" : \
utilisez la commande `python -m venv <nom environnement>` dans ce cas, \
"env" sera par convention, le nom environnement, soit `python -m venv env` 

Activation de l'environnement virtuel "env" : \
exécutez `env/Scripts/activate.bat` \
(si vous êtes sous Unix, la commande sera source `env/bin/activate`)

Installation des packages avec pip : \
`pip install -r requirements.txt`

Lancez le script : \
`python controleur.py` sous Unix \
`py controleur.py` sous Windows \
Si votre interpréteur est invalide pour le projet : 
`rm -rf env` pour supprimer les données de l'environnement virtuel \
Créez et activez depuis l'interface graphique de votre IDE python

***Rappel : Le script ne doit retourner aucune erreur à la fin de son exécution. \
La bonne exécution du script, ainsi que l'intégrité des données récupérées, \
dépendront de la stabilité de votre connexion internet.*** 

# Comment jouer:
Depuis le Menu principal tapez :
- "Créer" pour créer un nouveau tournoi
- "Ajouter" pour ajouter un nouveau joueur
- "Tournoi" pour démarrer un tournoi
- "Classement" pour afficher le classement d'un tournoi

Les rapports:

- "Stat1" (liste des joueurs par ordre alphabétique)
- "Stat2" (liste de tous les tournois)
- "Stat3" (nom et dates d’un tournoi donné)
- "Stat4" (liste des joueurs du tournoi par ordre alphabétique)
- "Stat5" (liste de tous les tours du tournoi et de tous les matchs du tour)
- "Raz" (remise à zéro des scores)
- "Quitter" pour stopper le programme
