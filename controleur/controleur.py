"""Le contrôleur garantit que les commandes utilisateurs soient exécutées correctement,
c’est la couche qui apporte une interaction avec l’utilisateur"""
import json
import numpy as np
import os
import random
import sys
from tabulate import tabulate
import time
import timg


from modele.joueurs import Joueur, joueur
from modele.tournois import Tournoi, tournoi
from modele.matchs import Match, match
from tours import Tours, tour1, tour2, tour3, tour4
from vue.vue import Vue


# méthodes statiques


# def controles():
#     """Entrées de l'application"""  # Liste de choix à créer puis router en passant avant la class controleur!!!
#     # reponse = self.get_menu()  # Problème !

class Controleur:
    """Classe qui contrôle l'application"""
    def __init__(self):
        self.vue = Vue()
        self.infos = "infos"
        self.fichier = "fichier"
        self.tournoi_actuel = "tournoi_actuel"
        self.joueur = Joueur(nom="nc", prenom="nc", idx="nc", daten="nc")
        #
        # self.match = Match(idtn=1, num_round=1, joueur0=int, joueur1=int)
        # self.tour = Tours(num_round=int)

    def run(self):
        """Démarre l'application"""

        try:
            while True:
                self.set_menu_options()
        except KeyboardInterrupt:
            print("\n\nLe programme a été interrompu ! Des données ont peut-être été perdues, au revoir !")
            sys.exit(0)

    def get_menu_option(self):
        """Controle le menu et retourne le choix"""

        return self.vue.prompt_menu_option()

    def set_menu_options(self):
        """Demande le choix de l'utilisateur"""

        user_option = self.vue.prompt_menu_option()

        menu_options = ('ajouter', 'tournoi', 'créer', 'creer', 'round',
                        'match', 'raz', 'quitter', 'quit', 'exit', 'classement', 'stat1',
                        'stat2', 'stat3', 'stat4', 'stat5')

        if user_option in menu_options:

            if user_option is None:
                pass

            elif user_option.lower() in menu_options:
                if "créer" in user_option.lower() or "creer" in user_option.lower():
                    self.creer_tournoi()
                elif "ajouter" in user_option.lower():
                    self.ajouter_joueur()
                elif "tournoi" in user_option.lower():
                    self.creer_tour1()  # ne pas oublier de démarrer que si len(datajoueurs)<=8
                    # Et empécher de démarrer si len(input
                elif "round" in user_option.lower():
                    self.demarrer_round()
                elif "match" in user_option.lower():
                    self.liste_matchs_auto_r4()
                elif "classement" in user_option.lower():
                    self.classement_tournoi()
                elif "stat1" in user_option.lower():
                    self.rapports_tournoi(stat="stat1")
                elif "stat2" in user_option.lower():
                    self.infos_tournois(liste_stats="liste_t")
                elif "stat3" in user_option.lower():
                    self.infos_tournois(liste_stats="stat3")
                elif "stat4" in user_option.lower():
                    self.infos_joueurs(stat="stat4")
                elif "stat5" in user_option.lower():
                    self.rapports_round_match()
                elif "raz" in user_option.lower():
                    self.raz_scores()
                elif "quitter" in user_option.lower() or "quit" in user_option.lower() or "exit" in user_option.lower():
                    quitter()

            elif user_option.lower() not in menu_options:
                return self.set_menu_options()

    def creer_tournoi(self):
        """ Permet de créer un tournoi"""

        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !

        # Constituer la liste des tournois:
        self.infos_tournois(liste_stats="liste_t")

        tournoi_dict = self.vue.prompt_creer_tournoi()

        self.ajouter_tournoi(tournoi_dict)

        return self.tournoi_actuel

    def infos_tournois(self, liste_stats):
        """Affiche les informations des tournois"""

        global input_num_t
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

            # print(datatournois)

            # Pour décoder en utf-8 sinon "CrÃ©teil" au lieu de "Créteil"
            # sjson = (datatournois["0"][0]["lieu"]).encode("latin1").decode("utf-8")
            # print(sjson)

        liste_t = []
        liste_inp = []
        for i in datatournois:
            tournoi.idx = i

            tournoi.nom_tournoi = datatournois[f'{i}'][0]["nom_tournoi"]
            try:
                tournoi.nom_tournoi = tournoi.nom_tournoi.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.date_debut = datatournois[f'{i}'][0]["date_debut"]
            tournoi.date_fin = datatournois[f'{i}'][0]["date_fin"]
            tournoi.nb_tours = datatournois[f'{i}'][0]["nb_tours"]
            tournoi.lieu = datatournois[f'{i}'][0]["lieu"]
            try:
                tournoi.lieu = tournoi.lieu.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            # Pour décoder en utf-8 sinon "CrÃ©teil" au lieu de "Créteil"
            tournoi.description = datatournois[f'{i}'][0]["description"]
            try:
                tournoi.description = tournoi.description.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.lj_r1 = datatournois[f'{i}'][0]["lj_r1"]
            tournoi.lj_r2 = datatournois[f'{i}'][0]["lj_r2"]
            tournoi.lj_r3 = datatournois[f'{i}'][0]["lj_r3"]
            tournoi.lj_r4 = datatournois[f'{i}'][0]["lj_r4"]

            # Afficher liste des tournois via tabulate
            idt = tournoi.idx
            nt = tournoi.nom_tournoi
            lt = tournoi.lieu
            dd = tournoi.date_debut
            df = tournoi.date_fin
            nbt = tournoi.nb_tours
            lj1 = tournoi.lj_r1
            lj2 = tournoi.lj_r2
            lj3 = tournoi.lj_r3
            lj4 = tournoi.lj_r4
            desc = tournoi.description
            liste_t.append([str(idt)] + [str(nt)] + [str(lt)] + [str(dd)] + [str(df)] + [str(nbt)]
                           + [str(lj1)] + [str(lj2)] + [str(lj3)] + [str(lj4)] + [str(desc)])

        if "liste_t" in liste_stats:
            print("\nliste des tournois:\n")
            liste_t = self.vue.afficher_infos_tournois(liste_t)
        else:
            pass

        if "stat3" in liste_stats:
            try:
                input_num_t = self.vue.prompt_stat3()
            except KeyError:
                print("Veuillez svp sélectionner un numéro dans la liste des tournois")
                self.infos_tournois(liste_stats="stat3")
            tournoi.nom_tournoi = datatournois[f'{input_num_t}'][0]["nom_tournoi"]
            try:
                tournoi.nom_tournoi = tournoi.nom_tournoi.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.date_debut = datatournois[f'{input_num_t}'][0]["date_debut"]
            tournoi.date_fin = datatournois[f'{input_num_t}'][0]["date_fin"]

            nt = tournoi.nom_tournoi
            dd = tournoi.date_debut
            df = tournoi.date_fin
            liste_inp.append([str(nt)] + [str(dd)] + [str(df)])
            self.vue.afficher_stat3(input_num_t, liste_inp)

        time.sleep(2)

        # Vérification encodage pour tabulate
        # print(f'sys.getdefaultencoding:{sys.getdefaultencoding()}')

    def ajouter_tournoi(self, tournoi_dict):
        """Ajoute le dict qui contient les infos du tournoi à créer"""

        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

        # print(datatournois)

        # Création nouvel objet tournoi:  # ok _x Manque incrément nb_joueurs +1 dans la classe joueur(init) !!!
        idx = len(datatournois)

        # print(tournoi.nom_tournoi, tournoi.lieu, tournoi.date_debut, tournoi.idn, tournoi.nb_tours)

        tournoi.nom_tournoi = tournoi_dict["nom_tournoi"]
        try:
            tournoi.nom_tournoi = tournoi.nom_tournoi.encode("latin1").decode("utf-8")
        except AttributeError:
            pass
            # print("\nLe champ description est vide !\n"
            #       "'NoneType' object has no attribute 'encode'\n")
        tournoi.lieu = tournoi_dict["lieu"]
        try:
            tournoi.lieu = tournoi.lieu.encode("latin1").decode("utf-8")
        except AttributeError:
            pass
            # print("\nLe champ description est vide !\n"
            #       "'NoneType' object has no attribute 'encode'\n")
        tournoi.date_debut = tournoi_dict["date_debut"]
        tournoi.idn = tournoi_dict["idn"]
        tournoi.nb_tours = tournoi_dict["nb_tours"]
        if tournoi.nb_tours != 4:
            tournoi.nb_tours = 4
        tournoi.description = tournoi_dict["description"]
        try:
            tournoi.description = tournoi.description.encode("latin1").decode("utf-8")
        except AttributeError:
            pass
            # print("\nLe champ description est vide !\n"
            #       "'NoneType' object has no attribute 'encode'\n")

        tournoi.idtn = len(datatournois)

        newtournoi = {f'{idx}': [{
            "nom_tournoi": tournoi.nom_tournoi,
            "lieu": tournoi.lieu,
            "date_debut": tournoi.date_debut,
            "date_fin": tournoi.date_fin,
            "nb_tours": tournoi.nb_tours,
            "num_tour_actuel": tournoi.num_tour_actuel,
            "liste_tours": tournoi.liste_tours,
            "liste_joueurs": tournoi.liste_joueurs,
            "description": tournoi.description,
            "lj_r1": tournoi.lj_r1,
            "lj_r2": tournoi.lj_r2,
            "lj_r3": tournoi.lj_r3,
            "lj_r4": tournoi.lj_r4,
            "matchs_r1": tournoi.matchs_r1,
            "matchs_r2": tournoi.matchs_r2,
            "matchs_r3": tournoi.matchs_r3,
            "matchs_r4": tournoi.matchs_r4,
            "score0": match.score0,
            "score1": match.score1,
            "score2": match.score2,
            "score3": match.score3,
            "score4": match.score4,
            "score5": match.score5,
            "score6": match.score6,
            "score7": match.score7,
            "liste_dj0": match.liste_dj0,
            "liste_dj1": match.liste_dj1,
            "liste_dj2": match.liste_dj2,
            "liste_dj3": match.liste_dj3,
            "liste_dj4": match.liste_dj4,
            "liste_dj5": match.liste_dj5,
            "liste_dj6": match.liste_dj6,
            "liste_dj7": match.liste_dj7,
            "score_j0": tournoi.score_j0,
            "score_j1": tournoi.score_j1,
            "score_j2": tournoi.score_j2,
            "score_j3": tournoi.score_j3,
            "score_j4": tournoi.score_j4,
            "score_j5": tournoi.score_j5,
            "score_j6": tournoi.score_j6,
            "score_j7": tournoi.score_j7,
            "score_m1_r1": tournoi.score_m1_r1,
            "score_m2_r1": tournoi.score_m2_r1,
            "score_m3_r1": tournoi.score_m3_r1,
            "score_m4_r1": tournoi.score_m4_r1,
            "score_m1_r2": tournoi.score_m1_r2,
            "score_m2_r2": tournoi.score_m2_r2,
            "score_m3_r2": tournoi.score_m3_r2,
            "score_m4_r2": tournoi.score_m4_r2,
            "score_m1_r3": tournoi.score_m1_r3,
            "score_m2_r3": tournoi.score_m2_r3,
            "score_m3_r3": tournoi.score_m3_r3,
            "score_m4_r3": tournoi.score_m4_r3,
            "score_m1_r4": tournoi.score_m1_r4,
            "score_m2_r4": tournoi.score_m2_r4,
            "score_m3_r4": tournoi.score_m3_r4,
            "score_m4_r4": tournoi.score_m4_r4,
            "couleurs_r1": tournoi.couleurs_r1,
            "couleurs_r2": tournoi.couleurs_r2,
            "couleurs_r3": tournoi.couleurs_r3,
            "couleurs_r4": tournoi.couleurs_r4,
            "idtn": tournoi.idtn,
            "dateh_deb_r1": tour1.dateh_deb,
            "dateh_fin_r1": tour1.dateh_fin,
            "dateh_deb_r2": tour2.dateh_deb,
            "dateh_fin_r2": tour2.dateh_fin,
            "dateh_deb_r3": tour3.dateh_deb,
            "dateh_fin_r3": tour3.dateh_fin,
            "dateh_deb_r4": tour4.dateh_deb,
            "dateh_fin_r4": tour4.dateh_fin
        }]}
        tournoi.idtn = 1  # sinon reste à len(datatournois)
        datatournois.update(newtournoi)

        with open("../modele/data/tournaments/tournois.json", "w") as f:
            json.dump(datatournois, f, indent=2, sort_keys=True)

            print("\nTournoi créé !\n"
                  "Sauvegarde effectuée\n")
        return self.tournoi_actuel

    # -------------------------------CONTROLEUR ROUNDS---------------------------------
    def demarrer_round(self):
        """Permet de demmarer le round désiré"""

        input_num_round = self.vue.afficher_demarrer_round()

        if input_num_round == 1:
            self.creer_tour1()
        elif input_num_round == 2:
            self.creer_tour2()
        elif input_num_round == 3:
            self.creer_tour3()
        elif input_num_round == 4:
            self.creer_tour4()

    def creer_tour1(self):
        """Permet de créer des round"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        # Charge les données dans l'objet tournoi (en cours...)
        # Sinon
        # raise TypeError(f'Object of type {o.__class__.__name__} '
        # TypeError: Object of type type is not JSON serializable

        # liste_stats="liste_t" par defaut, sinon liste_stats="stat3" pour rapport n°3
        self.infos_tournois(liste_stats="liste_t")
        # Demander l'id du tournoi
        id_tournoi = self.vue.prompt_id_tournoi()
        if id_tournoi <= len(datatournois):
            tournoi.idtn = id_tournoi
        else:
            tournoi.idtn = 1  # Par défaut
        tournoi.nom_tournoi = datatournois[f'{id_tournoi}'][0]["nom_tournoi"]
        try:
            tournoi.nom_tournoi = tournoi.nom_tournoi.encode("latin1").decode("utf-8")
        except AttributeError:
            pass
            # print("\nLe champ description est vide !\n"
            #       "'NoneType' object has no attribute 'encode'\n")
        tournoi.date_debut = datatournois[f'{id_tournoi}'][0]["date_debut"]
        tournoi.date_fin = datatournois[f'{id_tournoi}'][0]["date_fin"]
        tournoi.nb_tours = datatournois[f'{id_tournoi}'][0]["nb_tours"]
        tournoi.lieu = datatournois[f'{id_tournoi}'][0]["lieu"]
        try:
            tournoi.lieu = tournoi.lieu.encode("latin1").decode("utf-8")
        except AttributeError:
            pass
            # print("\nLe champ description est vide !\n"
            #       "'NoneType' object has no attribute 'encode'\n")
        tournoi.description = datatournois[f'{id_tournoi}'][0]["description"]
        try:
            tournoi.description = tournoi.description.encode("latin1").decode("utf-8")
        except AttributeError:
            pass
            # print("\nLe champ description est vide !\n"
            #       "'NoneType' object has no attribute 'encode'\n")
        tournoi.liste_joueurs = datatournois[f'{id_tournoi}'][0]["liste_joueurs"]
        tournoi.liste_tours = datatournois[f'{id_tournoi}'][0]["liste_tours"]
        tournoi.lj_r1 = datatournois[f'{id_tournoi}'][0]["lj_r1"]
        tournoi.lj_r2 = datatournois[f'{id_tournoi}'][0]["lj_r2"]
        tournoi.lj_r3 = datatournois[f'{id_tournoi}'][0]["lj_r3"]
        tournoi.lj_r4 = datatournois[f'{id_tournoi}'][0]["lj_r4"]
        tournoi.matchs_r1 = datatournois[f'{id_tournoi}'][0]["matchs_r1"]
        tournoi.matchs_r2 = datatournois[f'{id_tournoi}'][0]["matchs_r2"]
        tournoi.matchs_r3 = datatournois[f'{id_tournoi}'][0]["matchs_r3"]
        tournoi.matchs_r4 = datatournois[f'{id_tournoi}'][0]["matchs_r4"]
        tournoi.score_j0 = datatournois[f'{id_tournoi}'][0]["score_j0"]
        tournoi.score_j1 = datatournois[f'{id_tournoi}'][0]["score_j1"]
        tournoi.score_j2 = datatournois[f'{id_tournoi}'][0]["score_j2"]
        tournoi.score_j3 = datatournois[f'{id_tournoi}'][0]["score_j3"]
        tournoi.score_j4 = datatournois[f'{id_tournoi}'][0]["score_j4"]
        tournoi.score_j5 = datatournois[f'{id_tournoi}'][0]["score_j5"]
        tournoi.score_j6 = datatournois[f'{id_tournoi}'][0]["score_j6"]
        tournoi.score_j7 = datatournois[f'{id_tournoi}'][0]["score_j7"]
        match.score0 = datatournois[f'{id_tournoi}'][0]["score0"]
        match.score1 = datatournois[f'{id_tournoi}'][0]["score1"]
        match.score2 = datatournois[f'{id_tournoi}'][0]["score2"]
        match.score3 = datatournois[f'{id_tournoi}'][0]["score3"]
        match.score4 = datatournois[f'{id_tournoi}'][0]["score4"]
        match.score5 = datatournois[f'{id_tournoi}'][0]["score5"]
        match.score6 = datatournois[f'{id_tournoi}'][0]["score6"]
        match.score7 = datatournois[f'{id_tournoi}'][0]["score7"]
        match.liste_dj0 = datatournois[f'{id_tournoi}'][0]["liste_dj0"]
        match.liste_dj1 = datatournois[f'{id_tournoi}'][0]["liste_dj1"]
        match.liste_dj2 = datatournois[f'{id_tournoi}'][0]["liste_dj2"]
        match.liste_dj3 = datatournois[f'{id_tournoi}'][0]["liste_dj3"]
        match.liste_dj4 = datatournois[f'{id_tournoi}'][0]["liste_dj4"]
        match.liste_dj5 = datatournois[f'{id_tournoi}'][0]["liste_dj5"]
        match.liste_dj6 = datatournois[f'{id_tournoi}'][0]["liste_dj6"]
        match.liste_dj7 = datatournois[f'{id_tournoi}'][0]["liste_dj7"]
        tournoi.couleurs_r1 = datatournois[f'{id_tournoi}'][0]["couleurs_r1"]
        tournoi.couleurs_r2 = datatournois[f'{id_tournoi}'][0]["couleurs_r2"]
        tournoi.couleurs_r3 = datatournois[f'{id_tournoi}'][0]["couleurs_r3"]
        tournoi.couleurs_r4 = datatournois[f'{id_tournoi}'][0]["couleurs_r4"]
        tournoi.num_tour_actuel = datatournois[f'{id_tournoi}'][0]["num_tour_actuel"]
        #tournoi.idtn = datatournois[f'{id_tournoi}'][0]["idtn"]
        tour1.dateh_deb = datatournois[f'{id_tournoi}'][0]["dateh_deb_r1"]
        tour1.dateh_fin = datatournois[f'{id_tournoi}'][0]["dateh_fin_r1"]
        tour2.dateh_deb = datatournois[f'{id_tournoi}'][0]["dateh_deb_r2"]
        tour2.dateh_fin = datatournois[f'{id_tournoi}'][0]["dateh_fin_r2"]
        tour3.dateh_deb = datatournois[f'{id_tournoi}'][0]["dateh_deb_r3"]
        tour3.dateh_fin = datatournois[f'{id_tournoi}'][0]["dateh_fin_r3"]
        tour4.dateh_deb = datatournois[f'{id_tournoi}'][0]["dateh_deb_r4"]
        tour4.dateh_fin = datatournois[f'{id_tournoi}'][0]["dateh_fin_r4"]

        tour1.dateh_deb = tour1.debut()

        self.vue.afficher_creer_tour1()

        update_tournoi(datatournois)

        self.melanger_joueurs_tour1()

    def creer_tour2(self):
        """Permet de créer des round"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        self.serialiser_obj_tournois()
        tournoi.num_tour_actuel = 2
        self.vue.afficher_creer_tour2()
        tour1.dateh_fin = tour1.fin()  # Termine en auto le précédent Round
        tour2.dateh_deb = tour2.debut()

        update_tournoi(datatournois)

        self.joueurs_autres_tours()

    def creer_tour3(self):
        """Permet de créer des round"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        self.serialiser_obj_tournois()
        tournoi.num_tour_actuel = 3
        self.vue.afficher_creer_tour3()
        tour2.dateh_fin = tour2.fin()  # Termine en auto le précédent Round
        tour3.dateh_deb = tour3.debut()

        update_tournoi(datatournois)

        self.joueurs_autres_tours()

    def creer_tour4(self):
        """Permet de créer des round"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        self.serialiser_obj_tournois()
        tournoi.num_tour_actuel = 4
        self.vue.afficher_creer_tour4()
        tour3.dateh_fin = tour3.fin()  # Termine en auto le précédent Round
        tour4.dateh_deb = tour4.debut()

        update_tournoi(datatournois)

        self.joueurs_autres_tours()

    def melanger_joueurs_tour1(self):  # faire un return de la liste de joueurs_idx
        """ Mélange les joueurs au premier tour de façon aléatoire"""

        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !

        # afficher les joueurs dans la base de données
        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

            # print(datajoueurs)

            #Demander l'id du tournoi ???
            # tournoi.idtn = 1  # Par défaut

            liste_j = []
            for i in datajoueurs:
                joueur.idx = i
                joueur.nom = datajoueurs[f'{i}'][0]["nom"]
                joueur.prenom = datajoueurs[f'{i}'][0]["prenom"]
                # print(joueur.idx, joueur.nom, joueur.prenom)

                listej = []

                lj = [joueur.idx, joueur.nom, joueur.prenom]
                listej.extend(lj)
                # print(listej)
                # Afficher liste des tournois via tabulate
                idj = joueur.idx
                nj = joueur.nom
                pj = joueur.prenom
                liste_j.append([str(idj)] + [str(nj)] + [str(pj)])

            self.vue.afficher_melanger_joueurs_tour1(liste_j)

        rep = "o"
        while rep == "o":

            input_idx = str
            input_idx = self.vue.prompt_joueurs_tour1() #vérifier que le bon nombre de car est retourné !!!!!!

            joueurs_idx = []



            yonj = int(input("Veuillez confirmer (1: Oui) ou recommencer (0: Non) ?\n"
                             "1: Oui\n"
                             "0: Non\n"))

            liste_nombres = [int(x) for x in input_idx.split(",")]

            if yonj == 1:
                print(f'Voici les {len(liste_nombres)} joueur(s) sélectionnés pour le Round1 :\n')
            else:
                print("Démarrage du Round1...\n"), self.melanger_joueurs_tour1()


            #liste_nombres = [int(x) for x in input_idx.split(",")]

            # Assign array
            arr = np.array(liste_nombres)
            # Display original array
            # print("Original array: ", arr)

            # Shuffle array
            np.random.shuffle(arr)

            # Display shuffled array
            # print("Shuffled array: ", arr)

            with open("../modele/data/tournaments/joueurs.json", "r") as f:
                datajoueurs = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

            # print(datajoueurs)

                # Afficher liste des joueurs les joueurs sélectionnés
                liste_t = []  # !!!attention de ne pas oublier de déclarer en dehors !!!!!!!!!!!!!!!!!!!!!!!!!
                for liste_j in arr:

                    # print(datajoueurs[f'{liste_j}'][0]["nom"])
                    # print(datajoueurs[f'{liste_j}'][0]["prenom"])
                    # print("------------------------")
                    idj = liste_j
                    no = (datajoueurs[f'{liste_j}'][0]["nom"])
                    pr = (datajoueurs[f'{liste_j}'][0]["prenom"])
                    liste_t.append([str(idj)]+[str(no)]+[str(pr)])

                    # print(liste_t)  # je n'arrive pas à extend dans textable (dico?)

                # je n'arrive pas à obtenir cette exemple de liste dans liste_t2!!!!!!!!!!!!!résolu
                # table = ['Smollett', 'Jamal'], ['Henson', 'Cookie'], ['Byers', 'Andre']
                table = liste_t
                headers = ["Id", "Nom", "Prenom"]
                print(tabulate(table, headers, tablefmt="grid"))

                with open("../modele/data/tournaments/tournois.json", "r") as f2:
                    datatournois = json.load(f2)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!
                    # Charge les données dans l'objet tournoi (en cours...)

                    self.serialiser_obj_tournois()

                    idt_tournoi = 1  # le dernier de la liste est l'actuel

                    tournoi.idtn = 1  # Tournoi 1 par défaut !!!!!
                    #print(f'liste_ nombres {liste_nombres}')
                    tournoi.lj_r1 = liste_nombres
                    tournoi.liste_joueurs = liste_nombres

                    #print(datatournois)

                    #print(tuple(arr))

                    liste_ljr1 = arr  # Ok [arr] -le tuple ou liste ne passe pas en variable!!!!!!!!!
                    #tournoi.lj_r1 = liste_ljr1
                    tournoi.idtn = datatournois[f'{idt_tournoi}'][0]["idtn"]
                    tournoi.num_tour_actuel = 1  # car ici tour1
                    #print("idtn", tournoi.idtn)
                    #print(tournoi.nom_tournoi)

                    liste_num = []
                    for num in arr:
                        #print(num)
                        liste_num.append(num)
                    liste_num_f = str(liste_num).replace("[]", "()")
                    #print(f'liste_num_f: {liste_num_f}')
                    print(f'Enregistrement sur le Round{tournoi.num_tour_actuel}')
                    #datatournois[f'{tournoi.num_tour_actuel}'][0]["lj_r1"] = str(liste_num_f)  #En str car en int ça passe pas!!!
                    #print("arr", arr)

                    id_joueurs = arr  # base d'id !!!!!
                    # diviser la liste de joueurs en 2
                    paires_joueurs = [(id_joueurs[i], id_joueurs[i+1]) for i in range(0, len(id_joueurs), 2)]

                    #print(paires_joueurs)

                    xr = tournoi.num_tour_actuel
                    liste_p = self.vue.afficher_paires_joueurs(xr, paires_joueurs)

                    tournoi.matchs_r1 = str(liste_p)

                    #print(tournoi.lj_r1)
                    tournoi.idtn = 1


                    liste_xj = self.vue.afficher_paires_couleurs(xr, arr)
                    # Afficher les paires de couleurs des joueurs

                    tournoi.couleurs_r1 = str(liste_xj)

                    tournoi.num_tour_actuel += 1  # pour passer au auto en round 2
                    tournoi.idtn = 1
                    update_tournoi(datatournois)

                    self.liste_matchs_auto_r1()

    def joueurs_autres_tours(self):  # faire un return de la liste de joueurs_idx
        """ Tri par points les joueurs du précédent tour"""

        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f2:
            datatournois = json.load(f2)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!
            # Charge les données dans l'objet tournoi (en cours...)
            #idt_tournoi = len(datatournois) - 1  # le dernier de la liste est l'actuel

            self.serialiser_obj_tournois()

            # afficher les joueurs dans la base de données
            with open("../modele/data/tournaments/joueurs.json", "r") as f:
                datajoueurs = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

                # print(datajoueurs)

                liste_j = []

                idt_tournoi = tournoi.idtn
                num_round = tournoi.num_tour_actuel
                print(f'num_round: {num_round}')

                if num_round == 2:
                    tournoi.lj_r2 = datatournois[f'{idt_tournoi}'][0]["lj_r2"]
                    lj_r2 = tournoi.lj_r2
                    liste_pt = lj_r2
                elif num_round == 3:
                    tournoi.lj_r3 = datatournois[f'{idt_tournoi}'][0]["lj_r3"]
                    lj_r3 = tournoi.lj_r3
                    liste_pt = lj_r3
                elif num_round == 4:
                    tournoi.lj_r4 = datatournois[f'{idt_tournoi}'][0]["lj_r4"]
                    lj_r4 = tournoi.lj_r4
                    liste_pt = lj_r4

                # liste à jour en fct des points à replace car str!

                # print(f'liste_pt_f : {liste_pt_f}')
                indices = liste_pt  # test à mettre à jour en fct des points ok !
                print(f"---------- Liste des joueurs sélectionnés pour le Round{tournoi.num_tour_actuel}----------")
                # A trier par points ok !
                # problème avec num actuel car liste avant input_idrnd après...!!!!!
                for i in indices:
                    joueur.idx = i
                    joueur.nom = datajoueurs[f'{i}'][0]["nom"]
                    joueur.prenom = datajoueurs[f'{i}'][0]["prenom"]
                    # print(joueur.idx, joueur.nom, joueur.prenom)

                    listej = []

                    lj = [joueur.idx, joueur.nom, joueur.prenom]
                    listej.extend(lj)
                    # print(listej)
                    # Afficher liste des tournois via tabulate
                    idj = joueur.idx
                    nj = joueur.nom
                    pj = joueur.prenom
                    liste_j.append([str(idj)] + [str(nj)] + [str(pj)])

                listej = self.vue.afficher_joueurs_autres_tours(liste_j)

                rep = "o"
                while rep == "o":

                    joueurs_idx = []
                    #print("### Tip's pour import des 8 premiers joueurs: 0,1,2,3,4,5,6,7 ###")
                    print("\n----------[Round]----------")
                    #input_idrnd = 2

                    input_idrnd = self.vue.prompt_joueurs_autres_tours()

                    # Si un tour n'est démarré dans l'ordre depuis le Round1 !
                    if tournoi.num_tour_actuel != input_idrnd:
                        tournoi.num_tour_actuel = input_idrnd

                    # print(tournoi.num_tour_actuel)
                    update_tournoi(datatournois)
                    with open("../modele/data/tournaments/tournois.json", "r") as f2:
                        datatournois = json.load(f2)
                        #tournoi.num_tour_actuel = input_idrnd  # numéro du Round pour la sélection

                        self.serialiser_obj_tournois()
                        # récupérer la liste Joueurs/scores du round précédent pour total points/classement !!!!!!!!!
                        selection_points = None
                        yonj = int(input("Veuillez confirmer (1: oui) ou recommencer (o) ?\n"
                                         "1: Oui\n"
                                         "0: Non\n"))

                        #liste_nombres = None  # récupérer la liste

                        # fonction qui donne les déja joués pour 1 joueur:
                        # pour le 1er joueur print du vs
                        liste_dj0 = []
                        liste_dj1 = []
                        liste_dj2 = []
                        liste_dj3 = []
                        liste_dj4 = []
                        liste_dj5 = []
                        liste_dj6 = []
                        liste_dj7 = []

                        if num_round == 2:
                            id_joueurs = tournoi.lj_r2  # base d'id !!!!!
                            print(f'tournoi.lj_r2{tournoi.lj_r2}')
                        elif num_round == 3:
                            id_joueurs = tournoi.lj_r3
                        elif num_round == 4:
                            id_joueurs = tournoi.lj_r4
                        # diviser la liste de joueurs en 2
                        paires_joueurs = [(id_joueurs[i], id_joueurs[i + 1]) for i in range(0, len(id_joueurs), 2)]

                        print(f'paires_joueurs{paires_joueurs}')

                        liste_p = []
                        for i, paire in enumerate(paires_joueurs):
                            print(f'Paire {i + 1}: {paire}')
                            liste_p.append(paire)
                        print(liste_p)

                        print("\n Liste déja joué par joueurs:")
                        liste_dj0.append(liste_p[0][1])
                        liste_dj1.append(liste_p[0][0])
                        liste_dj2.append(liste_p[1][1])
                        liste_dj3.append(liste_p[1][0])
                        liste_dj4.append(liste_p[2][1])
                        liste_dj5.append(liste_p[2][0])
                        liste_dj6.append(liste_p[3][1])
                        liste_dj7.append(liste_p[3][0])

                        print(liste_dj0)
                        print(liste_dj1)
                        print(liste_dj2)
                        print(liste_dj3)
                        print(liste_dj4)
                        print(liste_dj5)
                        print(liste_dj6)
                        print(liste_dj7)

                        # liste déja joué par joueurs:

                        update_tournoi(datatournois)
                        self.serialiser_obj_tournois()
                        print(f'tournoi.lj_r2 {tournoi.lj_r2}')
                        # if num_round == 2:
                        #     tournoi.lj_r2
                        # elif num_round == 3:
                        #     tournoi.lj_r3
                        # elif num_round == 4:
                        #     tournoi.lj_r4
                        # else:
                        #     pass
                        if num_round == 2:
                            lj_r2_t2 = tournoi.lj_r2
                            nextdj0 = self.joueurs_dejajoue(liste_p[0][0], liste_dj0, tournoi.lj_r2)
                            print(f'nextdj0: {nextdj0}')

                            nextdj2 = self.joueurs_dejajoue(liste_p[1][0], liste_dj2, tournoi.lj_r2)
                            print(f'nextdj2: {nextdj2}')

                            nextdj4 = self.joueurs_dejajoue(liste_p[2][0], liste_dj4, tournoi.lj_r2)
                            print(f'nextdj4: {nextdj4}')

                            nextdj6 = self.joueurs_dejajoue(liste_p[3][0], liste_dj6, tournoi.lj_r2)
                            nextdj6 = list(map(int, liste_dj6))
                            nextdj6 = nextdj6[0]
                            print(f'nextdj6: {nextdj6}')
                            print(f'tournoi.lj_r2 {tournoi.lj_r2}')

                        elif num_round == 3:
                            lj_r3_t2 = tournoi.lj_r3
                            nextdj0 = self.joueurs_dejajoue(liste_p[0][0], liste_dj0, tournoi.lj_r3)
                            print(f'nextdj0: {nextdj0}')

                            nextdj2 = self.joueurs_dejajoue(liste_p[1][0], liste_dj2, tournoi.lj_r3)
                            print(f'nextdj2: {nextdj2}')

                            nextdj4 = self.joueurs_dejajoue(liste_p[2][0], liste_dj4, tournoi.lj_r3)
                            print(f'nextdj4: {nextdj4}')

                            nextdj6 = self.joueurs_dejajoue(liste_p[3][0], liste_dj6, tournoi.lj_r3)
                            nextdj6 = list(map(int, liste_dj6))
                            nextdj6 = nextdj6[0]
                            print(f'nextdj6: {nextdj6}')

                        elif num_round == 4:
                            lj_r4_t2 = tournoi.lj_r4
                            nextdj0 = self.joueurs_dejajoue(liste_p[0][0], liste_dj0, tournoi.lj_r4)
                            print(f'nextdj0: {nextdj0}')

                            nextdj2 = self.joueurs_dejajoue(liste_p[1][0], liste_dj2, tournoi.lj_r4)
                            print(f'nextdj2: {nextdj2}')

                            nextdj4 = self.joueurs_dejajoue(liste_p[2][0], liste_dj4, tournoi.lj_r4)
                            print(f'nextdj4: {nextdj4}')

                            nextdj6 = self.joueurs_dejajoue(liste_p[3][0], liste_dj6, tournoi.lj_r4)
                            nextdj6 = list(map(int, liste_dj6))
                            nextdj6 = nextdj6[0]
                            print(f'nextdj6: {nextdj6}')
                        else:
                            pass

                        #print(lj_rx_t2)


                        print(f'tournoi.lj_r2 {tournoi.lj_r2}')
                        self.serialiser_obj_tournois()  # <--- Pourquoi demander à guillaume !!!!!!!!!???????????
                        # sinon tournoi.lj_r2 = []

                        print(f'tournoi.lj_r2{tournoi.lj_r2}')
                        """
                        liste_p_def = [tournoi.lj_r2[0],]
                        if tournoi.lj_r2[1] == tournoi.lj_r2[0]:
                            liste_p_def.append()
                        """
                        #Mon algo de pairing perso !!! 1/2 jour de travail !!!
                        if num_round == 2:
                            liste_p_r2 = [tournoi.lj_r2[0], nextdj0, tournoi.lj_r2[1], nextdj2,
                                          tournoi.lj_r2[3], nextdj4, tournoi.lj_r2[5], nextdj6]

                            print(f'tournoi.lj_r2:{tournoi.lj_r2[1]}')
                            print(f'liste_p_r2{liste_p_r2}')
                            print(f'lj_r2_t2{lj_r2_t2}')
                        elif num_round == 3:
                            liste_p_r3 = [tournoi.lj_r3[0], nextdj0, tournoi.lj_r3[1], nextdj2,
                                          tournoi.lj_r3[3], nextdj4, tournoi.lj_r3[5], nextdj6]

                            print(f'tournoi.lj_r3:{tournoi.lj_r3[1]}')
                            print(f'liste_p_r3{liste_p_r3}')
                            print(f'lj_r3_t2{lj_r3_t2}')
                        elif num_round == 4:
                            liste_p_r4 = [tournoi.lj_r4[0], nextdj0, tournoi.lj_r4[1], nextdj2,
                                          tournoi.lj_r4[3], nextdj4, tournoi.lj_r4[5], nextdj6]

                            print(f'tournoi.lj_r4:{tournoi.lj_r4[1]}')
                            print(f'liste_p_r4{liste_p_r4}')
                            print(f'lj_r4_t2{lj_r4_t2}')

                        else:
                            pass

                        print(f'Enregistrement sur le Round{tournoi.num_tour_actuel}')
                        #tournoi.lj_r1 = str(liste_num_f)  # En str car en int ça passe pas!!!
                        # print("arr", arr)

                        if num_round == 2:
                            liste_p_rxx = liste_p_r2
                        elif num_round == 3:
                            liste_p_rxx = liste_p_r3
                        elif num_round == 4:
                            liste_p_rxx = liste_p_r4
                        else:
                            pass
                        id_joueurs = liste_p_rxx  # base d'id !!!!!
                        print(f'num_round: {num_round}')
                        print(f'liste_p_rxx: {liste_p_rxx}')
                        # diviser la liste de joueurs en 2
                        paires_joueurs = [(id_joueurs[i], id_joueurs[i + 1]) for i in range(0, len(id_joueurs), 2)]

                        # print(paires_joueurs)

                        # Afficher les paires de joueurs
                        print(f"---------PAIRES DE JOUEURS DU ROUND{tournoi.num_tour_actuel}---------")
                        liste_p = []
                        for i, paire in enumerate(paires_joueurs):
                            print(f'Paire {i + 1}: {paire}')
                            liste_p.append(paire)
                        print(liste_p)

                        # Envoyer liste_p avec des joueurs non joués !!!!!
                        if num_round == 2:
                            tournoi.matchs_r2 = liste_p_r2
                        elif num_round == 3:
                            tournoi.matchs_r3 = liste_p_r3
                        elif num_round == 4:
                            tournoi.matchs_r4 = liste_p_r4
                        else:
                            pass

                        #print(tournoi.lj_r2)


                        #tournoi.num_tour_actuel += 1  # pour passer au auto au round suivant
                        #update_tournoi(datatournois)  # sinon crash lj_r2 = [] !!!!!!!!!!!!!!!

                        """
                        paire1 = liste_p[0]
                        paire2 = liste_p[1]
                        paire3 = liste_p[2]
                        paire4 = liste_p[3]
                        """

                        # Afficher les paires de couleurs des joueurs
                        print(f"---PAIRES DE COULEURS DES JOUEURS DU ROUND{tournoi.num_tour_actuel}---")

                        if num_round == 2:
                            liste_p_rx = liste_p_r2
                        elif num_round == 3:
                            liste_p_rx = liste_p_r3
                        elif num_round == 4:
                            liste_p_rx = liste_p_r4

                        liste_xj = []
                        for i, xj in enumerate(liste_p_rx):
                            if i % 2 == 0:
                                couleur = 'noir'
                            else:
                                couleur = 'blanc'
                            liste_xj.append([str(xj) + "," + str(couleur)])
                        print(liste_xj)  # Doit etre en tuple ?

                        if tournoi.num_tour_actuel == 2:
                            tournoi.couleurs_r2 = str(liste_xj)
                        elif tournoi.num_tour_actuel == 3:
                            tournoi.couleurs_r3 = str(liste_xj)
                        elif tournoi.num_tour_actuel == 4:
                            tournoi.couleurs_r4 = str(liste_xj)
                        else:
                            pass

                        # Pas de tour 5...
                        if tournoi.num_tour_actuel == 4:
                            tournoi.num_tour_actuel = 1
                        else:
                            tournoi.num_tour_actuel += 1  # pour passer au auto au round suivant !
                        # gérer les try et éviter les modif si erreurs avant le dump

                        update_tournoi(datatournois)

                        with open("../modele/data/tournaments/tournois.json", "w") as f3:
                            json.dump(datatournois, f3, indent=2, sort_keys=True)

                            # print(datatournois)

                        self.serialiser_obj_tournois()

                        print("Sauvegarde effectuée")

                        if input_idrnd == 2:
                            tour1.dateh_fin = tour1.fin()  # Termine en auto le précédent Round, reste màj !!!!!!!!!
                            tour2.dateh_deb = tour2.debut()
                            update_tournoi(datatournois)
                            self.liste_matchs_auto_r2()

                        elif input_idrnd == 3:
                            tour3.dateh_fin = tour2.fin()  # Termine en auto le précédent Round, reste màj !!!!!!!!!
                            tour3.dateh_deb = tour3.debut()
                            update_tournoi(datatournois)
                            self.liste_matchs_auto_r3()

                        elif input_idrnd == 4:
                            tour4.dateh_fin = tour3.fin()  # Termine en auto le précédent Round, reste màj !!!!!!!!!
                            tour4.dateh_deb = tour4.debut()
                            update_tournoi(datatournois)
                            self.liste_matchs_auto_r4()

                        #Attention ne pas oublier de terminer le Round 4 si le dernier match est terminé !!!!!!!!!

                        else:
                            update_tournoi(datatournois)
                            self.liste_matchs_auto_r2()

    def liste_matchs_auto_r1(self):
        """ Permet de lister les matchs en fonction"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !

        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        # print(datatournois)
        # créer Match Round1
        idtn = tournoi.idtn  # input("Entrez l'idtn du tournoi:\n")  # afficher liste des tournois !!!!!!!
        print("\n----------[Matchs]----------\n")
        num_round = 1  # input("Entrez le numéro du round:\n")  # peut etre ...afficher liste des round

        tournoi.lj_r1 = datatournois[f'{idtn}'][0]["lj_r1"]
        tournoi.matchs_r1 = datatournois[f'{idtn}'][0]["matchs_r1"]
        tournoi.score_j0 = datatournois[f'{idtn}'][0]["score_j0"]
        tournoi.score_j1 = datatournois[f'{idtn}'][0]["score_j1"]
        tournoi.score_j2 = datatournois[f'{idtn}'][0]["score_j2"]
        tournoi.score_j3 = datatournois[f'{idtn}'][0]["score_j3"]
        tournoi.score_j4 = datatournois[f'{idtn}'][0]["score_j4"]
        tournoi.score_j5 = datatournois[f'{idtn}'][0]["score_j5"]
        tournoi.score_j6 = datatournois[f'{idtn}'][0]["score_j6"]
        tournoi.score_j7 = datatournois[f'{idtn}'][0]["score_j7"]

        #print(tournoi.matchs_r1)

        #print(tournoi.lj_r1)


        liste_joueurs = [int(tournoi.matchs_r1[2]), int(tournoi.matchs_r1[5]), int(tournoi.matchs_r1[10]),
                         int(tournoi.matchs_r1[13]), int(tournoi.matchs_r1[18]), int(tournoi.matchs_r1[21]),
                         int(tournoi.matchs_r1[26]), int(tournoi.matchs_r1[29])]
        #print(sorted(liste_joueurs, reverse=False))
        for i in liste_joueurs:
            setattr(match, "joueur" + str(i), liste_joueurs[i])

        rep_scores = self.vue.prompt_quest_liste_match()


        # retourne 1: oui ou 2: non
        if rep_scores == 1:  # manuel
            score0, score2, score4, score6 = self.vue.prompt_scores_liste_match()
            match.score0 = score0
            match.score2 = score2
            match.score4 = score4
            match.score6 = score6

        elif rep_scores == 0:  # Automatique
            a = 1.0
            b = 0.5
            c = 0.0
            x = [a, b, c]
            random.choice(x)
            score0 = random.choice([a, b, c])
            score2 = random.choice([a, b, c])
            score4 = random.choice([a, b, c])
            score6 = random.choice([a, b, c])
            match.score0 = score0
            match.score2 = score2
            match.score4 = score4
            match.score6 = score6
            if match.score0 == 1.0:
                match.score1 = 0.0
            elif match.score0 == 0.0:
                match.score1 = 1.0
            elif match.score0 == 0.5:
                match.score1 = 0.5

            if match.score2 == 1.0:
                match.score3 = 0.0
            elif match.score2 == 0.0:
                match.score3 = 1.0
            elif match.score2 == 0.5:
                match.score3 = 0.5

            if match.score4 == 1.0:
                match.score5 = 0.0
            elif match.score4 == 0.0:
                match.score5 = 1.0
            elif match.score4 == 0.5:
                match.score5 = 0.5

            if match.score6 == 1.0:
                match.score7 = 0.0
            elif match.score6 == 0.0:
                match.score7 = 1.0
            elif match.score6 == 0.5:
                match.score7 = 0.5
        else:
            self.liste_matchs_auto_r1()

        # Score retourne "1: 1.0\n" "2: 0.5\n" "3: 0.0\n
        # else:
        #     a = 1.0
        #     b = 0.5
        #     c = 0.0
        #     x = [a, b, c]
        #     random.choice(x)
        #     score0 = random.choice([a, b, c])
        #     score2 = random.choice([a, b, c])
        #     score4 = random.choice([a, b, c])
        #     score6 = random.choice([a, b, c])
        #     match.score0 = score0
        #     match.score2 = score2
        #     match.score4 = score4
        #     match.score6 = score6




        match_m1_r1 = Match(idtn, num_round, match.joueur0, match.joueur1)
        print()
        print(f'----------[{match_m1_r1.nom_match}]----------')
        match.paire = tuple[(), ()]
        match.paire1 = [(match.joueur0, match.score0), (match.joueur1, match.score1)]
        print(match.paire1)

        print()
        if match.score0 > match.score1:
            print(f'----------Le joueur {match.joueur0} a gagné le match du Round{num_round} !----------')
        elif match.score0 == match.score1:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur1} a gagné le match du Round{num_round} !----------')

        match_m1_r1.lj_r1 = datatournois[f'{idtn}'][0]["lj_r1"]

        match_m2_r1 = Match(idtn, num_round, match.joueur2, match.joueur3)
        print()
        print(f'----------[{match_m2_r1.nom_match}]----------')
        match.paire2 = [(match.joueur2, match.score2), (match.joueur3, match.score3)]
        print(match.paire2)

        print()
        if match.score2 > match.score3:
            print(f'----------Le joueur {match.joueur2} a gagné le match du Round{num_round} !----------')
        elif match.score2 == match.score3:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur3} a gagné le match du Round{num_round} !----------')

        match_m2_r1.lj_r1 = datatournois[f'{idtn}'][0]["lj_r1"]

        match_m3_r1 = Match(idtn, num_round, match.joueur4, match.joueur5)
        print()
        print(f'----------[{match_m3_r1.nom_match}]----------')
        match.paire3 = [(match.joueur4, match.score4), (match.joueur5, match.score5)]
        print(match.paire3)

        print()
        if match.score4 > match.score5:
            print(f'----------Le joueur {match.joueur4} a gagné le match du Round{num_round} !----------')
        elif match.score4 == match.score5:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur5} a gagné le match du Round{num_round} !----------')

        match_m3_r1.lj_r1 = datatournois[f'{idtn}'][0]["lj_r1"]

        match_m4_r1 = Match(idtn, num_round, match.joueur6, match.joueur7)
        print()
        print(f'----------[{match_m4_r1.nom_match}]----------')
        match.paire4 = [(match.joueur6, match.score6), (match.joueur7, match.score7)]
        print(match.paire4)

        print()
        if match.score6 > match.score7:
            print(f'----------Le joueur {match.joueur6} a gagné le match du Round{num_round} !----------')
        elif match.score6 == match.score7:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur7} a gagné le match du Round{num_round} !----------')

        match_m4_r1.lj_r1 = datatournois[f'{idtn}'][0]["lj_r1"]

        tournoi.score_m1_r1 = match.paire1  # Tuple à stocker dans datatournois !!!!!!
        tournoi.score_m2_r1 = match.paire2
        tournoi.score_m3_r1 = match.paire3
        tournoi.score_m4_r1 = match.paire4

        time.sleep(0.8)

        update_tournoi(datatournois)

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            # Charge les données dans l'objet tournoi (en cours...)
            # Sinon
            # raise TypeError(f'Object of type {o.__class__.__name__} '
            # TypeError: Object of type type is not JSON serializable
            tournoi.idtn = 1

            self.serialiser_obj_tournois()

            # joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], daten=None)
            # joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], daten=None)
            # joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], daten=None)
            # joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], daten=None)
            # joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], daten=None)
            # joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], daten=None)
            # joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], daten=None)
            # joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], daten=None)
            # joueur9 = Joueur(nom=datajoueurs[8][0]["nom"], prenom=datajoueurs[8][0]["prenom"], daten=None)
            # pas plus de 10 joueurs car problème recup 2 digits lors des matchs/scores/points !!!!

        tournoi.score_j0 += match.score0
        tournoi.score_j1 += match.score1
        tournoi.score_j2 += match.score2
        tournoi.score_j3 += match.score3
        tournoi.score_j4 += match.score4
        tournoi.score_j5 += match.score5
        tournoi.score_j6 += match.score6
        tournoi.score_j7 += match.score7

        joueursdict = [
            {"nom": datajoueurs[f'{match.joueur0}'][0]["nom"] + " " + datajoueurs[f'{match.joueur0}'][0]["prenom"],
             "idj": match.joueur0, "points": match.score0, "pts total": tournoi.score_j0},
            {"nom": datajoueurs[f'{match.joueur1}'][0]["nom"] + " " + datajoueurs[f'{match.joueur1}'][0]["prenom"],
             "idj": match.joueur1, "points": match.score1, "pts total": tournoi.score_j1},
            {"nom": datajoueurs[f'{match.joueur2}'][0]["nom"] + " " + datajoueurs[f'{match.joueur2}'][0]["prenom"],
             "idj": match.joueur2, "points": match.score2, "pts total": tournoi.score_j2},
            {"nom": datajoueurs[f'{match.joueur3}'][0]["nom"] + " " + datajoueurs[f'{match.joueur3}'][0]["prenom"],
             "idj": match.joueur3, "points": match.score3, "pts total": tournoi.score_j3},
            {"nom": datajoueurs[f'{match.joueur4}'][0]["nom"] + " " + datajoueurs[f'{match.joueur4}'][0]["prenom"],
             "idj": match.joueur4, "points": match.score4, "pts total": tournoi.score_j4},
            {"nom": datajoueurs[f'{match.joueur5}'][0]["nom"] + " " + datajoueurs[f'{match.joueur5}'][0]["prenom"],
             "idj": match.joueur5, "points": match.score5, "pts total": tournoi.score_j5},
            {"nom": datajoueurs[f'{match.joueur6}'][0]["nom"] + " " + datajoueurs[f'{match.joueur6}'][0]["prenom"],
             "idj": match.joueur6, "points": match.score6, "pts total": tournoi.score_j6},
            {"nom": datajoueurs[f'{match.joueur7}'][0]["nom"] + " " + datajoueurs[f'{match.joueur7}'][0]["prenom"],
             "idj": match.joueur7, "points": match.score7, "pts total": tournoi.score_j7}
            ]
        # score_r1 contient les points qui se mettent à jour apres chaque match !!!

        joueursdict_tries = sorted(joueursdict, key=lambda x1: x1["pts total"], reverse=True)

        classement = []
        position = 1
        for x1 in joueursdict_tries:
            classement.append([position, x1["nom"], x1["idj"], x1["points"], x1["pts total"]])
            position += 1

        self.vue.afficher_classement(num_round, classement)

        time.sleep(0.8)

        # print("liste en fonction des points")
        liste_lj_r2 = []
        for x2 in classement:
            ljr2 = x2[2]
            liste_lj_r2.append(str(ljr2))
        # print(liste_lj_r2)
        tournoi.lj_r2 = liste_lj_r2

        # Pour enregistrement au bon endroit !!! sinon dernier par défaut tournoi.idtn
        print(f'tournoi.idtn: {tournoi.idtn}')
        print(f'num_round: {num_round}')
        update_tournoi(datatournois)

        # print(f'classement{classement}')

        self.creer_tour2()

    def liste_matchs_auto_r2(self):
        """ Permet de lister les matchs en fonction"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !

        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        # print(datatournois)
        # créer Match Round1
        idtn = tournoi.idtn  # input("Entrez l'idtn du tournoi:\n")  # afficher liste des tournois !!!!!!!
        print("\n----------[Matchs]----------\n")
        num_round = 2  # input("Entrez le numéro du round:\n")  # peut etre ...afficher liste des round

        tournoi.lj_r2 = datatournois[f'{idtn}'][0]["lj_r2"]
        tournoi.matchs_r2 = datatournois[f'{idtn}'][0]["matchs_r2"]
        tournoi.score_j0 = datatournois[f'{idtn}'][0]["score_j0"]
        tournoi.score_j1 = datatournois[f'{idtn}'][0]["score_j1"]
        tournoi.score_j2 = datatournois[f'{idtn}'][0]["score_j2"]
        tournoi.score_j3 = datatournois[f'{idtn}'][0]["score_j3"]
        tournoi.score_j4 = datatournois[f'{idtn}'][0]["score_j4"]
        tournoi.score_j5 = datatournois[f'{idtn}'][0]["score_j5"]
        tournoi.score_j6 = datatournois[f'{idtn}'][0]["score_j6"]
        tournoi.score_j7 = datatournois[f'{idtn}'][0]["score_j7"]

        print(f'tournoi.matchs_r2{tournoi.matchs_r2}')

        #print(tournoi.lj_r2)

        liste_joueurs = (tournoi.matchs_r2[0], tournoi.matchs_r2[1], tournoi.matchs_r2[2],
                         tournoi.matchs_r2[3], tournoi.matchs_r2[4], tournoi.matchs_r2[5],
                         tournoi.matchs_r2[6], tournoi.matchs_r2[7])
        liste_joueurs_int = int(tournoi.matchs_r2[0]), int(tournoi.matchs_r2[1]), int(tournoi.matchs_r2[2]), \
                            int(tournoi.matchs_r2[3]), int(tournoi.matchs_r2[4]), int(tournoi.matchs_r2[5]), \
                            int(tournoi.matchs_r2[6]), int(tournoi.matchs_r2[7])
        #print(sorted(liste_joueurs, reverse=False))
        for i in liste_joueurs_int:
            setattr(match, "joueur" + str(i), liste_joueurs_int[i])

            # # ----------MATCH 1 ----- ROUND 2 ----------
            # match.joueur0 = tournoi.matchs_r2[0]
            # match.joueur1 = tournoi.matchs_r2[1]
            # # ----------MATCH 2 ----- ROUND 2 ----------
            # match.joueur2 = tournoi.matchs_r2[2]
            # match.joueur3 = tournoi.matchs_r2[3]
            # # ----------MATCH 3 ----- ROUND 2 ----------
            # match.joueur4 = tournoi.matchs_r2[4]
            # match.joueur5 = tournoi.matchs_r2[5]
            # # ----------MATCH 4 ----- ROUND 2 ----------
            # match.joueur6 = tournoi.matchs_r2[6]
            # match.joueur7 = tournoi.matchs_r2[7]

        a = 1.0
        b = 0.5
        c = 0.0
        x = [a, b, c]
        random.choice(x)
        score0 = random.choice([a, b, c])
        score2 = random.choice([a, b, c])
        score4 = random.choice([a, b, c])
        score6 = random.choice([a, b, c])
        match.score0 = score0
        match.score2 = score2
        match.score4 = score4
        match.score6 = score6

        if match.score0 == 1.0:
            match.score1 = 0.0
        elif match.score0 == 0.0:
            match.score1 = 1.0
        elif match.score0 == 0.5:
            match.score1 = 0.5

        if match.score2 == 1.0:
            match.score3 = 0.0
        elif match.score2 == 0.0:
            match.score3 = 1.0
        elif match.score2 == 0.5:
            match.score3 = 0.5

        if match.score4 == 1.0:
            match.score5 = 0.0
        elif match.score4 == 0.0:
            match.score5 = 1.0
        elif match.score4 == 0.5:
            match.score5 = 0.5

        if match.score6 == 1.0:
            match.score7 = 0.0
        elif match.score6 == 0.0:
            match.score7 = 1.0
        elif match.score6 == 0.5:
            match.score7 = 0.5

        match_m1_r2 = Match(idtn, num_round, match.joueur0, match.joueur1)
        print()
        print(f'----------[{match_m1_r2.nom_match}]----------')
        match.paire = tuple[(), ()]
        match.paire1 = [(match.joueur0, match.score0), (match.joueur1, match.score1)]
        print(match.paire1)

        print()
        if match.score0 > match.score1:
            print(f'----------Le joueur {match.joueur0} a gagné le match du Round{num_round} !----------')
        elif match.score0 == match.score1:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur1} a gagné le match du Round{num_round} !----------')

        match_m1_r2.lj_r2 = datatournois[f'{idtn}'][0]["lj_r2"]

        match_m2_r2 = Match(idtn, num_round, match.joueur2, match.joueur3)
        print()
        print(f'----------[{match_m2_r2.nom_match}]----------')
        match.paire2 = [(match.joueur2, match.score2), (match.joueur3, match.score3)]
        print(match.paire2)

        print()
        if match.score2 > match.score3:
            print(f'----------Le joueur {match.joueur2} a gagné le match du Round{num_round} !----------')
        elif match.score2 == match.score3:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur3} a gagné le match du Round{num_round} !----------')

        match_m2_r2.lj_r2 = datatournois[f'{idtn}'][0]["lj_r2"]

        match_m3_r2 = Match(idtn, num_round, match.joueur4, match.joueur5)
        print()
        print(f'----------[{match_m3_r2.nom_match}]----------')
        match.paire3 = [(match.joueur4, match.score4), (match.joueur5, match.score5)]
        print(match.paire3)

        print()
        if match.score4 > match.score5:
            print(f'----------Le joueur {match.joueur4} a gagné le match du Round{num_round} !----------')
        elif match.score4 == match.score5:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur5} a gagné le match du Round{num_round} !----------')

        match_m3_r2.lj_r2 = datatournois[f'{idtn}'][0]["lj_r2"]

        match_m4_r2 = Match(idtn, num_round, match.joueur6, match.joueur7)
        print()
        print(f'----------[{match_m4_r2.nom_match}]----------')
        match.paire4 = [(match.joueur6, match.score6), (match.joueur7, match.score7)]
        print(match.paire4)

        print()
        if match.score6 > match.score7:
            print(f'----------Le joueur {match.joueur6} a gagné le match du Round{num_round} !----------')
        elif match.score6 == match.score7:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur7} a gagné le match du Round{num_round} !----------')

        match_m4_r2.lj_r2 = datatournois[f'{idtn}'][0]["lj_r2"]

        tournoi.score_m1_r2 = match.paire1  # Tuple à stocker dans datatournois !!!!!!
        tournoi.score_m2_r2 = match.paire2
        tournoi.score_m3_r2 = match.paire3
        tournoi.score_m4_r2 = match.paire4

        time.sleep(0.8)

        update_tournoi(datatournois)

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            # Charge les données dans l'objet tournoi (en cours...)
            # Sinon
            # raise TypeError(f'Object of type {o.__class__.__name__} '
            # TypeError: Object of type type is not JSON serializable
            tournoi.idtn = 1

            self.serialiser_obj_tournois()

            # joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], daten=None)
            # joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], daten=None)
            # joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], daten=None)
            # joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], daten=None)
            # joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], daten=None)
            # joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], daten=None)
            # joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], daten=None)
            # joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], daten=None)
            # joueur9 = Joueur(nom=datajoueurs[8][0]["nom"], prenom=datajoueurs[8][0]["prenom"], daten=None)
            # pas plus de 10 joueurs car problème recup 2 digits lors des matchs/scores/points !!!!

        tournoi.score_j0 += match.score0
        tournoi.score_j1 += match.score1
        tournoi.score_j2 += match.score2
        tournoi.score_j3 += match.score3
        tournoi.score_j4 += match.score4
        tournoi.score_j5 += match.score5
        tournoi.score_j6 += match.score6
        tournoi.score_j7 += match.score7

        joueursdict = [
            {"nom": datajoueurs[f'{match.joueur0}'][0]["nom"] + " " + datajoueurs[f'{match.joueur0}'][0]["prenom"],
             "idj": match.joueur0, "points": match.score0, "pts total": tournoi.score_j0},
            {"nom": datajoueurs[f'{match.joueur1}'][0]["nom"] + " " + datajoueurs[f'{match.joueur1}'][0]["prenom"],
             "idj": match.joueur1, "points": match.score1, "pts total": tournoi.score_j1},
            {"nom": datajoueurs[f'{match.joueur2}'][0]["nom"] + " " + datajoueurs[f'{match.joueur2}'][0]["prenom"],
             "idj": match.joueur2, "points": match.score2, "pts total": tournoi.score_j2},
            {"nom": datajoueurs[f'{match.joueur3}'][0]["nom"] + " " + datajoueurs[f'{match.joueur3}'][0]["prenom"],
             "idj": match.joueur3, "points": match.score3, "pts total": tournoi.score_j3},
            {"nom": datajoueurs[f'{match.joueur4}'][0]["nom"] + " " + datajoueurs[f'{match.joueur4}'][0]["prenom"],
             "idj": match.joueur4, "points": match.score4, "pts total": tournoi.score_j4},
            {"nom": datajoueurs[f'{match.joueur5}'][0]["nom"] + " " + datajoueurs[f'{match.joueur5}'][0]["prenom"],
             "idj": match.joueur5, "points": match.score5, "pts total": tournoi.score_j5},
            {"nom": datajoueurs[f'{match.joueur6}'][0]["nom"] + " " + datajoueurs[f'{match.joueur6}'][0]["prenom"],
             "idj": match.joueur6, "points": match.score6, "pts total": tournoi.score_j6},
            {"nom": datajoueurs[f'{match.joueur7}'][0]["nom"] + " " + datajoueurs[f'{match.joueur7}'][0]["prenom"],
             "idj": match.joueur7, "points": match.score7, "pts total": tournoi.score_j7}
            ]
        # score_r2 contient les points qui se mettent à jour apres chaque match !!!

        joueursdict_tries = sorted(joueursdict, key=lambda x1: x1["pts total"], reverse=True)

        classement = []
        position = 1
        for x1 in joueursdict_tries:
            classement.append([position, x1["nom"], x1["idj"], x1["points"], x1["pts total"]])
            position += 1

        self.vue.afficher_classement(num_round, classement)

        time.sleep(0.8)

        # print("liste en fonction des points")
        liste_lj_r3 = []
        for x3 in classement:
            ljr3 = x3[2]
            liste_lj_r3.append(str(ljr3))
        # print(liste_lj_r3)
        tournoi.lj_r3 = liste_lj_r3

        # Pour enregistrement au bon endroit !!! sinon dernier par défaut tournoi.idtn
        print(f'tournoi.idtn: {tournoi.idtn}')
        print(f'num_round: {num_round}')
        update_tournoi(datatournois)

        # print(f'classement{classement}')

        self.creer_tour3()

    def liste_matchs_auto_r3(self):
        """ Permet de lister les matchs en fonction"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !

        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        # print(datatournois)
        # créer Match Round1
        idtn = tournoi.idtn  # input("Entrez l'idtn du tournoi:\n")  # afficher liste des tournois !!!!!!!
        print("\n----------[Matchs]----------\n")
        num_round = 3  # input("Entrez le numéro du round:\n")  # peut etre ...afficher liste des round

        tournoi.lj_r3 = datatournois[f'{idtn}'][0]["lj_r3"]
        tournoi.matchs_r3 = datatournois[f'{idtn}'][0]["matchs_r3"]
        tournoi.score_j0 = datatournois[f'{idtn}'][0]["score_j0"]
        tournoi.score_j1 = datatournois[f'{idtn}'][0]["score_j1"]
        tournoi.score_j2 = datatournois[f'{idtn}'][0]["score_j2"]
        tournoi.score_j3 = datatournois[f'{idtn}'][0]["score_j3"]
        tournoi.score_j4 = datatournois[f'{idtn}'][0]["score_j4"]
        tournoi.score_j5 = datatournois[f'{idtn}'][0]["score_j5"]
        tournoi.score_j6 = datatournois[f'{idtn}'][0]["score_j6"]
        tournoi.score_j7 = datatournois[f'{idtn}'][0]["score_j7"]

        print(f'tournoi.matchs_r3{tournoi.matchs_r3}')

        # print(tournoi.lj_r3)

        liste_joueurs = (tournoi.matchs_r3[0], tournoi.matchs_r3[1], tournoi.matchs_r3[2],
                         tournoi.matchs_r3[3], tournoi.matchs_r3[4], tournoi.matchs_r3[5],
                         tournoi.matchs_r3[6], tournoi.matchs_r3[7])
        liste_joueurs_int = int(tournoi.matchs_r3[0]), int(tournoi.matchs_r3[1]), int(tournoi.matchs_r3[2]),\
                            int(tournoi.matchs_r3[3]), int(tournoi.matchs_r3[4]), int(tournoi.matchs_r3[5]),\
                            int(tournoi.matchs_r3[6]), int(tournoi.matchs_r3[7])
        # print(sorted(liste_joueurs, reverse=False))
        for i in liste_joueurs_int:
            setattr(match, "joueur" + str(i), liste_joueurs_int[i])

        a = 1.0
        b = 0.5
        c = 0.0
        x = [a, b, c]
        random.choice(x)
        score0 = random.choice([a, b, c])
        score2 = random.choice([a, b, c])
        score4 = random.choice([a, b, c])
        score6 = random.choice([a, b, c])
        match.score0 = score0
        match.score2 = score2
        match.score4 = score4
        match.score6 = score6

        if match.score0 == 1.0:
            match.score1 = 0.0
        elif match.score0 == 0.0:
            match.score1 = 1.0
        elif match.score0 == 0.5:
            match.score1 = 0.5

        if match.score2 == 1.0:
            match.score3 = 0.0
        elif match.score2 == 0.0:
            match.score3 = 1.0
        elif match.score2 == 0.5:
            match.score3 = 0.5

        if match.score4 == 1.0:
            match.score5 = 0.0
        elif match.score4 == 0.0:
            match.score5 = 1.0
        elif match.score4 == 0.5:
            match.score5 = 0.5

        if match.score6 == 1.0:
            match.score7 = 0.0
        elif match.score6 == 0.0:
            match.score7 = 1.0
        elif match.score6 == 0.5:
            match.score7 = 0.5

        match_m1_r3 = Match(idtn, num_round, match.joueur0, match.joueur1)
        print()
        print(f'----------[{match_m1_r3.nom_match}]----------')
        match.paire = tuple[(), ()]
        match.paire1 = [(match.joueur0, match.score0), (match.joueur1, match.score1)]
        print(match.paire1)

        print()
        if match.score0 > match.score1:
            print(f'----------Le joueur {match.joueur0} a gagné le match du Round{num_round} !----------')
        elif match.score0 == match.score1:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur1} a gagné le match du Round{num_round} !----------')

        match_m1_r3.lj_r3 = datatournois[f'{idtn}'][0]["lj_r3"]

        match_m2_r3 = Match(idtn, num_round, match.joueur2, match.joueur3)
        print()
        print(f'----------[{match_m2_r3.nom_match}]----------')
        match.paire2 = [(match.joueur2, match.score2), (match.joueur3, match.score3)]
        print(match.paire2)

        print()
        if match.score2 > match.score3:
            print(f'----------Le joueur {match.joueur2} a gagné le match du Round{num_round} !----------')
        elif match.score2 == match.score3:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur3} a gagné le match du Round{num_round} !----------')

        match_m2_r3.lj_r3 = datatournois[f'{idtn}'][0]["lj_r3"]

        match_m3_r3 = Match(idtn, num_round, match.joueur4, match.joueur5)
        print()
        print(f'----------[{match_m3_r3.nom_match}]----------')
        match.paire3 = [(match.joueur4, match.score4), (match.joueur5, match.score5)]
        print(match.paire3)

        print()
        if match.score4 > match.score5:
            print(f'----------Le joueur {match.joueur4} a gagné le match du Round{num_round} !----------')
        elif match.score4 == match.score5:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur5} a gagné le match du Round{num_round} !----------')

        match_m3_r3.lj_r3 = datatournois[f'{idtn}'][0]["lj_r3"]

        match_m4_r3 = Match(idtn, num_round, match.joueur6, match.joueur7)
        print()
        print(f'----------[{match_m4_r3.nom_match}]----------')
        match.paire4 = [(match.joueur6, match.score6), (match.joueur7, match.score7)]
        print(match.paire4)

        print()
        if match.score6 > match.score7:
            print(f'----------Le joueur {match.joueur6} a gagné le match du Round{num_round} !----------')
        elif match.score6 == match.score7:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur7} a gagné le match du Round{num_round} !----------')

        match_m4_r3.lj_r3 = datatournois[f'{idtn}'][0]["lj_r3"]

        tournoi.score_m1_r3 = match.paire1  # Tuple à stocker dans datatournois !!!!!!
        tournoi.score_m2_r3 = match.paire2
        tournoi.score_m3_r3 = match.paire3
        tournoi.score_m4_r3 = match.paire4

        time.sleep(0.8)

        update_tournoi(datatournois)

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            # Charge les données dans l'objet tournoi (en cours...)
            # Sinon
            # raise TypeError(f'Object of type {o.__class__.__name__} '
            # TypeError: Object of type type is not JSON serializable
            tournoi.idtn = 1

            self.serialiser_obj_tournois()

            # joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], daten=None)
            # joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], daten=None)
            # joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], daten=None)
            # joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], daten=None)
            # joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], daten=None)
            # joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], daten=None)
            # joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], daten=None)
            # joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], daten=None)
            # joueur9 = Joueur(nom=datajoueurs[8][0]["nom"], prenom=datajoueurs[8][0]["prenom"], daten=None)
            # pas plus de 10 joueurs car problème recup 2 digits lors des matchs/scores/points !!!!

        tournoi.score_j0 += match.score0
        tournoi.score_j1 += match.score1
        tournoi.score_j2 += match.score2
        tournoi.score_j3 += match.score3
        tournoi.score_j4 += match.score4
        tournoi.score_j5 += match.score5
        tournoi.score_j6 += match.score6
        tournoi.score_j7 += match.score7

        joueursdict = [
            {"nom": datajoueurs[f'{match.joueur0}'][0]["nom"] + " " + datajoueurs[f'{match.joueur0}'][0]["prenom"],
             "idj": match.joueur0, "points": match.score0, "pts total": tournoi.score_j0},
            {"nom": datajoueurs[f'{match.joueur1}'][0]["nom"] + " " + datajoueurs[f'{match.joueur1}'][0]["prenom"],
             "idj": match.joueur1, "points": match.score1, "pts total": tournoi.score_j1},
            {"nom": datajoueurs[f'{match.joueur2}'][0]["nom"] + " " + datajoueurs[f'{match.joueur2}'][0]["prenom"],
             "idj": match.joueur2, "points": match.score2, "pts total": tournoi.score_j2},
            {"nom": datajoueurs[f'{match.joueur3}'][0]["nom"] + " " + datajoueurs[f'{match.joueur3}'][0]["prenom"],
             "idj": match.joueur3, "points": match.score3, "pts total": tournoi.score_j3},
            {"nom": datajoueurs[f'{match.joueur4}'][0]["nom"] + " " + datajoueurs[f'{match.joueur4}'][0]["prenom"],
             "idj": match.joueur4, "points": match.score4, "pts total": tournoi.score_j4},
            {"nom": datajoueurs[f'{match.joueur5}'][0]["nom"] + " " + datajoueurs[f'{match.joueur5}'][0]["prenom"],
             "idj": match.joueur5, "points": match.score5, "pts total": tournoi.score_j5},
            {"nom": datajoueurs[f'{match.joueur6}'][0]["nom"] + " " + datajoueurs[f'{match.joueur6}'][0]["prenom"],
             "idj": match.joueur6, "points": match.score6, "pts total": tournoi.score_j6},
            {"nom": datajoueurs[f'{match.joueur7}'][0]["nom"] + " " + datajoueurs[f'{match.joueur7}'][0]["prenom"],
             "idj": match.joueur7, "points": match.score7, "pts total": tournoi.score_j7}
            ]
        # score_r3 contient les points qui se mettent à jour apres chaque match !!!

        joueursdict_tries = sorted(joueursdict, key=lambda x1: x1["pts total"], reverse=True)

        classement = []
        position = 1
        for x1 in joueursdict_tries:
            classement.append([position, x1["nom"], x1["idj"], x1["points"], x1["pts total"]])
            position += 1

        self.vue.afficher_classement(num_round, classement)

        time.sleep(0.8)

        # print("liste en fonction des points")
        liste_lj_r4 = []
        for x4 in classement:
            ljr4 = x4[2]
            liste_lj_r4.append(str(ljr4))
        # print(liste_lj_r4)
        tournoi.lj_r4 = liste_lj_r4

        # Pour enregistrement au bon endroit !!! sinon dernier par défaut tournoi.idtn
        print(f'tournoi.idtn: {tournoi.idtn}')
        print(f'num_round: {num_round}')
        update_tournoi(datatournois)

        # print(f'classement{classement}')

        self.creer_tour4()

    def liste_matchs_auto_r4(self):
        """ Permet de lister les matchs en fonction"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !

        with open("../modele/data/tournaments/tournois.json", "r") as f:
            datatournois = json.load(f)

        # print(datatournois)
        # créer Match Round1
        idtn = tournoi.idtn  # input("Entrez l'idtn du tournoi:\n")  # afficher liste des tournois !!!!!!!
        print("\n----------[Matchs]----------\n")
        num_round = 4  # input("Entrez le numéro du round:\n")  # peut etre ...afficher liste des round

        tournoi.lj_r4 = datatournois[f'{idtn}'][0]["lj_r4"]
        tournoi.matchs_r4 = datatournois[f'{idtn}'][0]["matchs_r4"]
        tournoi.score_j0 = datatournois[f'{idtn}'][0]["score_j0"]
        tournoi.score_j1 = datatournois[f'{idtn}'][0]["score_j1"]
        tournoi.score_j2 = datatournois[f'{idtn}'][0]["score_j2"]
        tournoi.score_j3 = datatournois[f'{idtn}'][0]["score_j3"]
        tournoi.score_j4 = datatournois[f'{idtn}'][0]["score_j4"]
        tournoi.score_j5 = datatournois[f'{idtn}'][0]["score_j5"]
        tournoi.score_j6 = datatournois[f'{idtn}'][0]["score_j6"]
        tournoi.score_j7 = datatournois[f'{idtn}'][0]["score_j7"]

        print(f'tournoi.matchs_r4{tournoi.matchs_r4}')

        # print(tournoi.lj_r4)

        liste_joueurs = (tournoi.matchs_r4[0], tournoi.matchs_r4[1], tournoi.matchs_r4[2],
                         tournoi.matchs_r4[3], tournoi.matchs_r4[4], tournoi.matchs_r4[5],
                         tournoi.matchs_r4[6], tournoi.matchs_r4[7])
        liste_joueurs_int = int(tournoi.matchs_r4[0]), int(tournoi.matchs_r4[1]), int(tournoi.matchs_r4[2]),\
                            int(tournoi.matchs_r4[3]), int(tournoi.matchs_r4[4]), int(tournoi.matchs_r4[5]),\
                            int(tournoi.matchs_r4[6]), int(tournoi.matchs_r4[7])
        # print(sorted(liste_joueurs, reverse=False))
        for i in liste_joueurs_int:
            setattr(match, "joueur" + str(i), liste_joueurs_int[i])

        a = 1.0
        b = 0.5
        c = 0.0
        x = [a, b, c]
        random.choice(x)
        score0 = random.choice([a, b, c])
        score2 = random.choice([a, b, c])
        score4 = random.choice([a, b, c])
        score6 = random.choice([a, b, c])
        match.score0 = score0
        match.score2 = score2
        match.score4 = score4
        match.score6 = score6

        if match.score0 == 1.0:
            match.score1 = 0.0
        elif match.score0 == 0.0:
            match.score1 = 1.0
        elif match.score0 == 0.5:
            match.score1 = 0.5

        if match.score2 == 1.0:
            match.score3 = 0.0
        elif match.score2 == 0.0:
            match.score3 = 1.0
        elif match.score2 == 0.5:
            match.score3 = 0.5

        if match.score4 == 1.0:
            match.score5 = 0.0
        elif match.score4 == 0.0:
            match.score5 = 1.0
        elif match.score4 == 0.5:
            match.score5 = 0.5

        if match.score6 == 1.0:
            match.score7 = 0.0
        elif match.score6 == 0.0:
            match.score7 = 1.0
        elif match.score6 == 0.5:
            match.score7 = 0.5

        match_m1_r4 = Match(idtn, num_round, match.joueur0, match.joueur1)
        print()
        print(f'----------[{match_m1_r4.nom_match}]----------')
        match.paire = tuple[(), ()]
        match.paire1 = [(match.joueur0, match.score0), (match.joueur1, match.score1)]
        print(match.paire1)

        print()
        if match.score0 > match.score1:
            print(f'----------Le joueur {match.joueur0} a gagné le match du Round{num_round} !----------')
        elif match.score0 == match.score1:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur1} a gagné le match du Round{num_round} !----------')

        match_m1_r4.lj_r4 = datatournois[f'{idtn}'][0]["lj_r4"]

        match_m2_r4 = Match(idtn, num_round, match.joueur2, match.joueur4)
        print()
        print(f'----------[{match_m2_r4.nom_match}]----------')
        match.paire2 = [(match.joueur2, match.score2), (match.joueur3, match.score3)]
        print(match.paire2)

        print()
        if match.score2 > match.score3:
            print(f'----------Le joueur {match.joueur2} a gagné le match du Round{num_round} !----------')
        elif match.score2 == match.score3:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur3} a gagné le match du Round{num_round} !----------')

        match_m2_r4.lj_r4 = datatournois[f'{idtn}'][0]["lj_r4"]

        match_m3_r4 = Match(idtn, num_round, match.joueur4, match.joueur5)
        print()
        print(f'----------[{match_m3_r4.nom_match}]----------')
        match.paire3 = [(match.joueur4, match.score4), (match.joueur5, match.score5)]
        print(match.paire3)

        print()
        if match.score4 > match.score5:
            print(f'----------Le joueur {match.joueur4} a gagné le match du Round{num_round} !----------')
        elif match.score4 == match.score5:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur5} a gagné le match du Round{num_round} !----------')

        match_m3_r4.lj_r4 = datatournois[f'{idtn}'][0]["lj_r4"]

        match_m4_r4 = Match(idtn, num_round, match.joueur6, match.joueur7)
        print()
        print(f'----------[{match_m4_r4.nom_match}]----------')
        match.paire4 = [(match.joueur6, match.score6), (match.joueur7, match.score7)]
        print(match.paire4)

        print()
        if match.score6 > match.score7:
            print(f'----------Le joueur {match.joueur6} a gagné le match du Round{num_round} !----------')
        elif match.score6 == match.score7:
            print(f'----------Il y a égalité pour le match du Round{num_round} !----------')
        else:
            print(f'----------Le joueur {match.joueur7} a gagné le match du Round{num_round} !----------')

        match_m4_r4.lj_r4 = datatournois[f'{idtn}'][0]["lj_r4"]

        tournoi.score_m1_r4 = match.paire1  # Tuple à stocker dans datatournois !!!!!!
        tournoi.score_m2_r4 = match.paire2
        tournoi.score_m3_r4 = match.paire3
        tournoi.score_m4_r4 = match.paire4

        time.sleep(0.8)

        update_tournoi(datatournois)

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            # Charge les données dans l'objet tournoi (en cours...)
            # Sinon
            # raise TypeError(f'Object of type {o.__class__.__name__} '
            # TypeError: Object of type type is not JSON serializable
            tournoi.idtn = 1

            self.serialiser_obj_tournois()

            # joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], daten=None)
            # joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], daten=None)
            # joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], daten=None)
            # joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], daten=None)
            # joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], daten=None)
            # joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], daten=None)
            # joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], daten=None)
            # joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], daten=None)
            # joueur9 = Joueur(nom=datajoueurs[8][0]["nom"], prenom=datajoueurs[8][0]["prenom"], daten=None)
            # pas plus de 10 joueurs car problème recup 2 digits lors des matchs/scores/points !!!!

        tournoi.score_j0 += match.score0
        tournoi.score_j1 += match.score1
        tournoi.score_j2 += match.score2
        tournoi.score_j3 += match.score3
        tournoi.score_j4 += match.score4
        tournoi.score_j5 += match.score5
        tournoi.score_j6 += match.score6
        tournoi.score_j7 += match.score7

        joueursdict = [
            {"nom": datajoueurs[f'{match.joueur0}'][0]["nom"] + " " + datajoueurs[f'{match.joueur0}'][0]["prenom"],
             "idj": match.joueur0, "points": match.score0, "pts total": tournoi.score_j0},
            {"nom": datajoueurs[f'{match.joueur1}'][0]["nom"] + " " + datajoueurs[f'{match.joueur1}'][0]["prenom"],
             "idj": match.joueur1, "points": match.score1, "pts total": tournoi.score_j1},
            {"nom": datajoueurs[f'{match.joueur2}'][0]["nom"] + " " + datajoueurs[f'{match.joueur2}'][0]["prenom"],
             "idj": match.joueur2, "points": match.score2, "pts total": tournoi.score_j2},
            {"nom": datajoueurs[f'{match.joueur3}'][0]["nom"] + " " + datajoueurs[f'{match.joueur3}'][0]["prenom"],
             "idj": match.joueur3, "points": match.score3, "pts total": tournoi.score_j3},
            {"nom": datajoueurs[f'{match.joueur4}'][0]["nom"] + " " + datajoueurs[f'{match.joueur4}'][0]["prenom"],
             "idj": match.joueur4, "points": match.score4, "pts total": tournoi.score_j4},
            {"nom": datajoueurs[f'{match.joueur5}'][0]["nom"] + " " + datajoueurs[f'{match.joueur5}'][0]["prenom"],
             "idj": match.joueur5, "points": match.score5, "pts total": tournoi.score_j5},
            {"nom": datajoueurs[f'{match.joueur6}'][0]["nom"] + " " + datajoueurs[f'{match.joueur6}'][0]["prenom"],
             "idj": match.joueur6, "points": match.score6, "pts total": tournoi.score_j6},
            {"nom": datajoueurs[f'{match.joueur7}'][0]["nom"] + " " + datajoueurs[f'{match.joueur7}'][0]["prenom"],
             "idj": match.joueur7, "points": match.score7, "pts total": tournoi.score_j7}
            ]
        # score_r4 contient les points qui se mettent à jour apres chaque match !!!

        joueursdict_tries = sorted(joueursdict, key=lambda x1: x1["pts total"], reverse=True)

        classement = []
        position = 1
        for x1 in joueursdict_tries:
            classement.append([position, x1["nom"], x1["idj"], x1["points"], x1["pts total"]])
            position += 1

        self.vue.afficher_classement(num_round, classement)

        time.sleep(0.8)

        # print("liste en fonction des points")
        # liste_lj_r4 = []
        # for x4 in classement:
        #     ljr4 = x4[2]
        #     liste_lj_r4.append(str(ljr4))
        # # print(liste_lj_r4)
        # tournoi.lj_r4 = liste_lj_r4

        # Pour enregistrement au bon endroit !!! sinon dernier par défaut tournoi.idtn
        print(f'tournoi.idtn: {tournoi.idtn}')
        print(f'num_round: {num_round}')
        update_tournoi(datatournois)

        # print(f'classement{classement}')

        for x1 in joueursdict_tries:
            classement.append([position, x1["nom"], x1["idj"], x1["points"], x1["pts total"]])
            break

        self.vue.afficher_gagnant(classement)
        image_gagnant()
        time.sleep(1)
        self.set_menu_options()


    def ajouter_joueur(self):
        """Permet d'ajouter un joueur dans la base de données via le prompt"""
        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

        #print(datajoueurs)

        liste_j_bdd = len(datajoueurs)
        #print(liste_j_bdd)
        if liste_j_bdd > 9:
            print("Il n'est pas possible d'ajouter plus de joueurs")
            self.set_menu_options()
        else:
            pass
        rep = "o"
        while rep == "o":

            nom, prenom, daten, yon = self.vue.afficher_ajouter_joueurs()

            joueur = Joueur(nom, prenom, daten)
            print(joueur.nom, joueur.prenom, joueur.daten)

            if yon == 1:
                print("Ajout d'un autre joueur...\n")
            else:
                self.vue.afficher_infos_joueurs(listej=self.infos_joueurs(stat="infos_joueurs"))

            # Changer répertoire de travail !!!
            # print(os.getcwd())
            # os.chdir("\\Users\olivier\PycharmProjects\projects\Tournoi-Echecs\modele")  # Corriger chemin Guillaume!!!
            # print(os.getcwd())
            # open("modele/data/tournaments/joueurs.json", "w+")
            # sérialiser


            # Création nouveau profil joueur:  # Manque incrément nb_joueurs +1 dans la classe joueur(init) !!!
            idx = len(datajoueurs)
            newjoueur = {f'{idx}': [{
                "date_de_naissance": daten,
                "id": idx,
                "nom": nom,
                "prenom": prenom,
                "sexe": "nc",
                "deja_joue": "nc"
            }]}

            datajoueurs.update(newjoueur)

            with open("../modele/data/tournaments/joueurs.json", "w") as f:
                json.dump(datajoueurs, f, indent=2, sort_keys=True)

                print(datajoueurs)

                quitter()

    def infos_joueurs(self, stat):
        """Affiche les informations des joueurs"""

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

            # Modification du nom à l'indice 0
            # datajoueurs["0"][0]["nom"] = "Lyon"  # Test modif dans dico .... ok

            # Afficher liste des joueurs de la base  # for in de datajoueurs

            listej = []
            lj = []
            for i in datajoueurs:
                joueur.idx = i
                joueur.nom = datajoueurs[f'{i}'][0]["nom"]
                try:
                    joueur.nom = joueur.nom.encode("latin1").decode("utf-8")
                except AttributeError:
                    pass
                    # print("\nLe champ description est vide !\n"
                    #       "'NoneType' object has no attribute 'encode'\n")
                joueur.prenom = datajoueurs[f'{i}'][0]["prenom"]
                try:
                    joueur.prenom = joueur.prenom.encode("latin1").decode("utf-8")
                except AttributeError:
                    pass
                    # print("\nLe champ description est vide !\n"
                    #       "'NoneType' object has no attribute 'encode'\n")
                # print(joueur.idx, joueur.nom, joueur.prenom)

                idj = joueur.idx
                nj = joueur.nom
                pj = joueur.prenom

                listej.append([str(idj)] + [str(nj)] + [str(pj)])

            # print(listej)
            # print(joueur.nom, joueur.prenom)

            if "stat4" not in stat:
                listej = self.vue.afficher_infos_joueurs(listej)
            else:
                pass

            if "stat4" in stat:

                listej_alpha = sorted(listej, key=lambda x1: x1[1], reverse=False)

                noms_alpha = []

                for x1 in listej_alpha:
                    noms_alpha.append([x1[0], x1[1], x1[2]])
                self.vue.afficher_stat4(noms_alpha)
            else:
                pass
            time.sleep(2)
            return listej, self.set_menu_options()

        # else:
        # print("prlm lecture joueurs.json")
        # print(os.getcwd())

    @staticmethod
    def joueurs_dejajoue(joueurx, joueursxdejajoue, listejoueurs):  # (joueurx, joueursdejajoue, listejoueurs)
        """Permet d'éviter que deux joueurs jouent à nouveau l'un contre l'autre
        et retourne le joueur suivant"""
        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!

        # print(datajoueurs)

        for i in joueurx:
            listejoueurs.remove(i)
            for x in joueursxdejajoue:
                if len(listejoueurs) == 0 and len(joueursxdejajoue) == 1:
                    pass
                else:
                    listejoueurs.remove(x)

        if len(listejoueurs) == 0:
            pass
        else:
            nextjoueurx = listejoueurs[0]
            print(f'nextjoueurx: {nextjoueurx}')
            return nextjoueurx

    def classement_tournoi(self):
        """ Permet de générer le classement général du tournoi en cours"""

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            id_tournoi = self.vue.prompt_id_tournoi()
            tournoi.idtn = id_tournoi
            self.serialiser_obj_tournois()
            #print(f'tournoi.idtn: {tournoi.idtn}')

            joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], idx="0", daten=None)
            joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], idx="1", daten=None)
            joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], idx="2", daten=None)
            joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], idx="3", daten=None)
            joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], idx="4", daten=None)
            joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], idx="5", daten=None)
            joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], idx="6", daten=None)
            joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], idx="7", daten=None)

        joueursdict = [
            {"nom": joueur0.nom + " " + joueur0.prenom, "idj": joueur0.idx, "points": joueur0.idx,
             "pts total": tournoi.score_j0},
            {"nom": joueur1.nom + " " + joueur1.prenom, "idj": joueur1.idx, "points": match.score1,
             "pts total": tournoi.score_j1},
            {"nom": joueur2.nom + " " + joueur2.prenom, "idj": joueur2.idx, "points": match.score2,
             "pts total": tournoi.score_j2},
            {"nom": joueur3.nom + " " + joueur3.prenom, "idj": joueur3.idx, "points": match.score3,
             "pts total": tournoi.score_j3},
            {"nom": joueur4.nom + " " + joueur4.prenom, "idj": joueur4.idx, "points": match.score4,
             "pts total": tournoi.score_j4},
            {"nom": joueur5.nom + " " + joueur5.prenom, "idj": joueur5.idx, "points": match.score5,
             "pts total": tournoi.score_j5},
            {"nom": joueur6.nom + " " + joueur6.prenom, "idj": joueur6.idx, "points": match.score6,
             "pts total": tournoi.score_j6},
            {"nom": joueur7.nom + " " + joueur7.prenom, "idj": joueur7.idx, "points": match.score7,
             "pts total": tournoi.score_j7}

        ]
        # score_r1 contient les points qui se mettent à jour apres chaque match !!!

        joueursdict_tries = sorted(joueursdict, key=lambda x1: x1["pts total"], reverse=True)

        print(f'joueursdict_tries{joueursdict_tries}')

        classement = []
        position = 1
        for x1 in joueursdict_tries:
            classement.append([position, x1["nom"], x1["idj"], x1["points"], x1["pts total"]])
            position += 1
        classement = self.vue.afficher_classement(1, classement)

        time.sleep(2)

    def rapports_tournoi(self, stat):
        """ Permet de générer des rapports (statistiques)"""

        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            # id_tournoi = self.vue.prompt_id_tournoi()
            # tournoi.idtn = id_tournoi
            self.serialiser_obj_tournois()
            # print(f'tournoi.idtn: {tournoi.idtn}')

            joueur0 = Joueur(nom=datajoueurs["0"][0]["nom"], prenom=datajoueurs["0"][0]["prenom"], idx="0", daten=None)
            joueur1 = Joueur(nom=datajoueurs["1"][0]["nom"], prenom=datajoueurs["1"][0]["prenom"], idx="1", daten=None)
            joueur2 = Joueur(nom=datajoueurs["2"][0]["nom"], prenom=datajoueurs["2"][0]["prenom"], idx="2", daten=None)
            joueur3 = Joueur(nom=datajoueurs["3"][0]["nom"], prenom=datajoueurs["3"][0]["prenom"], idx="3", daten=None)
            joueur4 = Joueur(nom=datajoueurs["4"][0]["nom"], prenom=datajoueurs["4"][0]["prenom"], idx="4", daten=None)
            joueur5 = Joueur(nom=datajoueurs["5"][0]["nom"], prenom=datajoueurs["5"][0]["prenom"], idx="5", daten=None)
            joueur6 = Joueur(nom=datajoueurs["6"][0]["nom"], prenom=datajoueurs["6"][0]["prenom"], idx="6", daten=None)
            joueur7 = Joueur(nom=datajoueurs["7"][0]["nom"], prenom=datajoueurs["7"][0]["prenom"], idx="7", daten=None)

        joueursdict = [
            {"nom": joueur0.nom + " " + joueur0.prenom, "idj": match.joueur0, "id": joueur0.idx, "points": match.score0,
             "pts total": tournoi.score_j0},
            {"nom": joueur1.nom + " " + joueur1.prenom, "idj": match.joueur1, "id": joueur1.idx, "points": match.score1,
             "pts total": tournoi.score_j1},
            {"nom": joueur2.nom + " " + joueur2.prenom, "idj": match.joueur2, "id": joueur2.idx, "points": match.score2,
             "pts total": tournoi.score_j2},
            {"nom": joueur3.nom + " " + joueur3.prenom, "idj": match.joueur3, "id": joueur3.idx, "points": match.score3,
             "pts total": tournoi.score_j3},
            {"nom": joueur4.nom + " " + joueur4.prenom, "idj": match.joueur4, "id": joueur4.idx, "points": match.score4,
             "pts total": tournoi.score_j4},
            {"nom": joueur5.nom + " " + joueur5.prenom, "idj": match.joueur5, "id": joueur5.idx, "points": match.score5,
             "pts total": tournoi.score_j5},
            {"nom": joueur6.nom + " " + joueur6.prenom, "idj": match.joueur6, "id": joueur6.idx, "points": match.score6,
             "pts total": tournoi.score_j6},
            {"nom": joueur7.nom + " " + joueur7.prenom, "idj": match.joueur7, "id": joueur7.idx, "points": match.score7,
             "pts total": tournoi.score_j7}

        ]
        # score_r1 contient les points qui se mettent à jour apres chaque match !!!

        joueursdict_alpha = sorted(joueursdict, key=lambda x1: x1["nom"], reverse=False)

        noms_alpha = []

        for x1 in joueursdict_alpha:
            noms_alpha.append([x1["id"], x1["nom"]])

        if "stat1" in stat:
            self.vue.afficher_stat1(noms_alpha)
        else:
            self.set_menu_options()

        time.sleep(1)

    def rapports_round_match(self):
        """ Permet de générer des rapports (statistiques)"""
        with open("../modele/data/tournaments/joueurs.json", "r") as f:
            datajoueurs = json.load(f)

            id_tournoi = self.vue.prompt_id_tournoi()
            tournoi.idtn = id_tournoi
            self.serialiser_obj_tournois()
            print(f'tournoi.idtn: {tournoi.idtn}')
            tournoidict = [
                {"round": "Round1",
                 "match1": tournoi.score_m1_r1,
                 "match2": tournoi.score_m2_r1,
                 "match3": tournoi.score_m3_r1,
                 "match4": tournoi.score_m4_r1},
                {"round": "Round2",
                 "match1": tournoi.score_m1_r2,
                 "match2": tournoi.score_m2_r2,
                 "match3": tournoi.score_m3_r2,
                 "match4": tournoi.score_m4_r2},
                {"round": "Round3",
                 "match1": tournoi.score_m1_r3,
                 "match2": tournoi.score_m2_r3,
                 "match3": tournoi.score_m3_r3,
                 "match4": tournoi.score_m4_r3},
                {"round": "Round4",
                 "match1": tournoi.score_m1_r4,
                 "match2": tournoi.score_m2_r4,
                 "match3": tournoi.score_m3_r4,
                 "match4": tournoi.score_m4_r4}
            ]
            rounds_matchs = []

            for x1 in tournoidict:
                rounds_matchs.append([x1["round"], x1["match1"], x1["match2"], x1["match3"], x1["match4"]])

            self.vue.afficher_stat5(rounds_matchs)

    def serialiser_obj_tournois(self):
        """Permet de charger les données json vers les objets tournoi, tour et match"""
        self.infos = "infos"  # juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f2:
            datatournois = json.load(f2)  # Vu pour changer le rep avec Guillaume -> "../" !!!!!!
            # Charge les données dans l'objet tournoi (en cours...)
            idt_tournoi = tournoi.idtn  # len(datatournois) - 1  # le dernier de la liste est l'actuel

            tournoi.nom_tournoi = datatournois[f'{idt_tournoi}'][0]["nom_tournoi"]
            try:
                tournoi.nom_tournoi = tournoi.nom_tournoi.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.date_debut = datatournois[f'{idt_tournoi}'][0]["date_debut"]
            tournoi.date_fin = datatournois[f'{idt_tournoi}'][0]["date_fin"]
            tournoi.nb_tours = datatournois[f'{idt_tournoi}'][0]["nb_tours"]
            tournoi.lieu = datatournois[f'{idt_tournoi}'][0]["lieu"]
            try:
                tournoi.lieu = tournoi.lieu.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.description = datatournois[f'{idt_tournoi}'][0]["description"]
            try:
                tournoi.description = tournoi.description.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.liste_joueurs = datatournois[f'{idt_tournoi}'][0]["liste_joueurs"]
            tournoi.liste_tours = datatournois[f'{idt_tournoi}'][0]["liste_tours"]
            tournoi.lj_r1 = datatournois[f'{idt_tournoi}'][0]["lj_r1"]
            tournoi.lj_r2 = datatournois[f'{idt_tournoi}'][0]["lj_r2"]
            tournoi.lj_r3 = datatournois[f'{idt_tournoi}'][0]["lj_r3"]
            tournoi.lj_r4 = datatournois[f'{idt_tournoi}'][0]["lj_r4"]
            tournoi.matchs_r1 = datatournois[f'{idt_tournoi}'][0]["matchs_r1"]
            tournoi.matchs_r2 = datatournois[f'{idt_tournoi}'][0]["matchs_r2"]
            tournoi.matchs_r3 = datatournois[f'{idt_tournoi}'][0]["matchs_r3"]
            tournoi.matchs_r4 = datatournois[f'{idt_tournoi}'][0]["matchs_r4"]
            tournoi.score_j0 = datatournois[f'{idt_tournoi}'][0]["score_j0"]
            tournoi.score_j1 = datatournois[f'{idt_tournoi}'][0]["score_j1"]
            tournoi.score_j2 = datatournois[f'{idt_tournoi}'][0]["score_j2"]
            tournoi.score_j3 = datatournois[f'{idt_tournoi}'][0]["score_j3"]
            tournoi.score_j4 = datatournois[f'{idt_tournoi}'][0]["score_j4"]
            tournoi.score_j5 = datatournois[f'{idt_tournoi}'][0]["score_j5"]
            tournoi.score_j6 = datatournois[f'{idt_tournoi}'][0]["score_j6"]
            tournoi.score_j7 = datatournois[f'{idt_tournoi}'][0]["score_j7"]
            match.score0 = datatournois[f'{idt_tournoi}'][0]["score0"]
            match.score1 = datatournois[f'{idt_tournoi}'][0]["score1"]
            match.score2 = datatournois[f'{idt_tournoi}'][0]["score2"]
            match.score3 = datatournois[f'{idt_tournoi}'][0]["score3"]
            match.score4 = datatournois[f'{idt_tournoi}'][0]["score4"]
            match.score5 = datatournois[f'{idt_tournoi}'][0]["score5"]
            match.score6 = datatournois[f'{idt_tournoi}'][0]["score6"]
            match.score7 = datatournois[f'{idt_tournoi}'][0]["score7"]
            match.liste_dj0 = datatournois[f'{idt_tournoi}'][0]["liste_dj0"]
            match.liste_dj1 = datatournois[f'{idt_tournoi}'][0]["liste_dj1"]
            match.liste_dj2 = datatournois[f'{idt_tournoi}'][0]["liste_dj2"]
            match.liste_dj3 = datatournois[f'{idt_tournoi}'][0]["liste_dj3"]
            match.liste_dj4 = datatournois[f'{idt_tournoi}'][0]["liste_dj4"]
            match.liste_dj5 = datatournois[f'{idt_tournoi}'][0]["liste_dj5"]
            match.liste_dj6 = datatournois[f'{idt_tournoi}'][0]["liste_dj6"]
            match.liste_dj7 = datatournois[f'{idt_tournoi}'][0]["liste_dj7"]
            tournoi.couleurs_r1 = datatournois[f'{idt_tournoi}'][0]["couleurs_r1"]
            tournoi.couleurs_r2 = datatournois[f'{idt_tournoi}'][0]["couleurs_r2"]
            tournoi.couleurs_r3 = datatournois[f'{idt_tournoi}'][0]["couleurs_r3"]
            tournoi.couleurs_r4 = datatournois[f'{idt_tournoi}'][0]["couleurs_r4"]
            tournoi.num_tour_actuel = datatournois[f'{idt_tournoi}'][0]["num_tour_actuel"]
            tournoi.score_m1_r1 = datatournois[f'{idt_tournoi}'][0]["score_m1_r1"]
            tournoi.score_m2_r1 = datatournois[f'{idt_tournoi}'][0]["score_m2_r1"]
            tournoi.score_m3_r1 = datatournois[f'{idt_tournoi}'][0]["score_m3_r1"]
            tournoi.score_m4_r1 = datatournois[f'{idt_tournoi}'][0]["score_m4_r1"]
            tournoi.score_m1_r2 = datatournois[f'{idt_tournoi}'][0]["score_m1_r2"]
            tournoi.score_m2_r2 = datatournois[f'{idt_tournoi}'][0]["score_m2_r2"]
            tournoi.score_m3_r2 = datatournois[f'{idt_tournoi}'][0]["score_m3_r2"]
            tournoi.score_m4_r2 = datatournois[f'{idt_tournoi}'][0]["score_m4_r2"]
            tournoi.score_m1_r3 = datatournois[f'{idt_tournoi}'][0]["score_m1_r3"]
            tournoi.score_m2_r3 = datatournois[f'{idt_tournoi}'][0]["score_m2_r3"]
            tournoi.score_m3_r3 = datatournois[f'{idt_tournoi}'][0]["score_m3_r3"]
            tournoi.score_m4_r3 = datatournois[f'{idt_tournoi}'][0]["score_m4_r3"]
            tournoi.score_m1_r4 = datatournois[f'{idt_tournoi}'][0]["score_m1_r4"]
            tournoi.score_m2_r4 = datatournois[f'{idt_tournoi}'][0]["score_m2_r4"]
            tournoi.score_m3_r4 = datatournois[f'{idt_tournoi}'][0]["score_m3_r4"]
            tournoi.score_m4_r4 = datatournois[f'{idt_tournoi}'][0]["score_m4_r4"]
            tournoi.idtn = datatournois[f'{idt_tournoi}'][0]["idtn"]

    def raz_scores(self):
        """ Permet de remettre à zéro tous les scores (Raz)"""

        self.infos = "infos"  # Ok juste pour enlever erreur creation méthode statique !
        with open("../modele/data/tournaments/tournois.json", "r") as f2:
            datatournois = json.load(f2)

            self.infos_tournois(liste_stats="liste_t")
            print("\n----------[Remise à zéro des scores !]----------\n")
            raz_input_t = int(input("Entrez l'id du tournoi pour la remise à zéro:\n"))
            if raz_input_t == 0:
                tournoi.idtn = raz_input_t
            elif raz_input_t == 1:
                tournoi.idtn = raz_input_t
            elif raz_input_t == 2:
                tournoi.idtn = raz_input_t
            else:
                print("Veuillez recommencer svp")
                self.raz_scores()

            idt_tournoi = tournoi.idtn  # len(datatournois) - 1  # le dernier de la liste est l'actuel

            tournoi.nom_tournoi = datatournois[f'{idt_tournoi}'][0]["nom_tournoi"]
            try:
                tournoi.nom_tournoi = tournoi.nom_tournoi.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.date_debut = datatournois[f'{idt_tournoi}'][0]["date_debut"]
            tournoi.date_fin = datatournois[f'{idt_tournoi}'][0]["date_fin"]
            tournoi.nb_tours = datatournois[f'{idt_tournoi}'][0]["nb_tours"]
            tournoi.lieu = datatournois[f'{idt_tournoi}'][0]["lieu"]
            try:
                tournoi.lieu = tournoi.lieu.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.description = datatournois[f'{idt_tournoi}'][0]["description"]
            try:
                tournoi.description = tournoi.description.encode("latin1").decode("utf-8")
            except AttributeError:
                pass
                # print("\nLe champ description est vide !\n"
                #       "'NoneType' object has no attribute 'encode'\n")
            tournoi.liste_joueurs = datatournois[f'{idt_tournoi}'][0]["liste_joueurs"]
            tournoi.liste_tours = datatournois[f'{idt_tournoi}'][0]["liste_tours"]
            tournoi.lj_r1 = datatournois[f'{idt_tournoi}'][0]["lj_r1"]
            tournoi.lj_r2 = datatournois[f'{idt_tournoi}'][0]["lj_r2"]
            tournoi.lj_r3 = datatournois[f'{idt_tournoi}'][0]["lj_r3"]
            tournoi.lj_r4 = datatournois[f'{idt_tournoi}'][0]["lj_r4"]
            tournoi.matchs_r1 = datatournois[f'{idt_tournoi}'][0]["matchs_r1"]
            tournoi.matchs_r2 = datatournois[f'{idt_tournoi}'][0]["matchs_r2"]
            tournoi.matchs_r3 = datatournois[f'{idt_tournoi}'][0]["matchs_r3"]
            tournoi.matchs_r4 = datatournois[f'{idt_tournoi}'][0]["matchs_r4"]
            tournoi.score_j0 = datatournois[f'{idt_tournoi}'][0]["score_j0"]
            tournoi.score_j1 = datatournois[f'{idt_tournoi}'][0]["score_j1"]
            tournoi.score_j2 = datatournois[f'{idt_tournoi}'][0]["score_j2"]
            tournoi.score_j3 = datatournois[f'{idt_tournoi}'][0]["score_j3"]
            tournoi.score_j4 = datatournois[f'{idt_tournoi}'][0]["score_j4"]
            tournoi.score_j5 = datatournois[f'{idt_tournoi}'][0]["score_j5"]
            tournoi.score_j6 = datatournois[f'{idt_tournoi}'][0]["score_j6"]
            tournoi.score_j7 = datatournois[f'{idt_tournoi}'][0]["score_j7"]
            match.score0 = datatournois[f'{idt_tournoi}'][0]["score0"]
            match.score1 = datatournois[f'{idt_tournoi}'][0]["score1"]
            match.score2 = datatournois[f'{idt_tournoi}'][0]["score2"]
            match.score3 = datatournois[f'{idt_tournoi}'][0]["score3"]
            match.score4 = datatournois[f'{idt_tournoi}'][0]["score4"]
            match.score5 = datatournois[f'{idt_tournoi}'][0]["score5"]
            match.score6 = datatournois[f'{idt_tournoi}'][0]["score6"]
            match.score7 = datatournois[f'{idt_tournoi}'][0]["score7"]
            match.liste_dj0 = datatournois[f'{idt_tournoi}'][0]["liste_dj0"]
            match.liste_dj1 = datatournois[f'{idt_tournoi}'][0]["liste_dj1"]
            match.liste_dj2 = datatournois[f'{idt_tournoi}'][0]["liste_dj2"]
            match.liste_dj3 = datatournois[f'{idt_tournoi}'][0]["liste_dj3"]
            match.liste_dj4 = datatournois[f'{idt_tournoi}'][0]["liste_dj4"]
            match.liste_dj5 = datatournois[f'{idt_tournoi}'][0]["liste_dj5"]
            match.liste_dj6 = datatournois[f'{idt_tournoi}'][0]["liste_dj6"]
            match.liste_dj7 = datatournois[f'{idt_tournoi}'][0]["liste_dj7"]
            tournoi.couleurs_r1 = datatournois[f'{idt_tournoi}'][0]["couleurs_r1"]
            tournoi.couleurs_r2 = datatournois[f'{idt_tournoi}'][0]["couleurs_r2"]
            tournoi.couleurs_r3 = datatournois[f'{idt_tournoi}'][0]["couleurs_r3"]
            tournoi.couleurs_r4 = datatournois[f'{idt_tournoi}'][0]["couleurs_r4"]
            tournoi.num_tour_actuel = datatournois[f'{idt_tournoi}'][0]["num_tour_actuel"]
            tournoi.idtn = datatournois[f'{idt_tournoi}'][0]["idtn"]

            tournoi.num_tour_actuel = 1
            tournoi.nb_tours = 4
            tournoi.liste_joueurs = None
            tournoi.lj_r1 = None
            tournoi.lj_r2 = None
            tournoi.lj_r3 = None
            tournoi.lj_r4 = None
            tournoi.couleurs_r1 = None
            tournoi.couleurs_r2 = None
            tournoi.couleurs_r3 = None
            tournoi.couleurs_r4 = None
            tournoi.matchs_r1 = None
            tournoi.matchs_r2 = None
            tournoi.matchs_r3 = None
            tournoi.matchs_r4 = None
            match.score0 = 0.0
            match.score1 = 0.0
            match.score2 = 0.0
            match.score3 = 0.0
            match.score4 = 0.0
            match.score5 = 0.0
            match.score6 = 0.0
            match.score7 = 0.0
            match.liste_dj0 = None
            match.liste_dj1 = None
            match.liste_dj2 = None
            match.liste_dj3 = None
            match.liste_dj4 = None
            match.liste_dj5 = None
            match.liste_dj6 = None
            match.liste_dj7 = None
            tournoi.score_j0 = 0.0
            tournoi.score_j1 = 0.0
            tournoi.score_j2 = 0.0
            tournoi.score_j3 = 0.0
            tournoi.score_j4 = 0.0
            tournoi.score_j5 = 0.0
            tournoi.score_j6 = 0.0
            tournoi.score_j7 = 0.0
            tournoi.score_m1_r1 = None
            tournoi.score_m1_r2 = None
            tournoi.score_m1_r3 = None
            tournoi.score_m1_r4 = None
            tournoi.score_m2_r1 = None
            tournoi.score_m2_r2 = None
            tournoi.score_m2_r3 = None
            tournoi.score_m2_r4 = None
            tournoi.score_m3_r1 = None
            tournoi.score_m3_r2 = None
            tournoi.score_m3_r3 = None
            tournoi.score_m3_r4 = None
            tournoi.score_m4_r1 = None
            tournoi.score_m4_r2 = None
            tournoi.score_m4_r3 = None
            tournoi.score_m4_r4 = None

            update_tournoi(datatournois)
            print("\n------Opération effectuée !------")
            time.sleep(0.8)


