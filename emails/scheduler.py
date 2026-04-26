"""
Planificateur d'emails automatiques.
À lancer chaque matin (cron ou tâche planifiée) pour envoyer les emails du jour.
"""

import logging
import os
from datetime import date

from core.csv_loader import charger_reservations, grouper_par_etape, Reservation
from core.gmail_client import GmailClient
from emails.templates import generer_email_pour_etape
from config.camping import CAMPING

logger = logging.getLogger(__name__)

# Étapes qui déclenchent un envoi automatique
ETAPES_AUTO = ["j_moins_7", "j_moins_1", "jour_arrivee", "j_plus_2", "annulation"]


def envoyer_emails_du_jour(zip_path: str, gmail: GmailClient) -> dict[str, int]:
    """
    Charge le fichier de sauvegarde, détecte les réservations concernées aujourd'hui
    et envoie les emails automatiques correspondants.

    Retourne un dict {etape: nb_envois} pour le rapport.
    """
    reservations = charger_reservations(zip_path)
    groupes = grouper_par_etape(reservations)
    compteurs: dict[str, int] = {etape: 0 for etape in ETAPES_AUTO}

    for etape in ETAPES_AUTO:
        liste = groupes.get(etape, [])
        for resa in liste:
            resultat = generer_email_pour_etape(resa, etape)
            if resultat is None:
                continue
            sujet, corps_html = resultat
            succes = gmail.envoyer_email(
                destinataire=resa.email,
                sujet=sujet,
                corps_html=corps_html,
            )
            if succes:
                compteurs[etape] += 1
                logger.info(f"[{etape}] Email envoyé à {resa.email} ({resa.nom_complet})")
            else:
                logger.error(f"[{etape}] Échec envoi à {resa.email}")

    total = sum(compteurs.values())
    logger.info(f"Planificateur terminé : {total} email(s) envoyé(s) au total")
    return compteurs


def generer_rapport_hebdomadaire(zip_path: str) -> str:
    """
    Génère un rapport texte hebdomadaire à destination du gérant du camping.
    Retourne le corps HTML du rapport.
    """
    reservations = charger_reservations(zip_path)
    aujourd_hui = date.today()

    actives = [r for r in reservations if not r.est_annulation]
    annulations = [r for r in reservations if r.est_annulation]
    en_cours = [r for r in actives if r.date_arrivee <= aujourd_hui <= r.date_depart]
    prochaines_30j = [
        r for r in actives
        if 0 < (r.date_arrivee - aujourd_hui).days <= 30
    ]

    pays_stats: dict[str, int] = {}
    for r in actives:
        pays_stats[r.pays or "Inconnu"] = pays_stats.get(r.pays or "Inconnu", 0) + 1
    top_pays = sorted(pays_stats.items(), key=lambda x: x[1], reverse=True)[:5]

    lignes_pays = "".join(
        f"<tr><td>{pays}</td><td>{nb}</td></tr>" for pays, nb in top_pays
    )

    rapport_html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; color: #333;">
      <div style="background-color: #1a237e; padding: 20px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 20px;">Rapport hebdomadaire – Agent IA</h1>
        <p style="color: #c5cae9; margin: 4px 0 0;">{CAMPING['nom']} · {aujourd_hui.strftime('%d/%m/%Y')}</p>
      </div>
      <div style="padding: 30px 24px;">
        <h2>Résumé de la semaine</h2>
        <table style="width:100%; border-collapse:collapse;">
          <tr style="background:#e8eaf6;">
            <td style="padding:8px; border:1px solid #ddd;"><strong>Séjours en cours aujourd'hui</strong></td>
            <td style="padding:8px; border:1px solid #ddd;">{len(en_cours)}</td>
          </tr>
          <tr>
            <td style="padding:8px; border:1px solid #ddd;"><strong>Arrivées dans les 30 prochains jours</strong></td>
            <td style="padding:8px; border:1px solid #ddd;">{len(prochaines_30j)}</td>
          </tr>
          <tr style="background:#e8eaf6;">
            <td style="padding:8px; border:1px solid #ddd;"><strong>Total réservations actives (fichier)</strong></td>
            <td style="padding:8px; border:1px solid #ddd;">{len(actives)}</td>
          </tr>
          <tr>
            <td style="padding:8px; border:1px solid #ddd;"><strong>Annulations (fichier)</strong></td>
            <td style="padding:8px; border:1px solid #ddd;">{len(annulations)}</td>
          </tr>
        </table>

        <h2 style="margin-top:24px;">Top nationalités</h2>
        <table style="width:100%; border-collapse:collapse;">
          <tr style="background:#e8eaf6;">
            <th style="padding:8px; border:1px solid #ddd; text-align:left;">Pays</th>
            <th style="padding:8px; border:1px solid #ddd; text-align:left;">Réservations</th>
          </tr>
          {lignes_pays}
        </table>

        <h2 style="margin-top:24px;">Prochaines arrivées (7 jours)</h2>
        <table style="width:100%; border-collapse:collapse;">
          <tr style="background:#e8eaf6;">
            <th style="padding:8px; border:1px solid #ddd; text-align:left;">Client</th>
            <th style="padding:8px; border:1px solid #ddd; text-align:left;">Arrivée</th>
            <th style="padding:8px; border:1px solid #ddd; text-align:left;">Emplacement</th>
            <th style="padding:8px; border:1px solid #ddd; text-align:left;">Pays</th>
          </tr>
          {"".join(
              f"<tr><td style='padding:8px;border:1px solid #ddd;'>{r.nom_complet}</td>"
              f"<td style='padding:8px;border:1px solid #ddd;'>{r.date_arrivee.strftime('%d/%m/%Y')}</td>"
              f"<td style='padding:8px;border:1px solid #ddd;'>{r.emplacement}</td>"
              f"<td style='padding:8px;border:1px solid #ddd;'>{r.pays}</td></tr>"
              for r in actives
              if 0 <= (r.date_arrivee - aujourd_hui).days <= 7
          ) or "<tr><td colspan='4' style='padding:8px;'>Aucune arrivée dans les 7 prochains jours</td></tr>"}
        </table>
      </div>
    </div>
    """
    return rapport_html


def envoyer_rapport_hebdomadaire(zip_path: str, gmail: GmailClient, email_gerant: str) -> bool:
    """Génère et envoie le rapport hebdomadaire au gérant."""
    rapport_html = generer_rapport_hebdomadaire(zip_path)
    aujourd_hui = date.today().strftime("%d/%m/%Y")
    sujet = f"[Rapport IA] Résumé camping – {aujourd_hui}"
    return gmail.envoyer_email(
        destinataire=email_gerant,
        sujet=sujet,
        corps_html=rapport_html,
    )
