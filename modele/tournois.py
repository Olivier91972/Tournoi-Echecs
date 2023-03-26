"""Classe Tournoi"""

#import pprint


class Tournoi:
    """Constructeur du tournoi"""

    def __init__(self, nom_tournoi, lieu, date_debut, idn="nc", nb_tours=4, idtn=0):
        date_fin = None
        self.nom_tournoi = nom_tournoi
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.description = None
        self.nb_tours = nb_tours
        self.num_tour_actuel = "num_tour_actuel"
        self.liste_tours = "liste_tours"
        self.idn = idn
        self.joueur = "joueur"
        self.liste_joueurs = None
        self.lj_r1 = None  #liste joueurs Round 1 (puis est aléatoire ensuite [arr])
        self.lj_r2 = None  # doit etre triée par points !
        self.lj_r3 = None
        self.lj_r4 = None
        self.matchs_r1 = None
        self.matchs_r2 = None
        self.matchs_r3 = None
        self.matchs_r4 = None
        self.score_j0 = None
        self.score_j1 = None
        self.score_j2 = None
        self.score_j3 = None
        self.score_j4 = None
        self.score_j5 = None
        self.score_j6 = None
        self.score_j7 = None
        self.couleurs_r1 = None
        self.couleurs_r2 = None
        self.couleurs_r3 = None
        self.couleurs_r4 = None
        self.score_m1_r1 = None
        self.score_m2_r1 = None
        self.score_m3_r1 = None
        self.score_m4_r1 = None
        self.score_m1_r2 = None
        self.score_m2_r2 = None
        self.score_m3_r2 = None
        self.score_m4_r2 = None
        self.score_m1_r3 = None
        self.score_m2_r3 = None
        self.score_m3_r3 = None
        self.score_m4_r3 = None
        self.score_m1_r4 = None
        self.score_m2_r4 = None
        self.score_m3_r4 = None
        self.score_m4_r4 = None
        self.idtn = idtn





tournoi = Tournoi(nom_tournoi="nc", lieu="nc", date_debut="nc", idn="nc", nb_tours=4, idtn=0)
# print(tournoi.nom_tournoi, tournoi.lieu)

#print(infos_tournoi())
#afficher = Vue()



