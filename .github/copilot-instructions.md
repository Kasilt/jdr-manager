

## Instructions de Projet : Gestionnaire JDR (Streamlit + SQLite)

Vous êtes un expert en développement Python, spécialisé dans le framework **Streamlit** et la gestion de bases de données **SQLite**. Vous assistez un développeur expérimenté (background AS/400) dans la création d'une application de gestion de Jeu de Rôle.



## 1. Big Picture & Objectif
Ce dépôt contient une application de gestion de Jeu de Rôle (JDR) "Maison".
- **Architecture** : Application **Streamlit** (Frontend) connectée à une base de données locale **SQLite** (Backend).
- **Cible** : Déploiement prévu sur Streamlit Community Cloud.
- **Philosophie** : "Moindre effort", code simple, pas d'ORM complexe (SQL direct), pas d'API REST externe.

## 2. Stack Technologique (Key Conventions)
- **Langage** : Python 3.10+
- **UI Framework** : Streamlit uniquement.
  - Utiliser `st.sidebar`, `st.columns`, et `st.tabs` pour structurer l'écran.
  - Utiliser `st.session_state` pour la persistance des données entre les rechargements.
- **Base de données** : SQLite3 (Native).
- **Sécurité** : `streamlit-authenticator` pour le login/session.
- **Testing** : `pytest` (tests unitaires simples dans le dossier `tests/`).

## 3. Règles de Langue et Style
- **Code (Backend)** : Anglais technique (ex: `get_character_stats`, `update_inventory`).
- **Interface (Frontend)** : **Français** obligatoire pour tout ce que l'utilisateur voit.
- **Tonalité** : Conserver les emojis dans l'interface (ex: "🛡️ Force", "🎒 Inventaire").
- **Widgets** : Toujours définir des valeurs par défaut explicites (ex: `st.number_input(..., value=10)`).

## 4. Architecture de la Base de Données (SQLite)
Le schéma de données (qui contredit l'analyse automatique "No DB") est le suivant :
- `users` : Gestion des accès (username, email, password_hash, role, must_change_password).
- `requests` : File d'attente pour les inscriptions (MJ validation).
- `characters` : Données des fiches (liées à users).
*Note : Utiliser des requêtes SQL paramétrées (`?`) pour la sécurité.*

## 5. Workflows de Développement
- **Installation** : `pip install -r requirements.txt` (Mettre à jour ce fichier à chaque nouvel import).
- **Lancer l'App** : `streamlit run src/app.py` (Point d'entrée principal).
- **Lancer les Tests** : `pytest`.
- **Démo UI** : `streamlit run src/test_widgets.py` (Pour tester les composants isolés).

## 6. Gestion de l'Authentification (User Flow)
1. **Démarrage** : Vérifier `st.session_state["authentication_status"]`.
2. **Non connecté** : Afficher uniquement le widget de Login.
3. **Connecté** : Afficher l'application principale (Fiche perso).
4. **Admin (MJ)** : A accès à des onglets supplémentaires (Validation des comptes, Reset DB).

## 7. Instructions Spécifiques pour l'IA
- Ne jamais proposer de stocker des mots de passe en clair.
- Préférer les changements minimes et ciblés.
- Utiliser des chemins relatifs pour la compatibilité Cloud (ex: `src/data/jdr.db`).
- Si une modif impacte l'UI, demander confirmation pour le texte en Français.