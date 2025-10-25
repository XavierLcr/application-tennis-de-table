################################################################################
# Application pour le tennis de table                                          #
# Constantes                                                                   #
################################################################################


# 1 -- Initialisation ----------------------------------------------------------


import os, yaml


# 2 -- Définition des chemins --------------------------------------------------


dossier_donnees = "Données"


# 3 -- Ouverture des fichiers --------------------------------------------------


## 3.1 -- Sauvegrade des parties -----------------------------------------------


try:

    with open(
        os.path.join(dossier_donnees, "sauvegarde_parties.yaml"),
        "r",
        encoding="utf-8",
    ) as file:
        sauvegarde = yaml.safe_load(file)

except:

    sauvegarde = {}


## 3.2 -- Chargement des intervalles de points ---------------------------------


try:

    with open(
        os.path.join(dossier_donnees, "points_gagnes_par_match.yaml"),
        "r",
        encoding="utf-8",
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
