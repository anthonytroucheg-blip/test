"""
Module de chargement de la sauvegarde Inaxel.
Lit le fichier ZIP quotidien et extrait les données clients/réservations.
"""

import zipfile
import csv
import io
import os
import logging
from datetime import datetime, date
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)

COLONNES_ATTENDUES = [
    "Statut", "Nom du camping", "Code de l'entreprise", "N° séjour",
    "N° client", "Civilité", "Nom", "Prénom", "Email",
    "Téléphone portable", "Date de naissance", "Adresse 1", "Adresse 2",
    "Code Postal", "Pays", "Langue", "Code langue ISO",
    "Date de création", "Date de modification ou annulation",
    "Date arrivée", "Date départ", "Emplacement", "Origine",
    "Montant TTC", "Catégorie emplacement", "Tarif de base", "Etat",
]

STATUTS_VALIDES = {"confirmé", "confirmee", "confirme", "confirmed"}
STATUTS_ANNULATION = {"annulé", "annule", "annulée", "annulee", "cancelled", "canceled"}


@dataclass
class Reservation:
    statut: str
    num_sejour: str
    num_client: str
    civilite: str
    nom: str
    prenom: str
    email: str
    telephone: str
    pays: str
    langue: str
    code_langue: str
    date_arrivee: date
    date_depart: date
    emplacement: str
    categorie_emplacement: str
    montant_ttc: str
    etat: str
    date_creation: Optional[date] = None
    date_modification: Optional[date] = None
    adresse1: str = ""
    adresse2: str = ""
    code_postal: str = ""
    origine: str = ""

    @property
    def nom_complet(self) -> str:
        return f"{self.prenom} {self.nom}".strip()

    @property
    def est_location(self) -> bool:
        cat = self.categorie_emplacement.lower()
        return any(mot in cat for mot in ["mobile", "lodge", "bungalow", "toile", "locatif"])

    @property
    def est_annulation(self) -> bool:
        return self.statut.lower().strip() in STATUTS_ANNULATION

    @property
    def etape_sejour(self) -> str:
        """Retourne l'étape du parcours client selon la date du jour."""
        aujourd_hui = date.today()
        delta_arrivee = (self.date_arrivee - aujourd_hui).days

        if self.est_annulation:
            return "annulation"
        if aujourd_hui < self.date_arrivee:
            if delta_arrivee == 7:
                return "j_moins_7"
            elif delta_arrivee == 1:
                return "j_moins_1"
            elif delta_arrivee == 0:
                return "jour_arrivee"
            else:
                return "avant_sejour"
        elif self.date_arrivee <= aujourd_hui <= self.date_depart:
            return "pendant_sejour"
        else:
            delta_depart = (aujourd_hui - self.date_depart).days
            if delta_depart == 2:
                return "j_plus_2"
            else:
                return "apres_sejour"

    @property
    def salutation(self) -> str:
        civ = self.civilite.strip().lower()
        if civ in ("m.", "m", "mr", "monsieur"):
            return f"Monsieur {self.nom}"
        elif civ in ("mme", "mme.", "madame"):
            return f"Madame {self.nom}"
        return self.nom_complet


def _parse_date(valeur: str) -> Optional[date]:
    """Parse une date depuis les formats Inaxel courants."""
    if not valeur or valeur.strip() == "":
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(valeur.strip(), fmt).date()
        except ValueError:
            continue
    logger.warning(f"Format de date non reconnu : {valeur}")
    return None


