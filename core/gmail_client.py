"""
Client Gmail pour l'agent IA : lecture IMAP et envoi SMTP.
Gère la connexion à la boîte dédiée du camping et l'envoi d'emails HTML.
"""

import imaplib
import smtplib
import email
import logging
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

GMAIL_IMAP_HOST = "imap.gmail.com"
GMAIL_IMAP_PORT = 993
GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587


@dataclass
class EmailRecu:
    uid: str
    expediteur: str
    sujet: str
    corps: str
    date_reception: datetime
    message_id: str


def _decoder_entete(valeur: str) -> str:
    """Décode un en-tête email encodé (RFC 2047)."""
    parties = decode_header(valeur)
    resultat = []
    for contenu, encodage in parties:
        if isinstance(contenu, bytes):
            resultat.append(contenu.decode(encodage or "utf-8", errors="replace"))
        else:
            resultat.append(contenu)
    return "".join(resultat)


def _extraire_corps(msg: email.message.Message) -> str:
    """Extrait le corps texte d'un email (préfère plain text)."""
    corps_plain = ""
    corps_html = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            payload = part.get_payload(decode=True)
            if payload is None:
                continue
            charset = part.get_content_charset() or "utf-8"
            texte = payload.decode(charset, errors="replace")
            if content_type == "text/plain":
                corps_plain = texte
            elif content_type == "text/html":
                corps_html = texte
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            texte = payload.decode(charset, errors="replace")
            if msg.get_content_type() == "text/html":
                corps_html = texte
            else:
                corps_plain = texte

    return corps_plain or corps_html


class GmailClient:
    """
    Client Gmail utilisant IMAP (lecture) et SMTP (envoi).
    Nécessite un mot de passe d'application Gmail (2FA activé).
    """

    def __init__(self, adresse: str, mot_de_passe_app: str):
        self.adresse = adresse
        self._mot_de_passe = mot_de_passe_app

    def lire_emails_non_lus(self, dossier: str = "INBOX") -> list[EmailRecu]:
        """Récupère tous les emails non lus de la boîte de réception."""
        emails = []
        try:
            with imaplib.IMAP4_SSL(GMAIL_IMAP_HOST, GMAIL_IMAP_PORT) as imap:
                imap.login(self.adresse, self._mot_de_passe)
                imap.select(dossier)

                _, uids = imap.search(None, "UNSEEN")
                uid_list = uids[0].split()

                for uid in uid_list:
                    _, data = imap.fetch(uid, "(RFC822)")
                    if not data or not data[0]:
                        continue
                    raw = data[0][1]
                    msg = email.message_from_bytes(raw)

                    expediteur_brut = msg.get("From", "")
                    # Extrait uniquement l'adresse email
                    expediteur = email.utils.parseaddr(expediteur_brut)[1].lower()

                    sujet = _decoder_entete(msg.get("Subject", ""))
                    corps = _extraire_corps(msg)
                    message_id = msg.get("Message-ID", "")

                    date_str = msg.get("Date", "")
                    try:
                        date_reception = email.utils.parsedate_to_datetime(date_str)
                    except Exception:
                        date_reception = datetime.now()

                    emails.append(EmailRecu(
                        uid=uid.decode(),
                        expediteur=expediteur,
                        sujet=sujet,
                        corps=corps,
                        date_reception=date_reception,
                        message_id=message_id,
                    ))

                logger.info(f"{len(emails)} email(s) non lu(s) récupéré(s)")

        except imaplib.IMAP4.error as e:
            logger.error(f"Erreur IMAP : {e}")
            raise

        return emails

    def marquer_comme_lu(self, uid: str, dossier: str = "INBOX") -> None:
        """Marque un email comme lu par son UID."""
        try:
            with imaplib.IMAP4_SSL(GMAIL_IMAP_HOST, GMAIL_IMAP_PORT) as imap:
                imap.login(self.adresse, self._mot_de_passe)
                imap.select(dossier)
                imap.store(uid, "+FLAGS", "\\Seen")
        except imaplib.IMAP4.error as e:
            logger.error(f"Erreur marquage lu (UID {uid}) : {e}")

    def envoyer_email(
        self,
        destinataire: str,
        sujet: str,
        corps_html: str,
        corps_texte: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
    ) -> bool:
        """
        Envoie un email HTML via SMTP.
        Retourne True si l'envoi réussit, False sinon.
        """
        msg = MIMEMultipart("alternative")
        msg["From"] = self.adresse
        msg["To"] = destinataire
        msg["Subject"] = sujet
        msg["Date"] = email.utils.formatdate(localtime=True)

        if reply_to_message_id:
            msg["In-Reply-To"] = reply_to_message_id
            msg["References"] = reply_to_message_id

        if corps_texte:
            msg.attach(MIMEText(corps_texte, "plain", "utf-8"))
        msg.attach(MIMEText(corps_html, "html", "utf-8"))

        try:
            with smtplib.SMTP(GMAIL_SMTP_HOST, GMAIL_SMTP_PORT) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(self.adresse, self._mot_de_passe)
                smtp.sendmail(self.adresse, destinataire, msg.as_string())
            logger.info(f"Email envoyé à {destinataire} : {sujet}")
            return True

        except smtplib.SMTPException as e:
            logger.error(f"Erreur SMTP lors de l'envoi à {destinataire} : {e}")
            return False


def creer_client_gmail_depuis_env() -> GmailClient:
    """Crée un GmailClient à partir des variables d'environnement."""
    adresse = os.environ.get("GMAIL_ADDRESS", "")
    mot_de_passe = os.environ.get("GMAIL_APP_PASSWORD", "")
    if not adresse or not mot_de_passe:
        raise EnvironmentError(
            "Variables d'environnement manquantes : GMAIL_ADDRESS et GMAIL_APP_PASSWORD"
        )
    return GmailClient(adresse=adresse, mot_de_passe_app=mot_de_passe)
