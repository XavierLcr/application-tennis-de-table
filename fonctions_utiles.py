def trier_cles_par_params(dictionnaire, *parametres):
    # Créer une liste de tuples : (clé, valeur_param1, valeur_param2, ...)
    cles_et_valeurs = [
        (cle, *(sous_dict[param] for param in parametres))
        for cle, sous_dict in dictionnaire.items()
    ]

    # Trier les tuples selon tous les paramètres donnés, dans l'ordre décroissant
    cles_et_valeurs_triees = sorted(
        cles_et_valeurs,
        key=lambda x: tuple(-v for v in x[1:]),
    )

    # Extraire uniquement les clés triées
    return [cle for cle, *_ in cles_et_valeurs_triees]


def associer_intervalle(intervalles, valeur):
    for (borne_min, borne_max), label in intervalles:
        if borne_min <= valeur < borne_max:
            return label
