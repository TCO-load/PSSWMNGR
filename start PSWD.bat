@echo off
setlocal enabledelayedexpansion

:: Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer Python et l'ajouter au PATH.
    echo Redirection vers la page de telechargement de Python...
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Vérifier si pip est installé
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip n'est pas installe ou n'est pas dans le PATH.
    echo Veuillez installer pip et l'ajouter au PATH.
    pause
    exit /b 1
)

:: Vérifier si cryptography est installé
python -c "import cryptography" >nul 2>&1
if %errorlevel% neq 0 (
    echo La bibliotheque cryptography n'est pas installee. Installation en cours...
    pip install cryptography
    if %errorlevel% neq 0 (
        echo Erreur lors de l'installation de cryptography.
        pause
        exit /b 1
    )
    echo cryptography a ete installe avec succes.
) else (
    echo La bibliotheque cryptography est deja installee.
)

:: Exécuter le programme Python
echo Lancement du gestionnaire de mots de passe...
python password_manager.py

:: Pause à la fin de l'exécution
pause