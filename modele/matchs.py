"""Classe Matchs"""


class Match:
    """Constructeur de Matchs"""
    def __init__(self, idtn, num_round, joueur0="nc", joueur1="nc"):
        joueur2 = "nc"
        joueur3 = "nc"
        joueur4 = "nc"
        joueur5 = "nc"
        joueur6 = "nc"
        joueur7 = "nc"
        liste_dj0 = None
        liste_dj1 = None
        liste_dj2 = None
        liste_dj3 = None
        liste_dj4 = None
        liste_dj5 = None
        liste_dj6 = None
        liste_dj7 = None
        self.nom_match = f'Match Round{num_round}: Joueur{joueur0} vs Joueur{joueur1}'
        self.joueur0 = joueur0
        self.joueur1 = joueur1  # paire = (joueur1, 0.0), (joueur2, 0.0)
        self.joueur2 = joueur2
        self.joueur3 = joueur3
        self.joueur4 = joueur4
        self.joueur5 = joueur5
        self.joueur6 = joueur6
        self.joueur7 = joueur7
        self.paire = tuple[(), ()]
        self.paire1_r1 = None
        self.paire2_r1 = None
        self.paire3_r1 = None
        self.paire4_r1 = None
        self.paire1_r2 = None
        self.paire2_r2 = None
        self.paire3_r2 = None
        self.paire4_r2 = None
        self.paire1_r3 = None
        self.paire2_r3 = None
        self.paire3_r3 = None
        self.paire4_r3 = None
        self.paire1_r4 = None
        self.paire2_r4 = None
        self.paire3_r4 = None
        self.paire4_r4 = None
        self.lj_r1 = None  # récup depuis Tournois.json à mettre à jour !!!!!!
        self.score = "score"
        self.score_r1 = None
        self.score_r2 = None
        self.score0 = None
        self.score1 = None
        self.score2 = None
        self.score3 = None
        self.score4 = None
        self.score5 = None
        self.score6 = None
        self.score7 = None
        self.liste_dj0 = liste_dj0
        self.liste_dj1 = liste_dj1
        self.liste_dj2 = liste_dj2
        self.liste_dj3 = liste_dj3
        self.liste_dj4 = liste_dj4
        self.liste_dj5 = liste_dj5
        self.liste_dj6 = liste_dj6
        self.liste_dj7 = liste_dj7

        self.round = round  # Round1, Round2,...
        self.nb_paires = None  # Si 4 joueurs 2 paires...
        self.points = None  # 1, 0 ou 0,5 point
        self.resultats_r1 = None  # Gagnant perdant ou nul
        self.resultats_r2 = None
        self.resultats_r3 = None
        self.resultats_r4 = None
        self.idtn = idtn
        self.score_j0_r1 = 0.0
        self.score_j1_r1 = 0.0
        self.score_j2_r1 = 0.0
        self.score_j3_r1 = 0.0
        self.score_j4_r1 = 0.0
        self.score_j5_r1 = 0.0
        self.score_j6_r1 = 0.0
        self.score_j7_r1 = 0.0
        self.score_j0_r2 = 0.0
        self.score_j1_r2 = 0.0
        self.score_j2_r2 = 0.0
        self.score_j3_r2 = 0.0
        self.score_j4_r2 = 0.0
        self.score_j5_r2 = 0.0
        self.score_j6_r2 = 0.0
        self.score_j7_r2 = 0.0
        self.score_j0_r3 = 0.0
        self.score_j1_r3 = 0.0
        self.score_j2_r3 = 0.0
        self.score_j3_r3 = 0.0
        self.score_j4_r3 = 0.0
        self.score_j5_r3 = 0.0
        self.score_j6_r3 = 0.0
        self.score_j7_r3 = 0.0
        self.score_j0_r4 = 0.0
        self.score_j1_r4 = 0.0
        self.score_j2_r4 = 0.0
        self.score_j3_r4 = 0.0
        self.score_j4_r4 = 0.0
        self.score_j5_r4 = 0.0
        self.score_j6_r4 = 0.0
        self.score_j7_r4 = 0.0


match = Match(idtn=int, num_round=int, joueur0="nc", joueur1="nc")
