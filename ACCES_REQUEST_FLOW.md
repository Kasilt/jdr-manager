# 📝 Système de Demande d'Accès - JDR Manager

## Fonctionnement

### 1. **Demande d'Accès (Nouvel Utilisateur)**

Les nouveaux utilisateurs qui n'ont pas encore de compte peuvent faire une demande d'accès :

1. Sur la page de login, cliquer sur le bouton **"📝 Demande d'accès"**
2. Remplir le formulaire :
   - **Identifiant** : Choisir un identifiant unique (3-20 caractères, lettres/chiffres/tiret bas)
   - **Email** : Entrer une adresse email valide
3. Cliquer sur **"📤 Envoyer ma demande"**
4. La demande est enregistrée dans la base de données et en attente de validation par l'administrateur

**Validations côté client :**
- L'identifiant doit contenir 3-20 caractères (lettres, chiffres, tiret bas uniquement)
- L'email doit être au format valide
- L'identifiant ne doit pas être déjà utilisé (ni dans `users` ni dans `requests`)
- Une seule demande en attente par email est autorisée

### 2. **Validation par l'Admin (Maître du Jeu)**

L'administrateur accède à l'onglet **"👑 Administration"** après connexion :

1. Voir la liste de toutes les demandes en attente
2. Pour chaque demande :
   - **Approuver** : Génère un mot de passe temporaire (8 caractères) et crée le compte utilisateur avec le flag `must_change_password = 1`
   - **Rejeter** : Change le statut de la demande à "REJECTED"
3. Copier le mot de passe temporaire généré
4. Envoyer manuellement le mot de passe à l'email du nouvel utilisateur (cette partie n'est pas automatisée)

**Données créées lors de l'approbation :**
- Compte utilisateur dans la table `users`
- Username, email, password_hash (temporaire)
- Rôle : `'joueur'` par défaut
- Flag `must_change_password = 1`
- Statut de la demande : `'APPROVED'`

### 3. **Premier Login & Changement de Mot de Passe Obligatoire**

Lors du premier login avec le mot de passe temporaire :

1. L'utilisateur se connecte avec son identifiant et le mot de passe temporaire
2. Un écran **"🔐 Changement de mot de passe obligatoire"** s'affiche
3. L'utilisateur doit entrer un nouveau mot de passe qui respecte :
   - Minimum 8 caractères
   - Au moins une majuscule
   - Au moins une minuscule
   - Au moins un chiffre
4. Confirmer le mot de passe
5. Cliquer sur **"🔐 Changer le mot de passe"**
6. Le flag `must_change_password` est mis à 0
7. L'utilisateur est redirigé vers l'application principale

### 4. **États des Demandes**

Les demandes d'accès peuvent avoir les statuts suivants :

| Statut | Signification |
|--------|---------------|
| `PENDING` | Demande en attente de validation |
| `APPROVED` | Demande approuvée, compte créé |
| `REJECTED` | Demande rejetée |

## Architecture Base de Données

### Table `requests`

```sql
CREATE TABLE requests (
    username TEXT PRIMARY KEY,
    email TEXT,
    status TEXT DEFAULT 'PENDING',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Table `users` (colonnes pertinentes)

```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password_hash TEXT,
    role TEXT DEFAULT 'joueur',
    must_change_password BOOLEAN DEFAULT 0
)
```

## Fichiers Concernés

### Nouveaux fichiers
- `src/ui/access_request.py` - Page de demande d'accès
- `src/ui/password_change.py` - Page de changement de mot de passe au premier login
- `src/ui/admin.py` - Panel d'administration pour les demandes

### Fichiers modifiés
- `src/app.py` - Intégration du flux de demande d'accès et changement de mot de passe
- `src/ui/login.py` - Lecture des credentials depuis la base de données, bouton "Demande d'accès"
- `src/ui/lab.py` - Affichage du panel admin pour les utilisateurs avec le rôle `admin`
- `src/database/db_init.py` - Correction de l'API Hasher

## Points Important à Noter

1. **Pas d'Email Automatique** : L'envoi du mot de passe temporaire doit se faire manuellement pour le moment
2. **Sécurité des Mots de Passe** : Les mots de passe sont hashés avec `streamlit-authenticator.Hasher`
3. **Rôle par Défaut** : Les nouveaux utilisateurs reçoivent le rôle `'joueur'` par défaut
4. **Admin Accès** : Seuls les utilisateurs avec le rôle `'admin'` voient l'onglet d'administration

## Flux Complet

```
Utilisateur Non Connecté
    ↓
Page de Login
    ├─ Option 1 : Login avec compte existant
    └─ Option 2 : Demande d'Accès (📝)
        ↓
    Page Demande d'Accès
        ├─ Saisir identifiant + email
        ├─ Validation client
        └─ Envoi à la DB (status PENDING)
        
Admin reçoit la demande
    ↓
Onglet Administration
    ├─ Approuver (génère mot de passe temporaire)
    │   ├─ Crée le compte utilisateur (must_change_password=1)
    │   └─ Envoie manuellement le mot de passe
    └─ Rejeter (status REJECTED)
        
Nouvel Utilisateur
    ↓
Login avec mot de passe temporaire
    ↓
Page Changement Mot de Passe Obligatoire
    ├─ Saisir nouveau mot de passe (validation exigences)
    ├─ Confirmation
    └─ Mise à jour DB (must_change_password=0)
        ↓
    Application Principale (Labo)
```

## Améliorations Futures

- [ ] Intégration d'un système d'email automatique (exemple: SendGrid, SMTP)
- [ ] Historique des demandes d'accès (approuvées/rejetées)
- [ ] Email de notification automatique à l'admin
- [ ] Expiration du mot de passe temporaire (x heures)
- [ ] Système de réinitialisation de mot de passe "J'ai oublié mon mot de passe"
