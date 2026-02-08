################################################################################
# Application pour un tournoi à pénalités                                      #
# Auteur : Xavier Lacour                                                       #
# 2. Script de création de l'onglet n°2                                        #
################################################################################


# 0 -- Initialisation ----------------------------------------------------------


from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt6.QtCore import pyqtSignal, Qt

from _0_fonctions_utiles import trier_cles_par_params


# 1 -- Onglet n°2 --------------------------------------------------------------


class Onglet2(QWidget):

    bouton_maj_classement_clique = pyqtSignal(bool)

    def __init__(self, dict_joueurs: dict):
        super().__init__()

        self.layout_resume_classement = QGridLayout()
        self.classement = QWidget()
        self.classement.setLayout(self.layout_resume_classement)
        self.classement_general = QScrollArea()
        self.classement_general.setWidgetResizable(True)
        self.classement_general.setWidget(self.classement)
        layout = QVBoxLayout()
        layout.addWidget(self.classement_general)
        self.mettre_a_jour(dict_joueurs)
        self.setLayout(layout)

    def mettre_a_jour(self, dict_joueurs):
        self.liste_noms_tri = trier_cles_par_params(
            dict_joueurs, "points_reference", "points_officiels"
        )
        self.afficher_classement(dict_joueurs)

    def envoyer_signal_bouton(self):
        self.bouton_maj_classement_clique.emit(True)

    def afficher_classement(self, dict_joueurs):
        # Supprimer l'ancien widget s'il existe
        for i in reversed(range(self.layout_resume_classement.count())):
            widget = self.layout_resume_classement.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Créer un QTableWidget
        table = QTableWidget(len(self.liste_noms_tri), 7)
        table.setHorizontalHeaderLabels(
            [
                "Rang",
                "Joueur",
                "Points",
                "Classement\nofficiel",
                "Matchs joués",
                "Part de\nvictoires",
                "Points/Match",
            ]
        )
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)

        # Remplir le tableau
        for row, nom_joueur in enumerate(self.liste_noms_tri, start=0):
            joueur_info = dict_joueurs[nom_joueur]
            if row < 3:
                place = ["🥇", "🥈", "🥉"][row]
            else:
                place = f"{row+1}ème"

            table.setItem(row, 0, QTableWidgetItem(place))
            table.setItem(row, 1, QTableWidgetItem(nom_joueur))
            table.setItem(
                row,
                2,
                QTableWidgetItem(
                    format(joueur_info["points_reference"], ",").replace(",", " ")
                ),
            )
            table.setItem(
                row,
                3,
                QTableWidgetItem(
                    format(joueur_info["points_officiels"], ",").replace(",", " ")
                ),
            )
            table.setItem(
                row,
                4,
                QTableWidgetItem(
                    format(joueur_info["matches_joues"], ",").replace(",", " ")
                ),
            )

            if joueur_info["matches_joues"] == 0:
                ratio_victoires = ""
                ratio_points = ""
            else:
                ratio_victoires = f"{round(100 * joueur_info.get('matches_gagnes', 0) / joueur_info['matches_joues'], 1):.0f} %".replace(
                    ".", ","
                )
                ratio_points = f"{round(joueur_info['points_reference'] / joueur_info['matches_joues'], 1):.1f}".replace(
                    ".", ","
                )

            table.setItem(row, 5, QTableWidgetItem(ratio_victoires))
            table.setItem(row, 6, QTableWidgetItem(ratio_points))

            # Alignement centré pour toutes les cellules
            for col in range(7):
                item = table.item(row, col)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style avec QSS
        table.setStyleSheet(
            """
            QTableWidget {
                border: 1px solid #D0D0D0;
                gridline-color: #D0D0D0;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #F0F0F0;
                padding: 4px;
                border: 1px solid #D0D0D0;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #D0E4FF;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A0A0A0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """
        )

        # Ajouter le tableau au layout
        self.layout_resume_classement.addWidget(table)
