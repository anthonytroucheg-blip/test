"""
Point d'entrée principal de l'agent IA camping.

Usage :
  python main.py emails       # Traite les emails entrants (réponse aux clients)
  python main.py scheduler    # Envoie les emails automatiques du jour (J-7, J-1, etc.)
  python main.py rapport      # Envoie le rapport hebdomadaire au gérant
  python main.py all          # Exécute scheduler + emails (mode cron recommandé)
"""

import argparse
import logging
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join("logs", "agent.log"), encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def _verifier_env() -> None:
    """Vérifie que toutes les variables d'environnement nécessaires sont présentes."""
    obligatoires = ["GMAIL_ADDRESS", "GMAIL_APP_PASSWORD", "ANTHROPIC_API_KEY", "ZIP_BACKUP_PATH"]
    manquantes = [v for v in obligatoires if not os.environ.get(v)]
    if manquantes:
        logger.error(f"Variables d'environnement manquantes : {', '.join(manquantes)}")
        logger.error("Copiez .env.example vers .env et remplissez les valeurs.")
        sys.exit(1)


def cmd_emails(zip_path: str) -> None:
    """Lit les emails entrants et envoie des réponses IA."""
    from core.csv_loader import charger_reservations
    from core.gmail_client import creer_client_gmail_depuis_env
    from agent.agent import AgentCamping

    gmail = creer_client_gmail_depuis_env()
    reservations = charger_reservations(zip_path)
    agent = AgentCamping(gmail=gmail, reservations=reservations)
    nb = agent.traiter_emails_entrants()
    logger.info(f"Emails entrants traités : {nb}")


def cmd_scheduler(zip_path: str) -> None:
    """Envoie les emails automatiques du jour."""
    from core.gmail_client import creer_client_gmail_depuis_env
    from emails.scheduler import envoyer_emails_du_jour

    gmail = creer_client_gmail_depuis_env()
    compteurs = envoyer_emails_du_jour(zip_path=zip_path, gmail=gmail)
    for etape, nb in compteurs.items():
        if nb > 0:
            logger.info(f"  {etape}: {nb} email(s) envoyé(s)")


def cmd_rapport(zip_path: str) -> None:
    """Envoie le rapport hebdomadaire au gérant."""
    from core.gmail_client import creer_client_gmail_depuis_env
    from emails.scheduler import envoyer_rapport_hebdomadaire

    email_gerant = os.environ.get("EMAIL_GERANT", "")
    if not email_gerant:
        logger.error("Variable EMAIL_GERANT manquante dans .env")
        sys.exit(1)

    gmail = creer_client_gmail_depuis_env()
    succes = envoyer_rapport_hebdomadaire(
        zip_path=zip_path, gmail=gmail, email_gerant=email_gerant
    )
    if succes:
        logger.info(f"Rapport hebdomadaire envoyé à {email_gerant}")
    else:
        logger.error("Échec de l'envoi du rapport")


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent IA Camping – Suivi client automatisé")
    parser.add_argument(
        "commande",
        choices=["emails", "scheduler", "rapport", "all"],
        help="Commande à exécuter",
    )
    args = parser.parse_args()

    _verifier_env()

    zip_path = os.environ["ZIP_BACKUP_PATH"]
    if not os.path.exists(zip_path):
        logger.error(f"Fichier de sauvegarde ZIP introuvable : {zip_path}")
        sys.exit(1)

    if args.commande == "emails":
        cmd_emails(zip_path)
    elif args.commande == "scheduler":
        cmd_scheduler(zip_path)
    elif args.commande == "rapport":
        cmd_rapport(zip_path)
    elif args.commande == "all":
        cmd_scheduler(zip_path)
        cmd_emails(zip_path)


if __name__ == "__main__":
    main()
