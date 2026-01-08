# 📧 Guide : Envoi des Mots de Passe Temporaires

## Situation Actuelle

L'envoi automatique d'emails n'est **pas activé** par défaut pour éviter les dépendances externes complexes.

L'administrateur doit donc envoyer manuellement les mots de passe temporaires par email.

## 🔄 Flux Actuel

### 1. Approval d'une Demande (Admin)

1. Admin accède à l'onglet "👑 Administration"
2. Clique sur "✅ Approuver" pour une demande
3. Un mot de passe temporaire est **généré automatiquement** et affiché à l'écran :

```
🔐 Mot de passe temporaire : a3K7_m2X
À envoyer à joueur@example.com
```

4. **Admin copie le mot de passe** et l'envoie manuellement par email

### 2. Email à Envoyer

L'admin doit envoyer un email au joueur avec ce contenu (exemple) :

---

**Sujet :** 🧙‍♂️ Accès JDR Manager - Mot de passe temporaire

**Corps :**

Bonjour [username],

Bienvenue sur JDR Manager ! 🎲

Votre demande d'accès a été approuvée. Voici vos identifiants de connexion temporaires :

📝 **Identifiant** : [username]  
🔐 **Mot de passe temporaire** : [COPIER ICI LE MOT DE PASSE]

**Accès** : http://localhost:8502 (ou l'URL de votre serveur)

⚠️ **Important** :
- Connectez-vous avec le mot de passe ci-dessus
- Vous devrez **obligatoirement changer ce mot de passe** lors de votre première connexion
- Votre nouveau mot de passe doit contenir :
  - Au minimum 8 caractères
  - Une majuscule, une minuscule et un chiffre

Bon jeu ! 🎉

---

## 🤖 Activation de l'Email Automatique (Futur)

Pour activer l'envoi automatique d'emails à l'avenir :

### Option 1 : Gmail (Recommandé pour Dev)

1. **Créer un "App Password" Gmail :**
   - Aller à https://myaccount.google.com/apppasswords
   - Sélectionner "Mail" et "Windows Computer"
   - Copier le mot de passe généré (16 caractères)

2. **Remplir `src/database/email_config.py` :**
   ```python
   EMAIL_CONFIG = {
       "enabled": True,  # Activer
       "sender_email": "votre.email@gmail.com",
       "sender_password": "[16-char app password]",
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
   }
   ```

3. **Décommenter la fonction** dans `src/database/email_config.py`

4. **Modifier `src/ui/admin.py`** pour appeler la fonction :
   ```python
   from database.email_config import send_temporary_password_email
   
   # Dans approve_request():
   success, message = send_temporary_password_email(email, username, temp_password)
   if success:
       st.success(message)
   else:
       st.warning(f"Email non envoyé : {message}")
   ```

### Option 2 : SendGrid

1. Créer un compte https://sendgrid.com
2. Générer une clé API
3. Installer `pip install sendgrid`
4. Adapter le code d'envoi dans `email_config.py`

### Option 3 : SMTP Personnalisé

- Office 365, Outlook, Zoho, etc.
- Configurer les paramètres SMTP dans `email_config.py`

## 📋 Checklist pour Admin

Pour chaque approbation :

- [ ] Cliquer "✅ Approuver"
- [ ] Copier le mot de passe affiché
- [ ] Ouvrir son client email
- [ ] Envoyer le template ci-dessus avec :
  - [ ] [username] remplacé
  - [ ] [COPIER ICI LE MOT DE PASSE] remplacé
- [ ] Confirmer à l'utilisateur qu'il peut se connecter

## 🔒 Sécurité

- ✅ Les mots de passe temporaires sont **aléatoires** (8 caractères alphanumériques)
- ✅ Ils sont **hashés** dans la base de données
- ✅ Forçage du changement au **premier login**
- ⚠️ **HTTPS recommandé** en production pour le partage des mots de passe

## 📞 Troubleshooting

| Problème | Solution |
|----------|----------|
| Email n'arrive pas | Vérifier l'adresse email / Vérifier le spam |
| L'utilisateur ne peut pas se connecter | Vérifier que le mot de passe temporaire est exact |
| Nouveau mot de passe rejeté | Vérifier les exigences : 8+ chars, majuscule, minuscule, chiffre |

## 📌 Notes

- Les mots de passe temporaires ne **n'expirent pas** (à améliorer)
- Un utilisateur peut demander son mot de passe plusieurs fois si oublié (système futur)
- L'email est le **seul moyen** pour le nouvel utilisateur de recevoir ses credentials
