# 📝 NOTE: Sauvegarde du Mot de Passe Temporaire

**Date**: 8 janvier 2026  
**Modification**: Sauvegarde du MDP temporaire en clair dans la base de données

## 🔄 Changement Apporté

### Avant
- Le mot de passe temporaire était généré et affiché une seule fois
- Si l'admin ne copiait pas immédiatement, il n'avait aucun moyen de le récupérer
- Impossible pour l'admin de voir les demandes approuvées avec leurs MDP

### Après
- ✅ Le MDP temporaire est **sauvegardé en clair** dans la colonne `temp_password` de la table `requests`
- ✅ L'admin peut **consulter le MDP à tout moment** après approbation
- ✅ Le MDP reste visible même après fermeture/rechargement de la page
- ✅ Code `temp_password` cliquable pour copier facilement

## 📊 Schéma Base de Données

### Table `requests` - Nouvelle Colonne

```sql
CREATE TABLE requests (
    username TEXT PRIMARY KEY,
    email TEXT,
    status TEXT DEFAULT 'PENDING',
    temp_password TEXT,              -- ← NOUVEAU
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🔐 Sécurité

⚠️ **Important** : Le mot de passe temporaire est stocké en **clair** pour permettre à l'admin de le consulter.

**Mitigations de sécurité** :
- ✅ Le MDP temporaire est **aléatoire** (8 caractères sûrs)
- ✅ L'utilisateur est **forcé de changer** ce MDP au 1er login
- ✅ Accès au panel admin **restreint** aux rôles admins
- ✅ Base de données locale (pas de serveur public)
- 📝 En production : Utiliser HTTPS + chiffrer la connexion à la BD

## 🔄 Fonctionnement

### Flux Utilisateur

1. **Admin demande accès** → Status: `PENDING`, temp_password: `NULL`
2. **Admin approuve** → Status: `APPROVED`, temp_password: `abc12xyz` (généré et sauvegardé)
3. **Admin peut consulter MDP** → Affiché dans le panel admin
4. **Admin envoie MDP** → Par email ou manuelle
5. **User login 1ère fois** → Forcé de changer le MDP
6. **Demande résolue** → Ancien MDP temporaire inutile

### Avantages

- ✅ Admin peut revérifier le MDP des demandes approuvées
- ✅ Admin peut envoyer le MDP multiple fois si l'user demande
- ✅ Traçabilité : Les demandes gardent le MDP généré
- ✅ Simplicité : Pas de système d'email complexe requis

## 📝 Modifications de Code

### admin.py
- `get_pending_requests()` → Retourne maintenant `temp_password`
- `approve_request()` → Sauvegarde le temp_password en clair
- `show_admin_requests_panel()` → Affiche le temp_password s'il existe

### db_init.py
- Table `requests` → Nouvelle colonne `temp_password TEXT`

## 🧪 Vérification

La base de données a été réinitialisée avec le nouveau schéma :

```
=== Schéma Table REQUESTS ===
  username             TEXT           
  email                TEXT           
  status               TEXT           
  temp_password        TEXT           
  request_date         TIMESTAMP      
```

## ⚡ Prochaines Étapes (Optionnel)

- [ ] Intégrer email automatique (prendra le MDP depuis `temp_password`)
- [ ] Ajouter "Renvoyer MDP" pour l'admin
- [ ] Logs d'accès (qui a consulté quel MDP)
- [ ] Expiration automatique du MDP temporaire (24h)
