# 🔧 Guide de Dépannage - Système d'Accès JDR Manager

Si vous rencontrez un problème, trouvez-le dans cette liste et suivez la solution.

---

## ❌ L'Application Ne Démarre Pas

### Symptôme: `streamlit: command not found`

**Cause**: Environnement virtuel non activé

**Solution**:
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Puis lancer l'app
streamlit run src/app.py
```

---

### Symptôme: `ModuleNotFoundError: No module named 'streamlit'`

**Cause**: Dépendances non installées

**Solution**:
```bash
# Installer les dépendances
source venv/bin/activate
pip install -r requirements.txt
```

---

### Symptôme: Port 8502 déjà utilisé

**Cause**: Une autre instance de Streamlit tourne

**Solution**:
```bash
# Lancer sur un autre port
streamlit run src/app.py --server.port 8503

# Ou tuer le processus existant
lsof -ti:8502 | xargs kill -9
```

---

## ❌ Erreurs à la Base de Données

### Symptôme: `sqlite3.OperationalError: database is locked`

**Cause**: BD en cours d'utilisation par un autre processus

**Solution**:
```bash
# Attendre quelques secondes puis relancer
# Ou supprimer et réinitialiser la BD
rm -f jdr_data.db
python src/database/db_init.py
```

---

### Symptôme: `FileNotFoundError: jdr_data.db`

**Cause**: BD non initialisée

**Solution**:
```bash
# Initialiser la BD
python src/database/db_init.py
```

---

## ❌ Problèmes de Login

### Symptôme: Admin login ne fonctionne pas (`admin` / `admin123`)

**Cause**: BD pas initialisée ou compte admin supprimé

**Solution**:
```bash
# Réinitialiser la BD
rm -f jdr_data.db
python src/database/db_init.py

# Relancer l'app
streamlit run src/app.py
```

---

### Symptôme: Cannot select user after login (page blanche)

**Cause**: Erreur de session Streamlit

**Solution**:
1. Fermer le navigateur complètement
2. Relancer l'app
3. Vider le cache du navigateur (Ctrl+Shift+Delete)
4. Réessayer

---

## ❌ Problèmes de Demande d'Accès

### Symptôme: Bouton "Demande d'accès" ne répond pas

**Cause**: Erreur de rendu Streamlit

**Solution**:
1. Rafraîchir la page (F5)
2. Vider le cache du navigateur
3. Redémarrer Streamlit

---

### Symptôme: "Cet identifiant est déjà pris" alors que c'est nouveau

**Cause**: Demande précédente en attente

**Solution**:
- Un identifiant ne peut être utilisé qu'une fois (déjà pris)
- Choisir un identifiant différent
- Ou admin doit approuver/rejeter la demande existante

---

### Symptôme: "Une demande d'accès est déjà en cours pour cet email"

**Cause**: Email a déjà soumis une demande en attente

**Solution**:
- Attendre que l'admin approuve/rejette la demande existante
- Ou utiliser un email différent

---

### Symptôme: Validation email accepte un email invalide

**Cause**: Validation simplifiée (regex basique)

**Solution**:
- C'est normal, validation basique
- Email doit contenir @ et un domaine
- Si besoin de validation plus stricte, contacter dev

---

## ❌ Problèmes de Changement de Mot de Passe

### Symptôme: Page changement MDP n'apparaît pas au 1er login

**Cause**: Flag `must_change_password` pas activé

**Solution**:
```sql
-- Vérifier en SQL
SELECT username, must_change_password FROM users WHERE username='votre_user';

-- Si 0, mettre à 1
UPDATE users SET must_change_password = 1 WHERE username = 'votre_user';
```

---

### Symptôme: "Le mot de passe doit contenir des majuscules, minuscules et chiffres"

**Cause**: Mot de passe ne respecte pas les exigences

**Exigences**:
- ✅ Au minimum **8 caractères**
- ✅ Au moins **1 majuscule** (A-Z)
- ✅ Au moins **1 minuscule** (a-z)
- ✅ Au moins **1 chiffre** (0-9)

**Exemple valide**: `Motdepasse123`

---

### Symptôme: "Les mots de passe ne correspondent pas"

**Cause**: Les 2 champs ne sont pas identiques

**Solution**:
- Vérifier la saisie (pas d'espace/caractère en trop)
- Retaper les deux mots de passe

---

## ❌ Problèmes Admin

### Symptôme: Onglet "Administration" n'apparaît pas

**Cause**: Utilisateur n'a pas le rôle `admin`

**Solution**:
1. Vérifier en BD que l'utilisateur a `role = 'admin'`
2. Ou se connecter avec le compte `admin` (défaut)

```sql
-- Vérifier le rôle
SELECT username, role FROM users WHERE username = 'votre_user';

