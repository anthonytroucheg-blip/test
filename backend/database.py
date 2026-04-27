import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

os.makedirs("data", exist_ok=True)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    _seed_initial_data()


def _seed_initial_data():
    from .models import MemoryItem, Setting
    db = SessionLocal()
    try:
        if db.query(MemoryItem).count() == 0:
            items = [
                MemoryItem(
                    category="camping",
                    title="Camping Saint Lambert — Fiche identité",
                    content=(
                        "Flower Camping Saint Lambert, 3 étoiles, Millau (Aveyron 12).\n"
                        "141 emplacements dont 32 premium en bord de rivière Dourbie.\n"
                        "Check-in : 14h (emplacements), 16h (locations). Check-out : 12h / 10h.\n"
                        "Équipements : piscine chauffée (10h-19h, mai-sept), plage privée, snack-bar, WiFi gratuit.\n"
                        "Réseau : Flower Camping. Site : https://www.camping-millau-riviere.fr"
                    ),
                ),
                MemoryItem(
                    category="vanea",
                    title="Vanéa — Concept",
                    content=(
                        "Concept d'aires de camping-car premium haut de gamme.\n"
                        "Vision : offrir une expérience qualitative aux camping-caristes, "
                        "différenciée des aires municipales standard.\n"
                        "Axes : services premium, équipements modernes, expérience locale."
                    ),
                ),
                MemoryItem(
                    category="objectives",
                    title="Objectifs stratégiques",
                    content=(
                        "1. Maximiser le taux d'occupation du Camping Saint Lambert\n"
                        "2. Développer et lancer le concept Vanéa\n"
                        "3. Améliorer la satisfaction et fidélisation clients\n"
                        "4. Digitaliser les opérations (IA, automatisation)\n"
                        "5. Développer les réservations en direct (réduire commissions OTA)"
                    ),
                ),
                MemoryItem(
                    category="constraints",
                    title="Contraintes & limites",
                    content=(
                        "- Saisonnalité forte (haute saison juillet-août)\n"
                        "- Ressources humaines limitées hors saison\n"
                        "- Budget marketing à optimiser\n"
                        "- Dépendance partielle aux OTA (Booking, Camping.fr)"
                    ),
                ),
            ]
            db.add_all(items)

        if db.query(Setting).count() == 0:
            defaults = [
                Setting(key="company_name", value="Camping Saint Lambert & Vanéa"),
                Setting(key="openai_model", value="gpt-4o"),
                Setting(key="response_style", value="professionnel"),
                Setting(key="openai_api_key", value=""),
            ]
            db.add_all(defaults)

        db.commit()
    finally:
        db.close()
