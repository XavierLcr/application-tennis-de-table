from cx_Freeze import setup, Executable

setup(
    name="Compétition hebdomadaire",
    version="1.0",
    description="",
    options={
        "build_exe": {
            "build_exe": r"C:\Users\xaruo\Documents\Tennis de table\Logiciel pour Florian\application-tennis-de-table\application",
            "packages": ["os", "sys", "PyQt6", "yaml"],
            "include_files": [
                "points_gagnes_par_match.yaml",
                "theme.css",
            ],
        }
    },
    executables=[
        Executable(
            "main.py",
            icon="logo-club.ico",
            target_name="Compétition hebdomadaire.exe",
            base="Win32GUI",
        )
    ],
)
