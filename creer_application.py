from cx_Freeze import setup, Executable
from constantes import dossier_donnees
import os

setup(
    name="Compétition hebdomadaire",
    version="1.0",
    description="",
    options={
        "build_exe": {
            "build_exe": r"C:\Users\xaruo\Documents\Tennis de table\Logiciel pour Florian\application-tennis-de-table\application",
            "packages": ["os", "sys", "PyQt6", "yaml"],
            "include_files": [(dossier_donnees, dossier_donnees)],
        }
    },
    executables=[
        Executable(
            "main.py",
            icon=os.path.join(dossier_donnees, "logo-club.ico"),
            target_name="Compétition hebdomadaire.exe",
            base="Win32GUI",
        )
    ],
)
