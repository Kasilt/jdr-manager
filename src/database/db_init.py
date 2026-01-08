import sqlite3
import streamlit_authenticator as stauth
import os

# Nom de la base de données (Le fichier physique sur le disque)
DB_NAME = "jdr_data.db"

def init_db():
    print(f"--- Initialisation de la base {DB_NAME} ---")
    
    # Connexion (équivalent à ouvrir la librairie)
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # ---------------------------------------------------------
    # 1. TABLE USERS (Sécurité)
    # Équivalent : DSPUSRPRF
    # ---------------------------------------------------------
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            password_hash TEXT,
            role TEXT DEFAULT 'joueur',  -- 'admin' ou 'joueur'
            must_change_password BOOLEAN DEFAULT 0
        )
    ''')
    print("✓ Table 'users' vérifiée.")

    # ---------------------------------------------------------
    # 2. TABLE REQUESTS (File d'attente)
    # Équivalent : JOBQ pour les inscriptions
    # ---------------------------------------------------------
    c.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            username TEXT PRIMARY KEY,
            email TEXT,
            status TEXT DEFAULT 'PENDING',
            temp_password TEXT,
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Table 'requests' vérifiée.")

    # ---------------------------------------------------------
    # 3. TABLE CHARACTERS (Données Métier)
    # Équivalent : Fichier Physique PF_PERSO
    # ---------------------------------------------------------
    c.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,             -- Lien vers la table users (Clé étrangère)
            nom_perso TEXT,
            classe TEXT,
            force INTEGER,
            pv_max INTEGER,
            pv_actuel INTEGER,
            xp INTEGER DEFAULT 0,
            inventaire_json TEXT,      -- On stockera la liste d'objets en texte brut
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    print("✓ Table 'characters' vérifiée.")

    # ---------------------------------------------------------
    # CRÉATION DU PREMIER ADMIN (QSECOFR)
    # Pour que vous puissiez vous connecter la première fois !
    # ---------------------------------------------------------
    
    # On vérifie si l'admin existe déjà pour ne pas l'écraser
    admin_exist = c.execute("SELECT 1 FROM users WHERE username='admin'").fetchone()
    
    if not admin_exist:
        print("Création du compte administrateur par défaut...")
        # Mot de passe par défaut : admin123
        hashed_pass = stauth.Hasher().hash('admin123')
        
        c.execute('''
            INSERT INTO users (username, name, email, password_hash, role, must_change_password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', 'Maitre du Jeu', 'admin@jdr.com', hashed_pass, 'admin', 0))
        print("✓ Compte 'admin' créé (Mot de passe: admin123)")
    else:
        print("ℹ️ Le compte admin existe déjà.")

    # Validation finale (COMMIT)
    conn.commit()
    conn.close()
    print("\n--- Terminée avec succès ---")

if __name__ == "__main__":
    # Ceci permet de lancer le script directement
    init_db()