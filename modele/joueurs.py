"""Gère les joueurs"""

import json


class Joueur:
    """Constructeur du joueur"""

    def __init__(self, nom, prenom, idx, daten):
        deja_joue = []
        self.nom = nom
        self.prenom = prenom
        self.daten = daten  # Au format JJ/MM/AAAA !
        self.sexe = "sexe"
        self.idx = idx
        self.deja_joue = deja_joue
        self.fichier = "fichier"
        self.joueur = "joueurx"
        self.bdd = "nc"

    def afficher_joueurs(self):
        print(self.nom, self.prenom, self.idx, self.daten, sep=":")

    def instancier_joueurs_json(self):
        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)
            """
            for x in datajoueurs:
                joueur_x = f'joueur{x}'
                joueur_x = Joueur(nom=f'joueur{x}', prenom=None, daten=None)
                print(joueur_x.nom)
            """

            joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], idx="0", daten=None)
            joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], idx="1", daten=None)
            joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], idx="2", daten=None)
            joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], idx="3", daten=None)
            joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], idx="4", daten=None)
            joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], idx="5", daten=None)
            joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], idx="6", daten=None)
            joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], idx="7", daten=None)

            # pas plus de 9 joueurs car problème recup 2 digits lors des matchs/scores/points !!!!

            listjoueurs = []
            for i in datajoueurs:
                self.joueur = Joueur(nom=str("joueur" + i), prenom=None, idx=None, daten=None)

                listjoueurs.append(self.joueur)

            # print(joueur_x.nom)

            print()
            print(f'Nombre de joueurs dans la base de données: {len(listjoueurs)}')

        return joueur0, joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7


joueur = Joueur(nom=None, prenom=None, idx=None, daten=None)

joueursbdd9max = Joueur(nom=None, prenom=None, idx=None, daten=None)


joueursbdd9max.instancier_joueurs_json()