def _trouver_csv_dans_zip(zip_path: str) -> Optional[str]:
    """Trouve le fichier CSV principal dans le ZIP."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        if not csv_files:
            return None
        # Priorité aux fichiers contenant "sejour", "reservation" ou "client"
        for mot in ["sejour", "reservation", "client", "export"]:
            for f in csv_files:
                if mot in f.lower():
                    return f
        return csv_files[0]


def charger_reservations(zip_path: str) -> list[Reservation]:
    """
    Charge toutes les réservations depuis la sauvegarde ZIP Inaxel.
    Retourne une liste de Reservation triée par date d'arrivée.
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Fichier de sauvegarde introuvable : {zip_path}")

    reservations = []

    with zipfile.ZipFile(zip_path, "r") as zf:
        nom_csv = _trouver_csv_dans_zip(zip_path)
        if not nom_csv:
            raise ValueError("Aucun fichier CSV trouvé dans la sauvegarde ZIP.")

        logger.info(f"Lecture du fichier : {nom_csv}")

        with zf.open(nom_csv) as f:
            contenu = f.read().decode("utf-8-sig", errors="replace")
            reader = csv.DictReader(io.StringIO(contenu), delimiter=";")

            for i, ligne in enumerate(reader, 1):
                try:
                    date_arrivee = _parse_date(ligne.get("Date arrivée", ""))
                    date_depart = _parse_date(ligne.get("Date départ", ""))

                    if not date_arrivee or not date_depart:
                        continue
                    if not ligne.get("Email", "").strip():
                        continue

                    resa = Reservation(
                        statut=ligne.get("Statut", "").strip(),
                        num_sejour=ligne.get("N° séjour", "").strip(),
                        num_client=ligne.get("N° client", "").strip(),
                        civilite=ligne.get("Civilité", "").strip(),
                        nom=ligne.get("Nom", "").strip(),
                        prenom=ligne.get("Prénom", "").strip(),
                        email=ligne.get("Email", "").strip().lower(),
                        telephone=ligne.get("Téléphone portable", "").strip(),
                        pays=ligne.get("Pays", "").strip(),
                        langue=ligne.get("Langue", "").strip(),
                        code_langue=ligne.get("Code langue ISO", "fr").strip().lower(),
                        date_arrivee=date_arrivee,
                        date_depart=date_depart,
                        emplacement=ligne.get("Emplacement", "").strip(),
                        categorie_emplacement=ligne.get("Catégorie emplacement", "").strip(),
                        montant_ttc=ligne.get("Montant TTC", "").strip(),
                        etat=ligne.get("Etat", "").strip(),
                        date_creation=_parse_date(ligne.get("Date de création", "")),
                        date_modification=_parse_date(ligne.get("Date de modification ou annulation", "")),
                        adresse1=ligne.get("Adresse 1", "").strip(),
                        adresse2=ligne.get("Adresse 2", "").strip(),
                        code_postal=ligne.get("Code Postal", "").strip(),
                        origine=ligne.get("Origine", "").strip(),
                    )
                    reservations.append(resa)

                except Exception as e:
                    logger.warning(f"Ligne {i} ignorée : {e}")
                    continue

    reservations.sort(key=lambda r: r.date_arrivee)
    logger.info(f"{len(reservations)} réservations chargées depuis {zip_path}")
    return reservations


def trouver_client_par_email(reservations: list[Reservation], email: str) -> Optional[Reservation]:
    """Trouve la réservation active la plus proche pour un email donné."""
    email = email.strip().lower()
    aujourd_hui = date.today()

    candidates = [
        r for r in reservations
        if r.email == email and not r.est_annulation
    ]
    if not candidates:
        return None

    # Priorité : séjour en cours > prochain séjour > dernier séjour passé
    en_cours = [r for r in candidates if r.date_arrivee <= aujourd_hui <= r.date_depart]
    if en_cours:
        return en_cours[0]

    futurs = [r for r in candidates if r.date_arrivee > aujourd_hui]
    if futurs:
        return min(futurs, key=lambda r: r.date_arrivee)

    passes = [r for r in candidates if r.date_depart < aujourd_hui]
    if passes:
        return max(passes, key=lambda r: r.date_depart)

    return None


def grouper_par_etape(reservations: list[Reservation]) -> dict[str, list[Reservation]]:
    """Groupe les réservations par étape du parcours client."""
    groupes: dict[str, list[Reservation]] = {
        "j_moins_7": [],
        "j_moins_1": [],
        "jour_arrivee": [],
        "avant_sejour": [],
        "pendant_sejour": [],
        "j_plus_2": [],
        "apres_sejour": [],
        "annulation": [],
    }
    for resa in reservations:
        etape = resa.etape_sejour
        if etape in groupes:
            groupes[etape].append(resa)
    return groupes
