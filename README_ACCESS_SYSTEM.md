# 🧙‍♂️ JDR Manager - Système d'Accès Utilisateur

## 📖 Vue d'Ensemble

JDR Manager est une application Streamlit pour gérer les personnages et les campagnes de jeux de rôle. Elle inclut maintenant un **système complet de gestion des demandes d'accès** avec validation d'administrateur et changement de mot de passe obligatoire au premier login.

## 🚀 Démarrage Rapide

### Installation & Lancement

```bash
# 1. Cloner le projet
git clone <repo>
cd jdr-manager

# 2. Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Initialiser la base de données
python src/database/db_init.py

# 5. Lancer l'application
streamlit run src/app.py
```

L'app sera disponible à http://localhost:8502

## 🔐 Système d'Accès

### 3 Étapes pour un Nouvel Utilisateur

```
┌─────────────────────────────────────────────────────┐
│ 1️⃣  DEMANDE D'ACCÈS (Nouvel utilisateur)            │
├─────────────────────────────────────────────────────┤
│ - Cliquer "📝 Demande d'accès" sur login page      │
│ - Entrer identifiant + email                        │
│ - Validations : identifiant unique, email valide   │
│ - Demande enregistrée (status: PENDING)            │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2️⃣  VALIDATION ADMIN (Admin du site)                │
├─────────────────────────────────────────────────────┤
│ - Login avec compte admin                           │
│ - Accès onglet "👑 Administration"                  │
│ - Voir liste demandes en attente                    │
│ - Approuver → MDP temporaire généré               │
│ - Envoyer manuellement par email                    │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3️⃣  PREMIER LOGIN & CHANGEMENT MDP (Nouvel user)    │
├─────────────────────────────────────────────────────┤
│ - Login avec MDP temporaire                         │
│ - Page forcée : Changer le MDP                      │
│ - Exigences : 8+ chars, 1 maj, 1 min, 1 chiffre   │
│ - Après validation → Accès app                      │
└─────────────────────────────────────────────────────┘
```

### Comptes Par Défaut

| Username | Password | Rôle | Notes |
|----------|----------|------|-------|
| `admin` | `admin123` | admin | Créé au 1er démarrage |

⚠️ **Important** : Changer le mot de passe admin après 1er démarrage !

## 📚 Documentation

Pour plus de détails, consulter :

- **[QUICK_START.md](QUICK_START.md)** - Guide rapide (5 min)
- **[ACCES_REQUEST_FLOW.md](ACCES_REQUEST_FLOW.md)** - Flux complet détaillé
- **[ADMIN_EMAIL_GUIDE.md](ADMIN_EMAIL_GUIDE.md)** - Guide pour admin
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Résumé technique
- **[CHANGELOG.md](CHANGELOG.md)** - Historique des changements

## 🎯 Scénarios d'Utilisation

### Scénario 1 : Nouvel Utilisateur Demande l'Accès

```
Utilisateur → Clique "Demande d'accès" → Saisit données
→ BD enregistre demande (PENDING)
→ [Admin approuve plus tard]
```

**Validations côté client :**
- Identifiant : 3-20 chars, alphanumériques + underscore uniquement
- Email : Format valide (`user@domain.com`)
- Unicité : Identifiant ne doit pas exister
- Une demande par email maximum en attente

### Scénario 2 : Admin Approuve une Demande

```
Admin → Login admin → Onglet "Administration"
→ Voir demandes en attente → Clique "Approuver"
→ MDP temporaire généré et affiché
→ Admin envoie manuellement par email
→ DB créée avec user + flag must_change_password=1
```

### Scénario 3 : Nouvel User Login & Change MDP

```
User → Login avec MDP temporaire
→ Page forcée "Changement MDP obligatoire"
→ Saisir nouveau MDP (doit respecter exigences)
→ Confirmation
→ Flag réinitialisé → Accès app normale
```

## 🔧 Architecture

### Fichiers Principaux

