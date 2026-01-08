# 🚀 Guide Rapide : Système de Demande d'Accès

## 📋 Résumé

Un système complet de gestion des demandes d'accès a été implémenté avec les étapes suivantes :

### 1. **Demande d'Accès (Nouvel Utilisateur)**
- Cliquer sur "📝 Demande d'accès" depuis la page de login
- Entrer un identifiant unique et une adresse email
- La demande est enregistrée dans la base de données

### 2. **Validation par Admin**
- L'admin se connecte et accède à l'onglet "👑 Administration"
- Valide ou rejette les demandes en attente
- Un mot de passe temporaire est généré automatiquement
- L'admin doit envoyer manuellement le mot de passe par email

### 3. **Premier Login - Changement de Mot de Passe Obligatoire**
- Le nouvel utilisateur se connecte avec le mot de passe temporaire
- Un écran force le changement de mot de passe
- Les exigences : 8+ caractères, majuscule, minuscule, chiffre
- Après validation, accès à l'application principale

## 📁 Fichiers Créés/Modifiés

### ✨ Nouveaux fichiers
| Fichier | Description |
|---------|-------------|
| `src/ui/access_request.py` | Page de demande d'accès |
| `src/ui/password_change.py` | Changement de mot de passe au 1er login |
| `src/ui/admin.py` | Panel d'administration pour valider les demandes |
| `tests/test_access_request.py` | Tests unitaires |
| `ACCES_REQUEST_FLOW.md` | Documentation complète du flux |

### 🔧 Fichiers modifiés
| Fichier | Modifications |
|---------|--------------|
| `src/app.py` | Ajout du flux demande d'accès et changement MDP |
| `src/ui/login.py` | Lecture BD pour credentials, bouton "Demande d'accès", vérification `must_change_password` |
| `src/ui/lab.py` | Onglet "👑 Administration" pour les admins |
| `src/database/db_init.py` | Correction API Hasher |

## 🗄️ Schéma Base de Données

### Table `requests` (existante, utilisée par le flux)
```sql
CREATE TABLE requests (
    username TEXT PRIMARY KEY,
    email TEXT,
    status TEXT DEFAULT 'PENDING',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Champs `users` utilisés
```sql
ALTER TABLE users ADD COLUMN must_change_password BOOLEAN DEFAULT 0;
```

## 🧪 Test Rapide

### Comptes de Test
- **Admin** : `admin` / `admin123` (créé par défaut)
- **Nouveaux** : Via demande d'accès

### Flux de Test
1. Ouvrir http://localhost:8502
2. Cliquer "📝 Demande d'accès"
3. Entrer : `testuser` / `test@example.com`
4. Se connecter avec `admin` / `admin123`
5. Aller à l'onglet "👑 Administration"
6. Approuver la demande (copier le mot de passe temporaire)
7. Se déconnecter
8. Login avec `testuser` / [mot de passe temporaire]
9. Changer le mot de passe (8+ caractères, majuscule, minuscule, chiffre)

## 🔐 Sécurité

✅ **Implémenté :**
- Hachage des mots de passe via `streamlit_authenticator.Hasher`
- Validation des emails et identifiants côté client
- Mot de passe temporaire aléatoire (8 caractères alphanumériques)
- Forçage du changement de mot de passe au premier login
- Contrôle d'accès au panel admin (rôle `admin` requis)

⚠️ **À Améliorer (Futur) :**
- Intégrer un service d'email automatique (SendGrid, SMTP)
- Ajouter une expiration du mot de passe temporaire
- Système "J'ai oublié mon mot de passe"
- Historique des demandes

## 📋 Validation des Données

### Identifiant
- 3-20 caractères
- Lettres, chiffres, tiret bas uniquement
- Unique (pas dans `users` ni `requests`)

### Email
- Format valide (`user@domain.com`)
- Une seule demande en attente par email

### Mot de Passe (Au changement)
- Minimum 8 caractères
- Au moins 1 majuscule, 1 minuscule, 1 chiffre
- Confirmation identique

## 🎯 Points Clés à Retenir

1. **Pas d'Email Auto** : Les mots de passe temporaires doivent être envoyés manuellement
2. **Rôle par Défaut** : Les nouveaux utilisateurs reçoivent le rôle `joueur`
3. **Flag `must_change_password`** : Forcé lors du 1er login, puis réinitialisé
4. **Statut des Demandes** : `PENDING` → `APPROVED`/`REJECTED`
5. **Lecture DB à Chaque Login** : Les credentials sont lus depuis la BD (pas de hardcode)

## ✅ Prêt pour Production ?

- ✅ Fonctionnalité complète
- ✅ Validations côté client
- ✅ Sécurité de base (hachage, contrôle d'accès)
- ⚠️ À faire : Email automatique, interface manuelle pour l'admin

## 📞 Besoin d'Aide ?

Consulter `ACCES_REQUEST_FLOW.md` pour la documentation complète.
