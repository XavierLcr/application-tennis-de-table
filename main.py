import sys
import os
import yaml
import copy
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox,
    QScrollArea,
    QGroupBox,
    QGridLayout,
    QFormLayout,
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
import fonctions_utiles

# Chargement d'une sauvegrade si elle existe
try:
    with open(
        os.path.join("sauvegarde_parties.yaml"),
        "r",
        encoding="utf-8",
    ) as file:
        sauvegarde = yaml.safe_load(file)
except:
    sauvegarde = {}

# Chargement des intervalles de points s'ils existent
try:

    with open(
        os.path.join("points_gagnes_par_match.yaml"), "r", encoding="utf-8"
    ) as file:
        points_par_match = yaml.safe_load(file)

        # Récupération des points du gagnant
        intervalles_gagnant_points = [
            ((float(item["min"]), float(item["max"])), item["points"])
            for item in points_par_match["intervalles_gagnant_points"]
        ]

        # Récupération des points du perdant
        points_defaite = points_par_match["points_defaite"]


except:

    # Valeurs par défaut
    intervalles_gagnant_points = [
        ((float("-inf"), -3), 4),
        ((-3, 0), 6),
        ((0, 4), 8),
        ((4, float("inf")), 10),
    ]
    points_defaite = 2


class Onglet1(QWidget):
    data_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.sauvegarde = sauvegarde

        self.individus = {}
        layout = QVBoxLayout()

        # --- Partie en cours ---
        groupbox_partie = QGroupBox("Partie en cours")
        layout_partie = QHBoxLayout()
        self.nom_partie = QComboBox()
        self.nom_partie.setEditable(True)
        self.nom_partie.addItems(list(sauvegarde.keys()))
        self.nom_partie.setCurrentText("")
        layout_partie.addWidget(self.nom_partie)
        self.nouvelle_partie = QPushButton("Nouvelle partie")
        layout_partie.addWidget(self.nouvelle_partie)
        self.nouvelle_partie.clicked.connect(self.ajouter_partie)
        self.btn_supprimer_partie = QPushButton("Supprimer cette partie")
        layout_partie.addWidget(self.btn_supprimer_partie)
        self.btn_supprimer_partie.clicked.connect(self.supprimer_partie)
        groupbox_partie.setLayout(layout_partie)
        layout.addWidget(groupbox_partie)

        # --- Ajout d'individu ---
        groupbox_individu = QGroupBox("Ajouter un individu")
        hbox_individu = QHBoxLayout()
        self.input_nom = QLineEdit()
        self.input_nom.setPlaceholderText("Nom de l'individu")
        self.nom_partie.blockSignals(True)
        self.nom_partie.setCurrentIndex(-1)
        self.nom_partie.blockSignals(False)
        self.input_nombre = QSpinBox()
        self.input_nombre.setRange(0, 10000)
        self.input_nombre.setPrefix("Points : ")
        btn_ajouter = QPushButton("Ajouter")
        btn_ajouter.clicked.connect(self.ajouter_individu)
        self.debut_partie = QCheckBox("Début de partie")
        self.debut_partie.setToolTip(
            "Si la case est cochée, le nombre de points à saisir correspond au classement officiel du joueur, afin de créer un classement de départ.\nSinon, cela correspond au nombre de points avec lequel le joueur débute la partie."
        )
        self.debut_partie.setChecked(True)
        hbox_individu.addWidget(self.input_nom)
        hbox_individu.addWidget(self.input_nombre)
        hbox_individu.addWidget(self.debut_partie)
        hbox_individu.addWidget(btn_ajouter)
        groupbox_individu.setLayout(hbox_individu)
        layout.addWidget(groupbox_individu)

        # --- Matchs ---
        groupbox_match = QGroupBox("Ajouter un match entre deux individus")
        self.gagnant = QComboBox()
        self.perdant = QComboBox()
        btn_match = QPushButton("Ajouter le match")
        btn_match.clicked.connect(self.ajouter_match)
        form_layout = QFormLayout()
        form_layout.addRow("Vainqueur :", self.gagnant)
        form_layout.addRow("Perdant :", self.perdant)
        form_layout.addRow(btn_match)
        groupbox_match.setLayout(form_layout)

        # --- Supprimer un individu ---
        groupbox_supprimer_indiv = QGroupBox("Supprimer un individu")
        self.layout_suppression_indiv = QVBoxLayout()
        self.liste_indiv_suppression = QComboBox()
        self.bouton_supprimer_individu = QPushButton("Supprimer cet individu")
        self.bouton_supprimer_individu.clicked.connect(self.supprimer_joueur)
        self.layout_suppression_indiv.addWidget(self.liste_indiv_suppression)
        self.layout_suppression_indiv.addWidget(self.bouton_supprimer_individu)
        groupbox_supprimer_indiv.setLayout(self.layout_suppression_indiv)

        # Mise côte-à-côte des deux groupboxes
        groupbox_match_layout = QHBoxLayout()
        groupbox_match_layout.addWidget(groupbox_match)
        groupbox_match_layout.addWidget(groupbox_supprimer_indiv)
        groupbox_match_layout.setStretch(0, 2)  # petite colonne gauche
        groupbox_match_layout.setStretch(1, 1)

        layout.addLayout(groupbox_match_layout)

        self.nom_partie.currentIndexChanged.connect(self.initialiser_sauvegarde)

        self.setLayout(layout)

    def ajouter_partie(self):
        nom = self.nom_partie.currentText()
        if nom:
            if nom not in list(self.sauvegarde.keys()):
                self.sauvegarde[nom] = {}
                self.individus = {}
                self.nom_partie.addItem(nom)
                self.gagnant.clear()
                self.perdant.clear()
                self.liste_indiv_suppression.clear()
                self.creer_sauvegarde()
                # self.nom_partie.setCurrentIndex(self.nom_partie.currentIndex() + 1)
                self.data_changed.emit(self.individus)

            else:
                QMessageBox.warning(self, "Erreur", "Cette partie existe déjà.")

    def supprimer_partie(self):

        # Récupération du nom de la partie
        nom = self.nom_partie.currentText()
        if not nom:
            return

        # Pop-up de confirmation
        reponse = QMessageBox.question(
            self,
            "Confirmation de suppression",
            f"Souhaitez-vous définitivement supprimer la partie « {nom} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        # Si confirmation de suppression
        if reponse == QMessageBox.StandardButton.Yes:
            self.sauvegarde = {
                cle: valeur for cle, valeur in sauvegarde.items() if cle != nom
            }
            self.individus = {}
            self.nom_partie.removeItem(self.nom_partie.findText(nom))
            self.nom_partie.blockSignals(True)
            self.nom_partie.setCurrentText("")
            self.nom_partie.setCurrentIndex(-1)
            self.nom_partie.blockSignals(False)
            self.gagnant.clear()
            self.perdant.clear()
            self.liste_indiv_suppression.clear()
            self.creer_sauvegarde()
            self.data_changed.emit(self.individus)

    def supprimer_joueur(self):

        # Récupération du nom de la partie
        nom_partie = self.nom_partie.currentText()
        if not nom_partie:
            return

        # Récupération du nom du joueur
        nom_joueur = self.liste_indiv_suppression.currentText()
        if not nom_joueur:
            return

        # Pop-up de confirmation
        reponse = QMessageBox.question(
            self,
            "Confirmation de suppression",
            f"Souhaitez-vous définitivement supprimer {nom_joueur} de cette partie ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        # Si confirmation de suppression
        if reponse == QMessageBox.StandardButton.Yes:

            # Si le joueur est dans la partie
            if nom_joueur in self.sauvegarde[nom_partie]:

                # Suppression
                del self.sauvegarde[nom_partie][nom_joueur]

                self.individus = self.sauvegarde[self.nom_partie.currentText()]
                self.gagnant.clear()
                self.perdant.clear()
                self.liste_indiv_suppression.clear()
                self.gagnant.addItems(list(self.individus.keys()))
                self.perdant.addItems(list(self.individus.keys()))
                self.liste_indiv_suppression.addItems(list(self.individus.keys()))
                self.creer_sauvegarde()
                self.data_changed.emit(self.individus)

    def initialiser_sauvegarde(self):
        if self.nom_partie.currentText() is not None:
            if self.nom_partie.currentText() in self.sauvegarde.keys():
                self.individus = self.sauvegarde[self.nom_partie.currentText()]
                self.input_nom.clear()
                self.input_nombre.setValue(0)
                self.gagnant.clear()
                self.perdant.clear()
                self.liste_indiv_suppression.clear()
                self.gagnant.addItems(list(self.individus.keys()))
                self.perdant.addItems(list(self.individus.keys()))
                self.liste_indiv_suppression.addItems(list(self.individus.keys()))
                self.data_changed.emit(self.individus)

    def ajouter_individu(self):
        nom = self.input_nom.text().strip()
        debut = self.debut_partie.isChecked()
        valeur = self.input_nombre.value()

        if self.nom_partie.currentText() not in self.sauvegarde:
            QMessageBox.warning(self, "Erreur", "Aucune partie n'est chargée.")

        elif nom and nom not in self.individus:
            indiv = {
                "points_officiels": 0,
                "points_reference": 0,
                "matches_joues": 0,
            }
            if debut:
                indiv["points_officiels"] = valeur
            else:
                indiv["points_reference"] = valeur

            self.individus[nom] = indiv
            self.gagnant.addItem(nom)
            self.perdant.addItem(nom)
            self.liste_indiv_suppression.addItem(nom)
            self.input_nom.clear()
            self.input_nombre.setValue(0)

            self.sauvegarde[self.nom_partie.currentText()] = self.individus
            self.creer_sauvegarde()

            # Mise à jour de l'onglet 2
            self.data_changed.emit(self.individus)
        else:
            QMessageBox.warning(self, "Erreur", "Nom vide ou déjà existant.")

    def ajouter_match(self):
        nom1 = self.gagnant.currentText()
        nom2 = self.perdant.currentText()

        if nom1 == nom2:
            QMessageBox.warning(
                self, "Erreur", "Un match nécessite deux individus différents."
            )
        elif self.nom_partie.currentText() not in self.sauvegarde:
            QMessageBox.warning(self, "Erreur", "Aucune partie n'est chargée.")
        else:

            liste_joueurs = fonctions_utiles.trier_cles_par_params(
                self.individus, "points_reference", "points_officiels"
            )

            self.individus[nom1]["matches_joues"] = (
                self.individus[nom1]["matches_joues"] + 1
            )
            self.individus[nom1]["matches_gagnes"] = (
                self.individus[nom1].get("matches_gagnes", 0) + 1
            )
            self.individus[nom2]["matches_joues"] = (
                self.individus[nom2]["matches_joues"] + 1
            )

            self.individus[nom1]["points_reference"] = self.individus[nom1][
                "points_reference"
            ] + fonctions_utiles.associer_intervalle(
                intervalles=intervalles_gagnant_points,
                valeur=liste_joueurs.index(nom1) - liste_joueurs.index(nom2),
            )
            self.individus[nom2]["points_reference"] = (
                self.individus[nom2]["points_reference"] + points_defaite
            )
            self.sauvegarde[self.nom_partie.currentText()] = copy.deepcopy(
                self.individus
            )

            self.creer_sauvegarde()
            self.data_changed.emit(self.individus)

            QMessageBox.information(self, "Match ajouté", f"{nom1} bat {nom2} !")

    def creer_sauvegarde(self):

        with open(
            os.path.join("sauvegarde_parties.yaml"),
            "w",
            encoding="utf-8",
        ) as f:
            yaml.dump(self.sauvegarde, f, allow_unicode=True, default_flow_style=False)


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
        self.liste_noms_tri = fonctions_utiles.trier_cles_par_params(
            dict_joueurs, "points_reference", "points_officiels"
        )
        self.afficher_classement(dict_joueurs)

    def envoyer_signal_bouton(self):
        self.bouton_maj_classement_clique.emit(True)

    def afficher_classement(self, dict_joueurs):
        for i in reversed(range(self.layout_resume_classement.count())):
            widget = self.layout_resume_classement.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.layout_resume_classement.addWidget(
            QLabel("Rang"), 0, 0, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_resume_classement.addWidget(
            QLabel("Joueur"), 0, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_resume_classement.addWidget(
            QLabel("Points"), 0, 2, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_resume_classement.addWidget(
            QLabel("Classement officiel"), 0, 3, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_resume_classement.addWidget(
            QLabel("Matchs joués"), 0, 4, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_resume_classement.addWidget(
            QLabel("Part de victoires"), 0, 5, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_resume_classement.addWidget(
            QLabel("Points/Match"), 0, 6, alignment=Qt.AlignmentFlag.AlignCenter
        )

        for row, nom_joueur in enumerate(self.liste_noms_tri, start=1):
            joueur_info = dict_joueurs[nom_joueur]

            if row <= 3:
                place = ["🥇", "🥈", "🥉"][row - 1]
            else:
                place = f"{row}ème"

            self.layout_resume_classement.addWidget(
                QLabel(f"{place}"), row, 0, alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.layout_resume_classement.addWidget(
                QLabel(nom_joueur), row, 1, alignment=Qt.AlignmentFlag.AlignCenter
            )
            self.layout_resume_classement.addWidget(
                QLabel(str(joueur_info["points_reference"])),
                row,
                2,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )
            self.layout_resume_classement.addWidget(
                QLabel(str(joueur_info["points_officiels"])),
                row,
                3,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )
            self.layout_resume_classement.addWidget(
                QLabel(str(joueur_info["matches_joues"])),
                row,
                4,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )

            # Stats
            if joueur_info["matches_joues"] == 0:
                ratio_victoires = ""
                ratio_points = ""
            else:
                ratio_victoires = (
                    str(
                        round(
                            100
                            * joueur_info.get("matches_gagnes", 0)
                            / joueur_info["matches_joues"],
                            1,
                        )
                    ).replace(".", ",")
                    + " %"
                )
                ratio_points = str(
                    round(
                        joueur_info["points_reference"] / joueur_info["matches_joues"],
                        1,
                    )
                ).replace(".", ",")

            self.layout_resume_classement.addWidget(
                QLabel(ratio_victoires),
                row,
                5,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )

            self.layout_resume_classement.addWidget(
                QLabel(ratio_points),
                row,
                6,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )

        self.layout_resume_classement.setRowStretch(len(self.liste_noms_tri) + 1, 6)


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compétition hebdomadaire")

        self.setWindowIcon(QIcon("logo-club.ico"))

        onglets = QTabWidget()
        self.onglet_1 = Onglet1()
        self.onglet_2 = Onglet2(self.onglet_1.individus)
        self.onglet_1.data_changed.connect(self.onglet_2.mettre_a_jour)

        onglets.addTab(self.onglet_1, "Compétition ​🏓​")
        onglets.addTab(self.onglet_2, "Classement 🏆​")
        self.setCentralWidget(onglets)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("theme.css") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        pass
    fenetre = FenetrePrincipale()
    fenetre.resize(600, 400)
    fenetre.show()
    sys.exit(app.exec())