-- Changer en admin si nécessaire
UPDATE users SET role = 'admin' WHERE username = 'votre_user';
```

---

### Symptôme: Demandes en attente ne s'affichent pas

**Cause**: Pas de demandes en attente

**Solution**:
- C'est normal, attendre des demandes
- Tester en soumettant une demande d'accès

---

### Symptôme: Bouton "Approuver" ne génère pas de MDP

**Cause**: Erreur lors de la création compte

**Solution**:
- Vérifier les logs Streamlit (terminal)
- Vérifier que l'identifiant n'existe pas en BD
- Réessayer

---

### Symptôme: Le MDP temporaire généré est trop court/long

**Cause**: Fonction de génération modifiée

**Solution**: C'est un bug - contacter dev

---

## ❌ Problèmes Tests

### Symptôme: Tests échouent (`pytest fails`)

**Cause**: Environnement pas configuré

**Solution**:
```bash
# Installer pytest
pip install pytest

# Réinitialiser BD
rm -f jdr_data.db jdr_test.db
python src/database/db_init.py

# Relancer tests
pytest tests/test_access_request.py -v
```

---

### Symptôme: `ImportError` dans les tests

**Cause**: Chemin Python incorrecte

**Solution**:
```bash
# S'assurer de lancer depuis la racine du projet
cd /home/sebastien/Developpement/jdr-manager
pytest tests/test_access_request.py -v
```

---

## ❌ Problèmes de Navigateur

### Symptôme: Page charge longtemps

**Cause**: Streamlit recharge

**Solution**:
- Normal, Streamlit peut être lent au redémarrage
- Attendre 5-10 secondes
- Refresh la page

---

### Symptôme: Les changements de code n'apparaissent pas

**Cause**: Cache Streamlit

**Solution**:
1. Cliquer "Always rerun" dans Streamlit
2. Ou dans le terminal Streamlit, appuyer sur `R`
3. Ou redémarrer l'app complètement

---

## ✅ Vérifications de Santé

### Vérifier que tout fonctionne

```bash
# 1. Compilation sans erreur
python -m py_compile src/app.py src/ui/*.py

# 2. Tests passent
pytest tests/test_access_request.py -v

# 3. BD existe
ls -la jdr_data.db

# 4. BD a les tables
sqlite3 jdr_data.db ".tables"

# 5. Admin existe
sqlite3 jdr_data.db "SELECT * FROM users WHERE username='admin';"

# 6. App démarre
streamlit run src/app.py
```

Si tout ✅, tout va bien !

---

## 📚 Où Chercher de l'Aide

| Problème | Doc à Lire |
|----------|-----------|
| Démarrage | QUICK_START.md |
| Flux utilisateur | ACCES_REQUEST_FLOW.md |
| Admin/Email | ADMIN_EMAIL_GUIDE.md |
| Technique | IMPLEMENTATION_SUMMARY.md |
| Architecture | README_ACCESS_SYSTEM.md |

---

## 🆘 Dernier Recours

Si rien ne marche :

```bash
# 1. Réinitialiser complètement
rm -rf venv jdr_data.db jdr_test.db .pytest_cache

# 2. Recréer l'env
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Réinitialiser BD
python src/database/db_init.py

# 4. Relancer
streamlit run src/app.py
```

---

## 💬 Logs Utiles à Vérifier

### Terminal Streamlit
```bash
# Affiche les erreurs en temps réel
# Vérifier les lignes avec "ERROR" ou "Traceback"
```

### Console du Navigateur
```javascript
// F12 → Console
// Vérifier les erreurs JavaScript
```

### BD SQLite
```bash
# Vérifier l'état de la BD
sqlite3 jdr_data.db ".schema"
sqlite3 jdr_data.db "SELECT COUNT(*) FROM requests;"
```

---

## 📞 Reporting un Bug

Si vous trouvez un bug :

1. Reproduire le problème
2. Noter les étapes exactes
3. Vérifier le troubleshooting ci-dessus
4. Vérifier les logs (terminal + navigateur)
5. Signaler avec : logs + étapes + navigateur + OS

---

## ✅ Checklist de Dépannage

- [ ] App s'est correctement lancée ?
- [ ] Environnement virtuel activé ?
- [ ] Dépendances installées ? (`pip list`)
- [ ] BD existe et contient admin ? (`sqlite3 jdr_data.db`)
- [ ] Pas d'erreurs dans le terminal ?
- [ ] Pas d'erreurs dans la console navigateur ? (F12)
- [ ] Cache navigateur vide ? (Ctrl+Shift+Delete)
- [ ] Autre instance de Streamlit tournant ?
- [ ] Port 8502 disponible ?

---

**Version du Guide**: 1.0  
**Date**: 8 janvier 2026  
**Status**: ✅ Prêt à aider
