################################################################################
# Application pour un tournoi à pénalités                                      #
# Auteur : Xavier Lacour                                                       #
# 3. Script principal de l'application                                         #
################################################################################


# 0 -- Initialisation ----------------------------------------------------------


import sys, os
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
)
from PyQt6.QtGui import QIcon

import constantes
from _1_onglet_1 import Onglet1
from _2_onglet_2 import Onglet2


# 1 -- Classe principale de l'application --------------------------------------


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compétition hebdomadaire")

        self.setWindowIcon(
            QIcon(os.path.join(constantes.dossier_donnees, "logo-club.ico"))
        )

        onglets = QTabWidget()
        self.onglet_1 = Onglet1()
        self.onglet_2 = Onglet2(self.onglet_1.individus)
        self.onglet_1.data_changed.connect(self.onglet_2.mettre_a_jour)

        onglets.addTab(self.onglet_1, "Compétition ​🏓​")
        onglets.addTab(self.onglet_2, "Classement 🏆​")
        self.setCentralWidget(onglets)


# 2 -- Exécution ---------------------------------------------------------------


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open(os.path.join(constantes.dossier_donnees, "theme.css")) as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass
    fenetre = FenetrePrincipale()
    fenetre.resize(600, 400)
    fenetre.show()
    sys.exit(app.exec())
