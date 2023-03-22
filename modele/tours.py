"""Classe qui défini les tours(Rounds)"""

from datetime import datetime


class Tours:
    """Constructeur du tour(round)"""
    def __init__(self, num_round):
        self.nom_round = f'Round{num_round}'
        self.liste_matchs = []
        self.date_debut = None
        self.date_fin = None
        self.dateh_deb = None
        self.dateh_fin = None
        self.dateh_deb_r1 = None
        self.dateh_fin_r1 = None
        self.dateh_deb_r2 = None
        self.dateh_fin_r2 = None
        self.dateh_deb_r3 = None
        self.dateh_fin_r3 = None
        self.dateh_deb_r4 = None
        self.dateh_fin_r4 = None

    def debut(self):
        """Date et heure de début du tour(round)"""
        self.dateh_deb = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
        return self.dateh_deb

    def fin(self):
        """Date et heure de fin du tour(round)"""
        self.dateh_fin = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')
        return self.dateh_fin


tour1 = Tours(num_round=1)
tour2 = Tours(num_round=2)
tour3 = Tours(num_round=3)
tour4 = Tours(num_round=4)
