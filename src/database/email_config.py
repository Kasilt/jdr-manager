"""Email configuration and utilities for sending temporary passwords.

NOTE: Email sending is currently disabled and must be sent manually by admin.
To enable automatic email sending, configure the settings below and implement the send_email function.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Tuple

# ============================================================================
# EMAIL CONFIGURATION
# ============================================================================
# To enable email sending, fill in these settings and uncomment the send_email function

EMAIL_CONFIG = {
    "enabled": False,  # Set to True to enable email sending
    "sender_email": "admin@jdr-manager.com",  # Your email address
    "sender_password": "",  # Your email password or app-specific password
    "smtp_server": "smtp.gmail.com",  # Gmail: smtp.gmail.com
    "smtp_port": 587,  # Gmail: 587
}

# ============================================================================
# EMAIL TEMPLATE
# ============================================================================

def get_access_granted_email(username: str, temp_password: str) -> Tuple[str, str]:
    """Generate email subject and body for access granted notification.
    
    Args:
        username: The username of the new player
        temp_password: The temporary password
    
    Returns:
        tuple: (subject, body)
    """
    subject = "🧙‍♂️ Accès JDR Manager - Mot de passe temporaire"
    
    body = f"""Bonjour {username},

Bienvenue sur JDR Manager ! 🎲

Votre demande d'accès a été approuvée. Voici vos identifiants de connexion temporaires :

📝 **Identifiant** : {username}
🔐 **Mot de passe temporaire** : {temp_password}

**Accès** : http://your-jdr-manager-url/

⚠️ **Important** :
- Connectez-vous avec le mot de passe ci-dessus
- Vous devrez obligatoirement changer ce mot de passe lors de votre première connexion
- Votre nouveau mot de passe doit contenir :
  - Au minimum 8 caractères
  - Une majuscule, une minuscule et un chiffre

Bon jeu ! 🎉

---
JDR Manager Admin
"""
    
    return subject, body


# ============================================================================
# FUNCTIONS (Currently Disabled)
# ============================================================================

def send_temporary_password_email(email: str, username: str, temp_password: str) -> Tuple[bool, str]:
    """Send temporary password email to new user.
    
    Args:
        email: Recipient email address
        username: The username
        temp_password: The temporary password
    
    Returns:
        tuple: (success: bool, message: str)
    
    NOTE: Currently not implemented. Manual sending required.
    To enable:
    1. Fill in EMAIL_CONFIG settings above
    2. Uncomment the code below
    3. Set EMAIL_CONFIG["enabled"] = True
    4. Import and call this function from admin.py
    """
    if not EMAIL_CONFIG["enabled"]:
        return False, "Email sending is disabled. Manual sending required."
    
    # Uncomment below to enable automatic sending:
    """
    try:
        subject, body = get_access_granted_email(username, temp_password)
        
        # Create message
        message = MIMEMultipart()
        message["From"] = EMAIL_CONFIG["sender_email"]
        message["To"] = email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "plain", "utf-8"))
        
        # Send email
        server = smtplib.SMTP(EMAIL_CONFIG["smtp_server"], EMAIL_CONFIG["smtp_port"])
        server.starttls()
        server.login(EMAIL_CONFIG["sender_email"], EMAIL_CONFIG["sender_password"])
        server.send_message(message)
        server.quit()
        
        return True, f"Email envoyé à {email}"
    
    except smtplib.SMTPAuthenticationError:
        return False, "Erreur d'authentification SMTP. Vérifier les identifiants email."
    except smtplib.SMTPException as e:
        return False, f"Erreur SMTP : {str(e)}"
    except Exception as e:
        return False, f"Erreur d'envoi d'email : {str(e)}"
    """
    return False, "Email sending not configured"


# ============================================================================
# SETUP INSTRUCTIONS
# ============================================================================
"""
To enable automatic email sending:

1. Choose an email provider:
   - Gmail : https://myaccount.google.com/apppasswords
   - SendGrid: https://app.sendgrid.com/
   - Custom SMTP server

2. For Gmail:
   a. Enable 2-factor authentication
   b. Create an "App Password" (not your regular password)
   c. Fill in EMAIL_CONFIG:
      - sender_email: your.email@gmail.com
      - sender_password: [16-char app password from step 2b]
      - smtp_server: smtp.gmail.com
      - smtp_port: 587

3. For Custom SMTP:
   a. Get SMTP server and port from your email provider
   b. Update EMAIL_CONFIG accordingly

4. Enable the send_temporary_password_email function:
   a. Uncomment the code in the function
   b. Set EMAIL_CONFIG["enabled"] = True

5. In admin.py, import and call send_temporary_password_email():
   from database.email_config import send_temporary_password_email
   
   success, message = send_temporary_password_email(email, username, temp_password)
   if success:
       st.success(message)
   else:
       st.warning(message + " - Please send manually.")

6. Test by submitting an access request and approving it
"""