```
src/
├── app.py                    # Point d'entrée
├── database/
│   ├── db_init.py           # Initialisation BD
│   └── email_config.py      # Config email (optionnel)
└── ui/
    ├── login.py             # Page login + lecture BD
    ├── access_request.py    # Page demande d'accès
    ├── password_change.py   # Page changement MDP
    ├── admin.py             # Panel administration
    └── lab.py               # App principale + onglet admin
```

### Base de Données

```
jdr_data.db
├── users (id, email, role, must_change_password)
├── requests (username, email, status, request_date)
└── characters (personnages des joueurs)
```

## 🔒 Sécurité

✅ **Implémenté :**
- Hachage des mots de passe
- Validations côté client
- Mot de passe temporaire aléatoire
- Forçage changement MDP 1er login
- Contrôle d'accès admin
- Requêtes SQL paramétrées

⚠️ **Recommandations Production :**
- HTTPS activé
- Admin change le MDP par défaut
- Sauvegardes BD régulières
- Configurer email auto pour MDP temporaires

## 🧪 Tests

Tests unitaires disponibles :

```bash
pytest tests/test_access_request.py -v
```

**Couverture :**
- Validation emails
- Validation identifiants
- Soumission demandes d'accès
- Gestion doublons

## 📧 Email (Optionnel)

Par défaut, l'envoi de mots de passe se fait **manuellement**.

Pour activer l'email automatique :
1. Lire [ADMIN_EMAIL_GUIDE.md](ADMIN_EMAIL_GUIDE.md)
2. Configurer `src/database/email_config.py`
3. Modifier `src/ui/admin.py` pour appeler la fonction
4. Tester

Options supportées : Gmail, SendGrid, SMTP personnalisé

## 🚀 Déploiement Streamlit Cloud

1. Pousser le code sur GitHub
2. Créer un compte Streamlit Cloud
3. Connecter le repo
4. Lancer l'app
5. Configurer secret pour les emails (si voulu)

[Docs Streamlit Cloud](https://docs.streamlit.io/streamlit-cloud)

## 📊 Flux Complet Visual

```
┌─────────────────┐
│ Visiteur Non    │
│ Connecté        │
└────────┬────────┘
         │
    ┌────▼─────────────┐
    │   PAGE LOGIN      │
    │   [Connexion]    │
    │   [Demande accès]│
    └─┬──────────────┬─┘
      │              │
      │ (Compte      │ (Pas encore
      │  existant)   │  de compte)
      │              │
      ▼              ▼
   [Connecté]  [Access Request Page]
      │              │
      │         ┌────▼─────────┐
      │         │ Saisir données│
      │         │ Valider       │
      │         │ Enregistrer BD│
      │         └────┬──────────┘
      │              │
      │         ┌────▼──────────────┐
      │         │ Admin approuve    │
      │         │ MDP temporaire    │
      │         │ Envoi manuel      │
      │         └────┬──────────────┘
      │              │
      │         ┌────▼──────────────┐
      │         │ 1er Login +       │
      │         │ Changement MDP    │
      │         │ Obligatoire       │
      │         └────┬──────────────┘
      │              │
      └──────┬───────┘
             │
        ┌────▼──────────┐
        │ [Connecté]    │
        │ ACCÈS APP     │
        │ JDR Manager   │
        └───────────────┘
```

## ✅ Checklist Déploiement

- [ ] Code testé localement
- [ ] BD initialisée (`python src/database/db_init.py`)
- [ ] Admin change le MDP par défaut
- [ ] Tests passent (`pytest tests/`)
- [ ] Documentation lue (QUICK_START.md minimum)
- [ ] Optionnel : Email configuré
- [ ] Optionnel : Déploiement Streamlit Cloud

## 📞 Support

Consulter la documentation :
- Problème démarrage ? → [QUICK_START.md](QUICK_START.md)
- Flux détaillé ? → [ACCES_REQUEST_FLOW.md](ACCES_REQUEST_FLOW.md)
- Admin questions ? → [ADMIN_EMAIL_GUIDE.md](ADMIN_EMAIL_GUIDE.md)
- Technique ? → [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## 📄 Licence

À compléter

## 👥 Équipe

JDR Manager - 2026

---

**Prêt à jouer !** 🎲
