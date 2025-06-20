from cx_Freeze import setup, Executable

setup(
    name="Compétition hebdomadaire",
    version="1.0",
    description="",
    options={
        "build_exe": {
            "packages": ["os", "sys", "PyQt6", "yaml"],
            "include_files": [
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
