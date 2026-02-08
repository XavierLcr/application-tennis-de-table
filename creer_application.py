################################################################################
# Application pour un tournoi à pénalités                                      #
# Auteur : Xavier Lacour                                                       #
# Script afin de créer le .exe de l'application                                #
################################################################################


# 0 -- Initialisation ----------------------------------------------------------


from cx_Freeze import setup, Executable
from constantes import dossier_donnees
import os


# 1 -- Création du .exe --------------------------------------------------------


setup(
    name="Compétition hebdomadaire",
    version="1.2",
    description="",
    options={
        "build_exe": {
            "build_exe": os.path.join(
                r"C:\Users",
                "xaruo",
                "Documents",
                "Tennis de table",
                "Logiciel pour Florian",
                "application-tennis-de-table",
                "Application compilée",
            ),
            "packages": ["os", "sys", "PyQt6", "yaml"],
            "include_files": [(dossier_donnees, dossier_donnees)],
        }
    },
    executables=[
        Executable(
            "main.py",
            icon=os.path.join(dossier_donnees, "logo-club.ico"),
            target_name="Compétition hebdomadaire.exe",
            base="gui",
        )
    ],
)
