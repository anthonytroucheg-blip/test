"""
Agent IA principal pour le suivi client du camping.
Utilise Claude via l'API Anthropic avec prompt caching pour répondre aux emails entrants.
"""

import logging
import os
from typing import Optional

import anthropic

from core.csv_loader import Reservation, trouver_client_par_email
from core.gmail_client import GmailClient, EmailRecu
from agent.prompts import (
    construire_prompt_systeme,
    construire_contexte_client,
    construire_contexte_inconnu,
)
from config.camping import CAMPING, MOTS_CLES_URGENCE

logger = logging.getLogger(__name__)

MODEL = "claude-opus-4-7"
MAX_TOKENS = 1024


def _contient_urgence(texte: str) -> bool:
    """Vérifie si le texte contient un mot-clé d'urgence."""
    texte_lower = texte.lower()
    return any(mot in texte_lower for mot in MOTS_CLES_URGENCE)


class AgentCamping:
    """
    Agent IA qui lit les emails entrants et génère des réponses personnalisées
    en utilisant le contexte de la réservation du client.
    """

    def __init__(self, gmail: GmailClient, reservations: list[Reservation]):
        self.gmail = gmail
        self.reservations = reservations
        self._client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        # Le prompt système est stable → mis en cache
        self._prompt_systeme = construire_prompt_systeme()

    def traiter_emails_entrants(self) -> int:
        """
        Lit les emails non lus, génère une réponse pour chacun et les envoie.
        Retourne le nombre de réponses envoyées.
        """
        emails = self.gmail.lire_emails_non_lus()
        nb_traites = 0

        for email_recu in emails:
            try:
                self._traiter_un_email(email_recu)
                self.gmail.marquer_comme_lu(email_recu.uid)
                nb_traites += 1
            except Exception as e:
                logger.error(f"Erreur traitement email de {email_recu.expediteur} : {e}")

        return nb_traites

    def _traiter_un_email(self, email_recu: EmailRecu) -> None:
        """Traite un seul email : trouve le client, génère et envoie la réponse."""
        expediteur = email_recu.expediteur
        logger.info(f"Traitement email de {expediteur} : {email_recu.sujet}")

        resa = trouver_client_par_email(self.reservations, expediteur)

        # Construction du contexte variable (non caché)
        if resa:
            contexte = construire_contexte_client(resa)
        else:
            contexte = construire_contexte_inconnu(expediteur)

        # Vérification urgence AVANT de passer par l'IA (optimisation)
        if _contient_urgence(email_recu.corps) or _contient_urgence(email_recu.sujet):
            logger.info(f"Urgence détectée pour {expediteur}, redirection accueil")
            reponse_html = self._reponse_urgence_html(resa)
            sujet_reponse = f"Re: {email_recu.sujet}"
            self.gmail.envoyer_email(
                destinataire=expediteur,
                sujet=sujet_reponse,
                corps_html=reponse_html,
                reply_to_message_id=email_recu.message_id,
            )
            return

        # Génération de la réponse via Claude
        reponse_texte = self._appeler_claude(contexte, email_recu.corps)

        if not reponse_texte:
            logger.warning(f"Réponse vide pour {expediteur}, email ignoré")
            return

        reponse_html = _texte_vers_html(reponse_texte, resa)
        sujet_reponse = f"Re: {email_recu.sujet}"

        self.gmail.envoyer_email(
            destinataire=expediteur,
            sujet=sujet_reponse,
            corps_html=reponse_html,
            corps_texte=reponse_texte,
            reply_to_message_id=email_recu.message_id,
        )

    def _appeler_claude(self, contexte_client: str, message_client: str) -> Optional[str]:
        """
        Appelle l'API Claude avec prompt caching sur le system prompt.
        - system prompt (stable, long) → mis en cache avec cache_control
        - contexte client + message → non caché (variable)
        """
        try:
            response = self._client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=[
                    {
                        "type": "text",
                        "text": self._prompt_systeme,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": f"{contexte_client}\n\n## Message du client\n\n{message_client}",
                    }
                ],
            )
            return response.content[0].text if response.content else None

        except anthropic.APIError as e:
            logger.error(f"Erreur API Claude : {e}")
            return None

    def _reponse_urgence_html(self, resa: Optional[Reservation]) -> str:
        """Génère une réponse HTML d'urgence redirigeant vers l'accueil physique."""
        from emails.templates import _enveloppe

        lang = resa.code_langue if resa else "fr"
        salutation = resa.salutation if resa else ""

        messages = {
            "en": (
                f"<p>Dear {salutation},</p>"
                f"<p>Thank you for your message. For any urgent matter, "
                f"please come directly to our reception desk, open from <strong>8:00 AM to 8:00 PM</strong>. "
                f"Our team will be delighted to assist you immediately.</p>"
                f"<p>Reception: {CAMPING['telephone']}</p>"
            ),
            "nl": (
                f"<p>Beste {salutation},</p>"
                f"<p>Voor dringende zaken verzoeken wij u om direct naar de receptie te komen, "
                f"open van <strong>8:00 tot 20:00</strong>. Ons team helpt u graag onmiddellijk.</p>"
                f"<p>Receptie: {CAMPING['telephone']}</p>"
            ),
            "de": (
                f"<p>Sehr geehrte/r {salutation},</p>"
                f"<p>Für dringende Angelegenheiten bitten wir Sie, direkt zur Rezeption zu kommen, "
                f"geöffnet von <strong>8:00 bis 20:00 Uhr</strong>. Unser Team hilft Ihnen sofort.</p>"
                f"<p>Rezeption: {CAMPING['telephone']}</p>"
            ),
            "es": (
                f"<p>Estimado/a {salutation},</p>"
                f"<p>Para cualquier asunto urgente, le rogamos que se dirija directamente a la recepción, "
                f"abierta de <strong>8:00 a 20:00</strong>. Nuestro equipo le atenderá inmediatamente.</p>"
                f"<p>Recepción: {CAMPING['telephone']}</p>"
            ),
            "fr": (
                f"<p>Bonjour {salutation},</p>"
                f"<p>{CAMPING['nom']} — {ACCUEIL_MESSAGE}</p>"
            ),
        }

        corps = messages.get(lang, messages["fr"])

        sous_titres = {
            "en": "We're here to help", "nl": "Wij zijn er voor u",
            "de": "Wir sind für Sie da", "es": "Estamos aquí para ayudarle",
        }
        sous_titre = sous_titres.get(lang, "Nous sommes là pour vous aider")
        return _enveloppe(sous_titre, corps)


# Import local pour éviter les imports circulaires
from config.camping import ACCUEIL
ACCUEIL_MESSAGE = ACCUEIL["message_urgence"]


def _texte_vers_html(texte: str, resa: Optional[Reservation]) -> str:
    """Convertit le texte plain de Claude en HTML enveloppé dans le template camping."""
    from emails.templates import _enveloppe

    # Conversion basique : sauts de ligne → paragraphes HTML
    paragraphes = texte.strip().split("\n\n")
    corps = "".join(f"<p>{p.replace(chr(10), '<br>')}</p>" for p in paragraphes if p.strip())

    lang = resa.code_langue if resa else "fr"
    sous_titres = {
        "en": "Your answer", "nl": "Uw antwoord",
        "de": "Ihre Antwort", "es": "Su respuesta",
    }
    sous_titre = sous_titres.get(lang, "Votre réponse")
    return _enveloppe(sous_titre, corps)
