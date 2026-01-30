# API REQUEST DATA INPI

Ce programme sert à récupérer les informations d'entreprise via l'API de DATA INPI et à les exporter sous un format Excel.

---

# Sommaire

# Architecture

# Guide d'instlalation 

## 1. Cloner le répertoire

``` bash
git clone git@github.com:Nassim-Naoui-BMI/data_inpi.git
cd data_inpi
```

## 2. Installer les dépendances avec Poetry

``` bash
poetry install
```

## 3. Généner le build de l'application "Desktop"

``` bash
poetry run pyinstaller --noconfirm --name "DataINPI_App" --onefile --windowed --add-data "src/data_inpi:data_inpi" --add-data "UI:UI" run.py
```

# Fonctionnalités