def update_tournoi(datatournois):
    """Mettre à jour les données saisies du tournoi"""
    update = {f'{tournoi.idtn}': [{
        "nom_tournoi": tournoi.nom_tournoi,
        "lieu": tournoi.lieu,
        "date_debut": tournoi.date_debut,
        "date_fin": tournoi.date_fin,
        "nb_tours": tournoi.nb_tours,
        "num_tour_actuel": tournoi.num_tour_actuel,
        "liste_tours": tournoi.liste_tours,
        "liste_joueurs": tournoi.liste_joueurs,
        "description": tournoi.description,
        "lj_r1": tournoi.lj_r1,
        "lj_r2": tournoi.lj_r2,
        "lj_r3": tournoi.lj_r3,
        "lj_r4": tournoi.lj_r4,
        "matchs_r1": tournoi.matchs_r1,
        "matchs_r2": tournoi.matchs_r2,
        "matchs_r3": tournoi.matchs_r3,
        "matchs_r4": tournoi.matchs_r4,
        "score0": match.score0,
        "score1": match.score1,
        "score2": match.score2,
        "score3": match.score3,
        "score4": match.score4,
        "score5": match.score5,
        "score6": match.score6,
        "score7": match.score7,
        "liste_dj0": match.liste_dj0,
        "liste_dj1": match.liste_dj1,
        "liste_dj2": match.liste_dj2,
        "liste_dj3": match.liste_dj3,
        "liste_dj4": match.liste_dj4,
        "liste_dj5": match.liste_dj5,
        "liste_dj6": match.liste_dj6,
        "liste_dj7": match.liste_dj7,
        "score_j0": tournoi.score_j0,
        "score_j1": tournoi.score_j1,
        "score_j2": tournoi.score_j2,
        "score_j3": tournoi.score_j3,
        "score_j4": tournoi.score_j4,
        "score_j5": tournoi.score_j5,
        "score_j6": tournoi.score_j6,
        "score_j7": tournoi.score_j7,
        "score_m1_r1": tournoi.score_m1_r1,
        "score_m2_r1": tournoi.score_m2_r1,
        "score_m3_r1": tournoi.score_m3_r1,
        "score_m4_r1": tournoi.score_m4_r1,
        "score_m1_r2": tournoi.score_m1_r2,
        "score_m2_r2": tournoi.score_m2_r2,
        "score_m3_r2": tournoi.score_m3_r2,
        "score_m4_r2": tournoi.score_m4_r2,
        "score_m1_r3": tournoi.score_m1_r3,
        "score_m2_r3": tournoi.score_m2_r3,
        "score_m3_r3": tournoi.score_m3_r3,
        "score_m4_r3": tournoi.score_m4_r3,
        "score_m1_r4": tournoi.score_m1_r4,
        "score_m2_r4": tournoi.score_m2_r4,
        "score_m3_r4": tournoi.score_m3_r4,
        "score_m4_r4": tournoi.score_m4_r4,
        "couleurs_r1": tournoi.couleurs_r1,
        "couleurs_r2": tournoi.couleurs_r2,
        "couleurs_r3": tournoi.couleurs_r3,
        "couleurs_r4": tournoi.couleurs_r4,
        "dateh_deb_r1": tour1.dateh_deb,
        "dateh_fin_r1": tour1.dateh_fin,
        "dateh_deb_r2": tour2.dateh_deb,
        "dateh_fin_r2": tour2.dateh_fin,
        "dateh_deb_r3": tour3.dateh_deb,
        "dateh_fin_r3": tour3.dateh_fin,
        "dateh_deb_r4": tour4.dateh_deb,
        "dateh_fin_r4": tour4.dateh_fin,
        "idtn": tournoi.idtn
    }]}
    datatournois.update(update)
    # gérer les try et éviter les modif si erreurs avant le dump
    with open("../modele/data/tournaments/tournois.json", "w") as f:
        json.dump(datatournois, f, indent=2, sort_keys=True)

        # print(datatournois)

    print("Sauvegarde effectuée")


def quitter():
    """ Quitter l'application """
    print("Au revoir !")
    sys.exit(0)


def image_gagnant():
    """Affiche une image Ascii Art de remise d'une coupe au gagnant"""
    obj = timg.Renderer()
    obj.load_image_from_file("../modele/data/gagnant.png")
    obj.resize(100, 40)
    obj.render(timg.ASCIIMethod)


controleur = Controleur()
controleur.run()

