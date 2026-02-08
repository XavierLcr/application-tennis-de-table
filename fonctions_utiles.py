################################################################################
# Application pour un tournoi à pénalités                                      #
# Auteur : Xavier Lacour                                                       #
# Script contenant des fonctions utiles                                        #
################################################################################


# 1 -- Fonction de tri d'un dictionnaire de dictionnaires selon des clefs ------


def trier_cles_par_params(dictionnaire, *parametres):

    # Trier les tuples selon tous les paramètres donnés, dans l'ordre décroissant
    cles_et_valeurs_triees = sorted(
        # Créer la liste de tuples : (clé, valeur_param1, valeur_param2, ...)
        [
            (cle, *(sous_dict[param] for param in parametres))
            for cle, sous_dict in dictionnaire.items()
        ],
        key=lambda x: tuple(-v for v in x[1:]),
    )

    # Extraire uniquement les clés triées
    return [cle for cle, *_ in cles_et_valeurs_triees]


# 2 -- Fonction de renvoi du nombre de points gagnés ---------------------------


def associer_intervalle(intervalles, valeur):
    for (borne_min, borne_max), label in intervalles:
        if borne_min <= valeur < borne_max:
            return label
