"""La vue présente les informations du modèle à l’utilisateur.
Elle sert d’interface visuelle et/ou sonore pour l’utilisateur"""
import os
import json
import pickle
import random
import sys
import time

import numpy as np
import timg
from tabulate import tabulate
from texttable import Texttable

# from pathlib import Path

from rich.console import Console

from datetime import datetime

from modele.joueurs import Joueur, joueur
from tournois import Tournoi, tournoi
from tours import Tours, tour1, tour2, tour3, tour4
from matchs import match, Match


def date_heure_now():
    dtime = datetime.now()
    dth = str(dtime.strftime("%d/%m/%Y, %H:%M:%S"))
    return dth


class Vue:
    """Classe pour l'affichage"""

    # -------------------------------VUE MENU ----------------------------------

    def __init__(self):

        self.idn = None
        self.nom_tournoi = None
        self.lieu = None
        self.date_debut = "01/01/2023"
        self.idtn = None
        self.couleur = None
        self.dated = "dth"
        self.infos = "infos"

    @staticmethod
    def prompt_menu_option():
        """ prompt du menu principal qui retourne une option choisie du menu"""
        # ----------Menu Dynamique----------
        dth = date_heure_now()
        # print(dtime)
        print()
        print(f'Menu Principal :..............{dth}..........')
        print("Bonjour et bienvenue sur l'application du tournoi d'échecs\n"
              "------------------------------------------------------------")

        print("\n----------[MENU]----------")
        print("Choisir une option")
        print('- Créer (Nouveau tournoi)')
        print('- Ajouter (Ajouter un joueur)')
        print('- Tournoi (Démarrer un tournoi)')
        print('- Round (Démarrer un round)')
        print('- Match (Démarrer un match)')
        print('- Classement')
        print('- Stat1 (liste des joueurs par ordre alphabétique)')
        print('- Stat2 (liste de tous les tournois)')
        print('- Stat3 (nom et dates d’un tournoi donné)')
        print('- Stat4 (liste des joueurs du tournoi par ordre alphabétique)')
        print('- Stat5 (liste de tous les tours du tournoi et de tous les matchs du tour)')
        print('- Raz (scores)')
        print('- Quitter')

        user_option = input("\nOption: \n")

        return user_option

    # -------------------------------VUE TOURNOI--------------------------------

    def prompt_creer_tournoi(self):
        """Prompt pour la création d'un tournoi en manuel ou automatique, et retourner oui ou non  """
        self.infos = "infos"
        rep = "o"
        while rep == "o":

            input_creer = input("\n----------[Tournoi]----------\n"
                                "Voulez vous créer un tournoi en mode manuel ?:\n"
                                " - Oui\n"
                                " - Non\n")
            if input_creer.lower() == "oui":
                tournoi.nom_tournoi = input("Entrez le nom du tournoi:\n")
                tournoi.lieu = input("Entrez le lieu du tournoi:\n")
                tournoi.date_debut = input("Entrez la date de début du tournoi:\n")
                tournoi.idn = input("Entrez l'identifiant national d'échecs:\n")
                tournoi.nb_tours = input("Entrez le nombre de tours, par défaut 4:\n")
                tournoi.description = input("Entrez le descriptif du tournoi :\n")
            elif input_creer.lower() == "non":
                pass
                if tournoi.nb_tours != 4:
                    tournoi.nb_tours = 4
                tournoi_dict = {
                    "nom_tournoi": tournoi.nom_tournoi,
                    "lieu": tournoi.lieu,
                    "date_debut": tournoi.date_debut,
                    "idn": tournoi.idn,
                    "nb_tours": tournoi.nb_tours,
                    "description": tournoi.description
                }
                return tournoi_dict

    def afficher_infos_tournois(self, liste_t):
        """Affiche la liste des tournois"""
        self.infos = "infos"

        table = liste_t
        headers = ["Id", "Nom", "Lieu", "Date de début", "Date de fin", "Nb Tours", "Round1",
                   "Round2", "Round3", "Round4", "Description"]
        print(tabulate(table, headers, tablefmt="grid"))

        time.sleep(1)

    def afficher_info_tournoi_actuel(self, tournoi):

        """Affiche les informations du tounoi en cours"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        print(f'Le nom du tournoi en cours est : {tournoi.nom_tournoi}')

    # -------------------------------VUE ROUNDS---------------------------------
    @staticmethod
    def afficher_demarrer_round():

        input_num_round = int(input("\n----------[Round]----------\n"
                                    "Quel round souhaitez vous démarrer ?\n"
                                    "1: pour le Round1\n"
                                    "2: pour le Round2\n"
                                    "3: pour le Round3\n"
                                    "4: pour le Round4\n"))
        return input_num_round

    @staticmethod
    def afficher_creer_tour1():
        """Permet d'afficher la création du tour1 (Round1)"""

        print(f"\n----------[{tour1.nom_round}]----------\n")
        print(f'Début du Round1:{tour1.dateh_deb}')

    @staticmethod
    def afficher_creer_tour2():
        """Permet d'afficher la création du tour2 (Round2)"""

        print(f"\n----------[{tour2.nom_round}]----------\n")
        print(f'Début du Round2:{tour2.dateh_deb}')
        print(f'Round1 Terminé !----------:{tour1.dateh_fin}')

    @staticmethod
    def afficher_creer_tour3():
        """Permet d'afficher la création du tour1 (Round1)"""

        print(f"\n----------[{tour3.nom_round}]----------\n")
        print(f'Début du Round3:{tour3.dateh_deb}')
        print(f'Round2 Terminé !----------:{tour2.dateh_fin}')


    @staticmethod
    def afficher_creer_tour4():
        """Permet d'afficher la création du tour1 (Round1)"""

        print(f"\n----------[{tour4.nom_round}]----------\n")
        print(f'Début du Round4:{tour4.dateh_deb}')
        print(f'Round3 Terminé !----------:{tour3.dateh_fin}')
        # Attention ne pas oublier de terminer le Round 4 si le dernier match est terminé !!!!!!!!!

    @staticmethod
    def prompt_id_tournoi():
        """Demande l'id du tournoi à exécuter"""
        id_tournoi = int(input("\n----------[Tournoi]----------\n"
                               "Sélectionnez l'id du tournoi:\n"))
        return id_tournoi

    @staticmethod
    def afficher_melanger_joueurs_tour1(liste_j):
        """Permet d'afficher la liste des joueurs mélangés au premier tour de façon aléatoire"""

        # self.infos = "infos"
        table = liste_j
        headers = ["Id", "Nom", "Prenom"]
        print(tabulate(table, headers, tablefmt="grid"))

    @staticmethod
    def prompt_joueurs_tour1():
        """ Affiche la question pour la selection de 8 joueurs"""

        print("### Tip's pour import des 8 premiers joueurs: 0,1,2,3,4,5,6,7 ###")
        input_idx = input("Sélectionnez l'id des joueurs exemple: 1,3,4,6...:\n"
                          "pour le Round1\n")
        return input_idx

    @staticmethod
    def prompt_quest_liste_match():
        """Permet à l'utilisateur de saisir manuellement ou non les scores des joueurs"""
        rep_scores = int(input("\n----------[Scores]----------\n"
                                "Souhaitez vous ajouter les scores manuellement ?\n"
                               "1: Oui\n"
                               "0: Non\n"))
        return rep_scores

    @staticmethod
    def prompt_scores_liste_match():
        """Permet à l'utilisateur de saisir les scores des joueurs"""
        score0 = float(input("\n----------[Scores]----------\n"
                           "Entrez le score du joueur0\n"
                           "1.0\n"
                           "0.5\n"
                           "0.0\n"))
        score2 = float(input("\n----------[Scores]----------\n"
                           "Entrez le score du joueur2\n"
                           "1.0\n"
                           "0.5\n"
                           "0.0\n"))
        score4 = float(input("\n----------[Scores]----------\n"
                           "Entrez le score du joueur4\n"
                           "1.0\n"
                           "0.5\n"
                           "0.0\n"))
        score6 = float(input("\n----------[Scores]----------\n"
                           "Entrez le score du joueur6\n"
                           "1.0\n"
                           "0.5\n"
                           "0.0\n"))
        return score0, score2, score4, score6

    @staticmethod
    def afficher_paires_joueurs(xr, paires_joueurs):
        """Affiche les paires de joueurs"""

        # Afficher les paires de joueurs
        print(f"---------PAIRES DE JOUEURS DU ROUND{xr}---------")
        liste_p = []
        for i, paire in enumerate(paires_joueurs):
            print(f'Paire {i + 1}: {paire}')
            liste_p.append(paire)
        print(liste_p)
        return liste_p

    @staticmethod
    def afficher_paires_couleurs(xr, arr):
        """Affiche les paires de couleur des joueurs"""

        print(f"---PAIRES DE COULEURS DES JOUEURS DU ROUND{xr}---")

        liste_xj = []
        for i, xj in enumerate(arr):
            if i % 2 == 0:
                couleur = 'noir'
            else:
                couleur = 'blanc'
            # print(f'Joueur {i + 1} id: {xj} : {couleur}')
            liste_xj.append([str(xj) + "," + str(couleur)])
        print(liste_xj)  # Doit etre en tuple ?
        """  # afficher tabulate avec couleurs des joueurs abandonné pas la temps
        table = liste_j
        headers = ["Id", "Nom", "Prenom"]
        print(tabulate(table, headers, tablefmt="grid"))
        """
        return liste_xj

    # -------------------------------VUE MATCHS---------------------------------
    # @staticmethod
    # def afficher_match1_auto_r1():
    #     """Affiche les matches du round1"""
    #     print("\n----------[Matchs]----------\n")
    #     # abandon faute de temps !

    @staticmethod
    def afficher_classement(num_round, classement):
        """Affiche le classement du round"""

        print()
        print(f"\n----------[CLASSEMENT GENERAL DU ROUND{num_round} ]----------\n")
        print(tabulate(classement, headers=["Rang", "Nom", "Id", "Points", "Pts total"], tablefmt="grid"))

    @staticmethod
    def afficher_joueurs_autres_tours(liste_j):
        """Affiche la liste des joueurs du tour suivant"""

        table = liste_j
        headers = ["Id", "Nom", "Prenom"]
        print()
        print(tabulate(table, headers, tablefmt="grid"))

    @staticmethod
    def prompt_joueurs_autres_tours():
        """Affiche le prompt de selection du tour suivant"""

        input_idrnd = int(input("Sélectionnez le numéro du Round\n"
                                "tapez 2 pour le Round2\n"
                                "tapez 3 pour le Round3\n"
                                "tapez 4 pour le Round4\n"))
        return input_idrnd

    @staticmethod
    def afficher_gagnant(classement):
        """Affiche le gagnant du tournoi"""
        print(classement)
        gagnant = f'classement{classement[1]} avec {classement[4]} points !'

        print(f"Le gagnant du tournoi est {gagnant}")

    def generer_paires(self, array):
        self.infos = "infos"
        """Générer les paires en fonction des résultats des joueurs pour le round"""
        results = []
        for i in range(0, len(array) - 1):
            for j in range(i + 1, len(array)):
                results.append(array[i] + array[j])

        print(results)

        # generer_paires([2, 4, 6, 8])  # ["A", "B", "C", "D"]

        # Returns: ["AB", "AC", "AD", "BC", "BD", "CD"]

    def generer_paires_couleur(self, array):  # Pas utilisé !!!!!!!
        self.infos = "infos"
        """Générer les paires en fonction des résultats des joueurs pour le round"""
        for n in array:
            random.shuffle(n)
            if n == 0:
                self.couleur = "Noir"
                # 'n' est impaire... joueur 2
            else:
                self.couleur = "Noir"
                # 'n' est paire... joueur 1

    def trier_points(self):
        """Trier les points tous les joueurs en fonction de leur nombre total de points
        dans le tournoi"""
        pass

    def associer_joueurs(self):
        """Associez les joueurs dans l’ordre (le joueur 1 avec le joueur 2, le joueur 3
        avec le joueur 4 et ainsi de suite.)"""
        pass

    # -------------------------------VUE JOUEURS--------------------------------
    @staticmethod
    def afficher_ajouter_joueurs():
        """Affiche le prompt pour retourner les variables d'ajout"""

        nom = input("Entrez le nom du joueur:\n")
        prenom = input("Entrez le prénom du joueur:\n")
        daten = input("Entrez la date de naissance du joueur au format JJ/MM/AAAA:\n")

        yon = int(input("Souhaitez vous ajouter un autre joueur ?\n"
                        "1: Oui\n"
                        "0: Non\n"))

        return nom, prenom, daten, yon

    @staticmethod
    def afficher_infos_joueurs(listej):
        """Affiche les joueurs sélectionnés pour le tournoi depuis la base de données json"""

        table = listej
        headers = ["Id", "Nom", "Prenom"]
        print(tabulate(table, headers, tablefmt="grid"))

    @staticmethod
    def afficher_stat1(noms_alpha):
        """Affiche la statistique n°1 : liste de tous les joueurs par ordre alphabétique"""

        table = noms_alpha
        headers = ["Id", "Nom", "Prenom"]
        print(tabulate(table, headers, tablefmt="grid"))

    @staticmethod
    def prompt_stat3():
        """Prompt pour retourner le n° du tournoi à afficher"""

        input_num_t = int(input("\n----------[Rapports]----------\n"
                                "Quel n° de tournoi souhaitez vous afficher ?\n"))

        return input_num_t

    @staticmethod
    def afficher_stat3(input_num_t, liste_inp):
        """Affiche la statistique n°3 : nom et dates d’un tournoi donné"""

        table = liste_inp
        headers = ["Nom", "Date de début", "Date de fin"]
        print(tabulate(table, headers, tablefmt="grid"))

    @staticmethod
    def afficher_stat4(noms_alpha):
        """Affiche la statistique n°4 : liste des joueurs du tournoi par ordre alphabétique"""

        print("\nliste des joueurs enregistrés par ordre alphabétique:\n")
        table = noms_alpha
        headers = ["Id", "Nom", "Prenom"]
        print(tabulate(table, headers, tablefmt="grid"))

    @staticmethod
    def afficher_stat5(rounds_matchs):
        """Affiche la statistique n°5 : liste de tous les tours du tournoi et de tous les matchs du tour"""

        table = rounds_matchs
        headers = ["Round", "Match1", "Match2", "Match3", "Match4"]
        print(tabulate(table, headers, tablefmt="grid"))

