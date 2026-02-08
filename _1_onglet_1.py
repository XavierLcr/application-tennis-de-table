################################################################################
# Application pour un tournoi à pénalités                                      #
# Auteur : Xavier Lacour                                                       #
# 1. Script de création de l'onglet n°1                                        #
################################################################################


# 0 -- Initialisation ----------------------------------------------------------


import os, yaml, copy
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QCheckBox,
    QComboBox,
    QMessageBox,
    QGroupBox,
    QFormLayout,
)
from PyQt6.QtCore import pyqtSignal, Qt

import constantes
from _0_fonctions_utiles import trier_cles_par_params, associer_intervalle


# 1 -- Onglet n°1 --------------------------------------------------------------


class Onglet1(QWidget):
    data_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.sauvegarde = constantes.sauvegarde

        self.individus = {}
        self.matchs_joues = {}
        layout = QVBoxLayout()

        # === Partie en cours === #

        groupbox_partie = QGroupBox("Partie en cours")
        layout_partie = QHBoxLayout()
        self.nom_partie = QComboBox()
        self.nom_partie.setEditable(True)
        self.nom_partie.addItems(list(constantes.sauvegarde.keys()))
        self.nom_partie.setCurrentText("")
        layout_partie.addWidget(self.nom_partie)
        self.nom_partie.currentIndexChanged.connect(self.initialiser_sauvegarde)
        self.nouvelle_partie = QPushButton("Nouvelle partie")
        layout_partie.addWidget(self.nouvelle_partie)
        self.nouvelle_partie.clicked.connect(self.ajouter_partie)
        self.btn_supprimer_partie = QPushButton("Supprimer cette partie")
        layout_partie.addWidget(self.btn_supprimer_partie)
        self.btn_supprimer_partie.clicked.connect(self.supprimer_partie)
        groupbox_partie.setLayout(layout_partie)
        layout.addWidget(groupbox_partie)

        # === Gestion des individus === #

        # --- Ajout d'individu --- #

        groupbox_ajout_individu = QGroupBox("Ajouter un individu")
        layout_ajout_individu = QVBoxLayout()
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
        layout_ajout_indiv_1 = QHBoxLayout()
        layout_ajout_indiv_2 = QHBoxLayout()
        layout_ajout_indiv_1.addWidget(self.input_nom)
        layout_ajout_indiv_2.addWidget(self.input_nombre)
        layout_ajout_indiv_1.addWidget(self.debut_partie)
        layout_ajout_indiv_2.addWidget(btn_ajouter)
        layout_ajout_individu.addLayout(layout_ajout_indiv_1)
        layout_ajout_individu.addLayout(layout_ajout_indiv_2)
        groupbox_ajout_individu.setLayout(layout_ajout_individu)

        # --- Suppression d'un individu --- #

        groupbox_supprimer_indiv = QGroupBox("Supprimer un individu")
        self.layout_suppression_indiv = QVBoxLayout()
        self.liste_indiv_suppression = QComboBox()
        self.bouton_supprimer_individu = QPushButton("Supprimer cet individu")
        self.bouton_supprimer_individu.clicked.connect(self.supprimer_individu)
        self.layout_suppression_indiv.addWidget(self.liste_indiv_suppression)
        self.layout_suppression_indiv.addWidget(self.bouton_supprimer_individu)
        groupbox_supprimer_indiv.setLayout(self.layout_suppression_indiv)

        # --- Mise côte-à-côte des deux groupboxes --- #

        layout_individu = QHBoxLayout()
        layout_individu.addWidget(groupbox_ajout_individu)
        layout_individu.addWidget(groupbox_supprimer_indiv)
        layout_individu.setStretch(0, 2)
        layout_individu.setStretch(1, 1)
        layout.addLayout(layout_individu)

        # === Matchs === #

        # --- Ajout des matchs --- #

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

        # --- Suppression du dernier match --- #

        groupbox_suppression_match = QGroupBox("Supprimer le dernier match")
        layout_suppression_match = QVBoxLayout()
        self.qlabel_dernier_match = QLabel()
        self.qlabel_dernier_match.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_QLabel_dernier_match()
        btn_supprimer_match = QPushButton("Supprimer le match")
        btn_supprimer_match.clicked.connect(self.supprimer_dernier_match)
        layout_suppression_match.addWidget(self.qlabel_dernier_match)
        layout_suppression_match.addWidget(btn_supprimer_match)
        groupbox_suppression_match.setLayout(layout_suppression_match)

        # --- Mise côte-à-côte des deux groupboxes --- #

        layout_matchs = QHBoxLayout()
        layout_matchs.addWidget(groupbox_match)
        layout_matchs.addWidget(groupbox_suppression_match)
        layout_matchs.setStretch(0, 5)
        layout_matchs.setStretch(1, 3)
        layout.addLayout(layout_matchs)

        # === Layout global === #

        self.setLayout(layout)

    def ajouter_partie(self):
        nom = self.nom_partie.currentText()
        if nom:
            if nom not in list(self.sauvegarde.keys()):
                self.sauvegarde[nom] = {"Joueurs": {}, "Matchs": {}}
                self.individus = {}
                self.matchs_joues = {}
                self.nom_partie.addItem(nom)
                self.gagnant.clear()
                self.perdant.clear()
                self.liste_indiv_suppression.clear()
                self.creer_sauvegarde()
                # self.nom_partie.setCurrentIndex(self.nom_partie.currentIndex() + 1)
                self.data_changed.emit(self.individus)
                self.set_QLabel_dernier_match()

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
                cle: valeur
                for cle, valeur in constantes.sauvegarde.items()
                if cle != nom
            }
            self.individus = {}
            self.matchs_joues = {}
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
            self.set_QLabel_dernier_match()

    def supprimer_individu(self):

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
            if nom_joueur in self.sauvegarde[nom_partie].get("Joueurs", {}):

                # Suppression
                del self.sauvegarde[nom_partie]["Joueurs"][nom_joueur]

                self.individus = self.sauvegarde[self.nom_partie.currentText()].get(
                    "Joueurs", {}
                )
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
                self.individus = self.sauvegarde[self.nom_partie.currentText()].get(
                    "Joueurs", {}
                )
                self.matchs_joues = self.sauvegarde[self.nom_partie.currentText()].get(
                    "Matchs", {}
                )
                self.input_nom.clear()
                self.input_nombre.setValue(0)
                self.gagnant.clear()
                self.perdant.clear()
                self.liste_indiv_suppression.clear()
                self.gagnant.addItems(list(self.individus.keys()))
                self.perdant.addItems(list(self.individus.keys()))
                self.liste_indiv_suppression.addItems(list(self.individus.keys()))
                self.data_changed.emit(self.individus)
                self.set_QLabel_dernier_match()

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

            self.sauvegarde[self.nom_partie.currentText()]["Joueurs"] = self.individus
            self.creer_sauvegarde()

            # Mise à jour de l'onglet 2
            self.data_changed.emit(self.individus)
        else:
            QMessageBox.warning(self, "Erreur", "Nom vide ou déjà existant.")

    def ajouter_match(self):

        # Récupéartion des noms des joueurs
        nom1 = self.gagnant.currentText()
        nom2 = self.perdant.currentText()

        if nom1 == nom2:

            # Les joueurs doivent être différents
            QMessageBox.warning(
                self, "Erreur", "Un match nécessite deux individus différents."
            )

        elif self.nom_partie.currentText() not in self.sauvegarde:

            # La partie doit exister
            QMessageBox.warning(self, "Erreur", "Aucune partie n'est chargée.")

        else:

            # Tri des joueurs
            liste_joueurs = trier_cles_par_params(
                self.individus, "points_reference", "points_officiels"
            )

            # Mise à jour des matchs gagnés/joués
            self.individus[nom1]["matches_joues"] = (
                self.individus[nom1]["matches_joues"] + 1
            )
            self.individus[nom1]["matches_gagnes"] = (
                self.individus[nom1].get("matches_gagnes", 0) + 1
            )
            self.individus[nom2]["matches_joues"] = (
                self.individus[nom2]["matches_joues"] + 1
            )

            # Ajout du nombre de points du vainqueur
            pts_gagnant = associer_intervalle(
                intervalles=constantes.intervalles_gagnant_points,
                valeur=liste_joueurs.index(nom1) - liste_joueurs.index(nom2),
            )
            self.individus[nom1]["points_reference"] = (
                self.individus[nom1]["points_reference"] + pts_gagnant
            )

            # Ajout du nombre de points du perdant
            pts_perdant = copy.copy(constantes.points_defaite)
            self.individus[nom2]["points_reference"] = (
                self.individus[nom2]["points_reference"] + pts_perdant
            )

            # Ajout du match à la liste de matchs
            self.matchs_joues[max(self.matchs_joues.keys(), default=-1) + 1] = {
                "gagnant": nom1,
                "perdant": nom2,
                "pts_gagnant": pts_gagnant,
                "pts_perdant": pts_perdant,
            }

            # Mise à jour des données
            self.sauvegarde[self.nom_partie.currentText()]["Joueurs"] = copy.deepcopy(
                self.individus
            )
            self.sauvegarde[self.nom_partie.currentText()]["Matchs"] = copy.deepcopy(
                self.matchs_joues
            )

            self.creer_sauvegarde()
            self.data_changed.emit(self.individus)

            QMessageBox.information(self, "Match ajouté", f"{nom1} bat {nom2} !")
            self.set_QLabel_dernier_match()

    def creer_sauvegarde(self):

        with open(
            os.path.join(constantes.dossier_donnees, "sauvegarde_parties.yaml"),
            "w",
            encoding="utf-8",
        ) as f:
            yaml.dump(self.sauvegarde, f, allow_unicode=True, default_flow_style=False)

    def set_QLabel_dernier_match(self):

        if not self.matchs_joues:
            self.qlabel_dernier_match.setText("Aucun match n'a été joué.")
        else:
            self.qlabel_dernier_match.setText(
                "Dernier match : "
                f"{self.matchs_joues[max(self.matchs_joues.keys(), default=-1)].get('gagnant', '')}"
                " bat "
                f"{self.matchs_joues[max(self.matchs_joues.keys(), default=-1)].get('perdant', '')}"
                "."
            )

    def supprimer_dernier_match(self):

        # Récupération de la clef dernier match
        clef = max(self.matchs_joues.keys(), default=-1)

        if clef == -1:

            # Erreur si le dernier match est inexistant
            QMessageBox.warning(self, "Erreur", "Aucun match n'a été joué.")

        else:

            # Récupération du dernier match
            gagnant = self.matchs_joues.get(clef).get("gagnant")
            perdant = self.matchs_joues.get(clef).get("perdant")
            pts_gagnant = self.matchs_joues.get(clef).get("pts_gagnant")
            pts_perdant = self.matchs_joues.get(clef).get("pts_perdant")

            reponse = QMessageBox.question(
                self,
                "Confirmation de suppression",
                f"Souhaitez-vous définitivement supprimer le match suivant : {gagnant} bat {perdant} ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reponse == QMessageBox.StandardButton.Yes:

                # Pour le gagnant
                if gagnant in self.individus:

                    # Mise à jour des matchs gagnés/joués
                    self.individus[gagnant]["matches_joues"] = (
                        self.individus[gagnant]["matches_joues"] - 1
                    )
                    self.individus[gagnant]["matches_gagnes"] = (
                        self.individus[gagnant].get("matches_gagnes", 0) - 1
                    )

                    # Suppression des points
                    self.individus[gagnant]["points_reference"] = (
                        self.individus[gagnant]["points_reference"] - pts_gagnant
                    )

                # Pour le perdant
                if perdant in self.individus:

                    # Mise à jour des matchs gagnés/joués
                    self.individus[perdant]["matches_joues"] = (
                        self.individus[perdant]["matches_joues"] - 1
                    )

                    # Suppression des point
                    self.individus[perdant]["points_reference"] = (
                        self.individus[perdant]["points_reference"] - pts_perdant
                    )

                # Suppression du match dans l'historique
                del self.matchs_joues[clef]

                # Mise à jour de la sauvegarde
                self.sauvegarde[self.nom_partie.currentText()]["Joueurs"] = (
                    copy.deepcopy(self.individus)
                )
                self.sauvegarde[self.nom_partie.currentText()]["Matchs"] = (
                    copy.deepcopy(self.matchs_joues)
                )

                self.creer_sauvegarde()
                self.data_changed.emit(self.individus)

                # Charger le nouveau dernier match
                self.set_QLabel_dernier_match()
