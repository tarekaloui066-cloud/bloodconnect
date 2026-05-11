# BloodConnect - Système de Gestion des Dons de Sang

## Description
BloodConnect est une application web Django pour gérer les dons de sang, connectant les donneurs avec les hôpitaux pour les demandes urgentes et les campagnes de collecte.

## Fonctionnalités Principales
- 📝 Inscription et authentification (Donneur & Hôpital)
- 🩸 Historique des dons avec calcul d'éligibilité (56j/84j)
- 🆘 Appels urgents filtrés par groupe sanguin
- 📅 Campagnes de collecte de sang
- 📊 Tableau de bord administrateur avec statistiques

## Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd bloodconnect
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données
```bash
python manage.py migrate
```

### 5. Créer un compte administrateur
```bash
python manage.py createsuperuser
```

### 6. Charger les données de test (optionnel)
```bash
python manage.py loaddata fixtures/initial_data.json
```

## Utilisation

### Lancer le serveur de développement
```bash
python manage.py runserver
```

Accédez à l'application à `http://localhost:8000/`

### Accéder à l'admin Django
`http://localhost:8000/admin/` (avec les identifiants du superuser)

## Structure du Projet
- `accounts/` - Gestion des utilisateurs et authentification
- `donneur/` - App pour les donneurs de sang
- `hopital/` - App pour les hôpitaux
- `home/` - App d'accueil
- `templates/` - Templates HTML
- `media/` - Fichiers uploadés (photos de profil)

## Modèles Principaux
- **Donneur** - Profil donneur avec groupe sanguin
- **Hopital** - Profil hôpital
- **DemandeUrgente** - Demandes de sang urgentes
- **Don** - Historique des dons
- **Campagne** - Campagnes de collecte de sang
- **ReponseAppel** - Réponses aux demandes urgentes

## Technologies
- Django 6.0.3
- SQLite3
- HTML/CSS/JavaScript
- Bootstrap

## Auteur
BloodConnect Team