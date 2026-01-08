# 📝 CHANGELOG - Système de Demande d'Accès

## [2026-01-08] - Système de Demande d'Accès Complet

### ✨ Nouvelles Fonctionnalités

#### 1. Page de Demande d'Accès
- **Fichier** : `src/ui/access_request.py`
- Formulaire pour les nouveaux utilisateurs
- Validation identifiant (3-20 chars, alphanumériques + underscore)
- Validation email (format RFC5322 simplifié)
- Vérification unicité identifiant
- Vérification demande existante par email
- Enregistrement en BD avec status `PENDING`

#### 2. Page d'Administration
- **Fichier** : `src/ui/admin.py`
- Panel accessible aux utilisateurs avec rôle `admin`
- Liste les demandes en attente
- Génération automatique mot de passe temporaire (8 chars)
- Création compte utilisateur avec flag `must_change_password=1`
- Option rejet des demandes
- Affichage du MDP temporaire pour copie manuelle

#### 3. Page Changement de Mot de Passe Obligatoire
- **Fichier** : `src/ui/password_change.py`
- Forcé au 1er login si flag `must_change_password=1`
- Validations strictes :
  - Minimum 8 caractères
  - Au moins 1 majuscule
  - Au moins 1 minuscule
  - Au moins 1 chiffre
- Confirmation du MDP
- Réinitialisation du flag après changement

#### 4. Configuration Email (Optionnelle)
- **Fichier** : `src/database/email_config.py`
- Squelette pour intégration email automatique
- Support Gmail, SendGrid, SMTP personnalisé
- Instructions complètes pour activation future

### 🔄 Flux de Workflow

```
Nouvelle Demande
    ↓ (Access Request Page)
    └─→ Validation + Enregistrement BD
            ↓
         Status: PENDING
            ↓
    Admin Approbation
            ↓
         Création Compte + MDP Temporaire
    MDP Envoyé manuellement par Admin
            ↓
    1er Login avec MDP Temporaire
            ↓
    Changement MDP Obligatoire (Page)
            ↓
    Nouvel Utilisateur peut Accéder App
```

### 🔐 Modifications Sécurité

- ✅ Hachage MDP via `streamlit_authenticator.Hasher().hash()`
- ✅ Validation emails et identifiants côté client
- ✅ Mot de passe temporaire aléatoire
- ✅ Forçage changement MDP 1er login
- ✅ Contrôle d'accès admin (rôle requis)
- ✅ Requêtes SQL paramétrées (prévention injection)

### 📁 Fichiers Créés (8)

```
src/ui/access_request.py          (210 lignes)
src/ui/password_change.py         (115 lignes)
src/ui/admin.py                   (145 lignes)
src/database/email_config.py      (150 lignes)
tests/test_access_request.py      (200 lignes)
ACCES_REQUEST_FLOW.md             (200 lignes)
ADMIN_EMAIL_GUIDE.md              (200 lignes)
QUICK_START.md                    (150 lignes)
IMPLEMENTATION_SUMMARY.md         (150 lignes)
```

### 📋 Fichiers Modifiés (4)

#### src/app.py
```python
# Avant : Affichait juste login + lab
# Après  : Gère access_request + password_change entre login et lab
```

#### src/ui/login.py
```python
# Nouveau : get_credentials_from_db() - Lecture depuis BD
# Nouveau : Bouton "📝 Demande d'accès"
# Nouveau : Vérification flag must_change_password
# Avant : Credentials hardcodées
```

#### src/ui/lab.py
```python
# Nouveau : Onglet "👑 Administration" pour admins
# Nouveau : Affichage rôle utilisateur en sidebar
# Avant : Pas d'onglet admin
```

#### src/database/db_init.py
```python
# Fix : Hasher().hash('pwd') au lieu de Hasher(['pwd']).generate()[0]
# Table requests : Déjà présente, utilisée par accès
```

### 🧪 Tests

**9 Tests Unitaires Ajoutés** (tous PASS ✅)

```python
TestEmailValidation::test_valid_emails           ✅
TestEmailValidation::test_invalid_emails         ✅
TestUsernameValidation::test_valid_usernames     ✅
TestUsernameValidation::test_invalid_usernames   ✅
TestAccessRequest::test_submit_valid_request     ✅
TestAccessRequest::test_duplicate_username       ✅
TestAccessRequest::test_invalid_email            ✅
TestAccessRequest::test_invalid_username         ✅
TestAccessRequest::test_duplicate_pending_request✅
```

**Exécution :**
```bash
pytest tests/test_access_request.py -v
```

### 📚 Documentation

3 fichiers documentations complets :

1. **ACCES_REQUEST_FLOW.md** (200+ lignes)
   - Flux complet
   - Architecture BD
   - Schéma visual
   - Améliorations futures

2. **QUICK_START.md** (150+ lignes)
   - Résumé rapide
   - Test flow
   - Sécurité
   - Troubleshooting

3. **ADMIN_EMAIL_GUIDE.md** (200+ lignes)
   - Envoi manuel MDP
   - Configuration email (futures)
   - Options (Gmail, SendGrid, SMTP)
   - Checklist admin

### 🔧 Détails Techniques

**API Streamlit Utilisée :**
- `st.text_input()` - Formulaires
- `st.button()` - Actions
- `st.tabs()` - Navigation admin
- `st.session_state` - Persistance état
- `st.error/success/info/warning` - Messages

**Dépendances Existantes :**
- `streamlit` (1.52.2)
- `streamlit-authenticator` (0.4.2)
- `sqlite3` (natif Python)

**Dépendances Ajoutées :**
- `secrets` (natif Python) - Génération MDP temporaire

### ✅ Statut Déploiement

- [x] Code implémenté
- [x] Tests unitaires
- [x] Documentation complète
- [x] App testée localement
- [x] BD initialisée
- [x] Admin accessible
- [ ] Email automatique (optionnel, ready pour futur)
- [ ] Streamlit Cloud (prêt, en attente déploiement)

### 🚀 Pour Déployer

```bash
# Environnement local
cd jdr-manager
source venv/bin/activate
streamlit run src/app.py

# Streamlit Cloud
git push origin main
# Configurer sur cloud.streamlit.app
```

### 📝 Notes

- MDP temporaire format : 8 caractères alphanumériques + underscore
- Email sending : Manuel pour le moment (peut être automatisé via email_config.py)
- Rôle par défaut nouveau user : `joueur`
- Durée cookie session : 30 jours
- BD chemin : `jdr_data.db` (racine projet)

### 🔮 Améliorations Futures

- [ ] Intégration email automatique
- [ ] Expiration MDP temporaire (e.g., 24h)
- [ ] "J'ai oublié mon MDP"
- [ ] Historique demandes (UI)
- [ ] Envoi notification email admin
- [ ] Rate limiting demandes d'accès
- [ ] Confirmation email (double opt-in)
- [ ] Dashboard métriques admin

---

**Version**: 1.0  
**Date**: 2026-01-08  
**Auteur**: JDR Manager Team  
**Status**: ✅ PRÊT POUR PRODUCTION (sans email auto)
