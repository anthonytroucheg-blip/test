"""
Configuration du Flower Camping Saint Lambert - Millau Rivière
Toutes les informations du camping utilisées par l'agent IA.
"""

CAMPING = {
    "nom": "Flower Camping Saint Lambert",
    "nom_court": "Camping Millau Rivière",
    "adresse": "2050 Avenue de l'Aigoual, 12100 Millau",
    "telephone": "+33 (0)5 65 60 00 48",
    "email_contact": "contact@campingsaintlambert.fr",
    "email_agent": "",  # À renseigner : adresse Gmail de l'agent IA
    "site_web": "https://www.camping-millau-riviere.fr",
    "classement": "3 étoiles",
    "reseau": "Flower Camping",
    "lien_avis_tripadvisor": "https://www.tripadvisor.fr/Hotel_Review-g196627-d6579555-Reviews-Camping_Saint_Lambert-Millau_Aveyron_Occitanie.html",
    "lien_avis_google": "",  # À renseigner : lien Google Maps avis
}

LOCALISATION = {
    "region": "Occitanie",
    "departement": "Aveyron (12)",
    "ville": "Millau",
    "description": (
        "Situé à 2,5 km du centre-ville de Millau, à l'entrée des Gorges du Tarn, "
        "sur les rives ombragées de la rivière Dourbie. "
        "À proximité du célèbre Viaduc de Millau et des Grands Causses."
    ),
    "attractions_proches": [
        "Viaduc de Millau",
        "Gorges du Tarn",
        "Grottes de Roquefort-sur-Soulzon",
        "Plateaux du Larzac",
        "Canoë, kayak, rafting, canyoning, escalade",
    ],
}

HEBERGEMENTS = {
    "emplacements": {
        "nombre_total": 141,
        "nombre_premium": 32,
        "description_premium": "Emplacements premium en bord de rivière",
        "check_in": "14h00",
        "check_out": "12h00",
    },
    "locations": {
        "types": ["Mobile-home", "Lodge", "Bungalow toile", "Tente équipée"],
        "capacite_max": 6,
        "check_in": "16h00",
        "check_out": "10h00",
    },
}

EQUIPEMENTS = {
    "piscine": {
        "disponible": True,
        "description": "Piscine chauffée en plein air",
        "periode": "Mai à Septembre",
        "horaires": "10h00 - 19h00",
    },
    "riviere": {
        "disponible": True,
        "description": "Plage privée sur la Dourbie avec accès direct pour baignade et pêche à la truite",
    },
    "restauration": {
        "disponible": True,
        "services": ["Restaurant/Snack-bar", "Bar", "Pain frais le matin"],
    },
    "wifi": {
        "disponible": True,
        "gratuit": True,
        "description": "WiFi gratuit sur l'ensemble du camping",
    },
    "sanitaires": {
        "disponible": True,
        "description": "Sanitaires chauffés et propres, lave-linge et sèche-linge disponibles",
    },
    "activites": [
        "Pétanque",
        "Ping-pong",
        "Baby-foot",
        "Badminton",
        "Mini-golf",
        "Structures gonflables",
        "Aire de jeux enfants",
        "Pêche à la truite",
        "Baignade en rivière",
    ],
    "services": [
        "Wifi gratuit",
        "Location de vélos",
        "Épicerie / pain frais",
        "Lave-linge / sèche-linge",
    ],
}

ACCUEIL = {
    "horaires": "8h00 - 20h00",
    "telephone": "+33 (0)5 65 60 00 48",
    "message_urgence": (
        "Pour toute situation urgente, notre équipe à l'accueil est disponible "
        "de 8h00 à 20h00 et sera ravie de vous aider immédiatement."
    ),
}

REGLEMENT = {
    "animaux": {
        "acceptes": True,
        "conditions": "Animaux acceptés sur présentation du carnet de vaccination à jour. "
                      "Tenus en laisse obligatoire sur le camping.",
    },
    "silence": "Silence demandé à partir de 22h00.",
    "vitesse": "Vitesse limitée à 10 km/h sur le camping.",
    "dechets": "Tri sélectif obligatoire. Poubelles de tri situées près de l'entrée principale.",
}

LANGUES_SUPPORTEES = {
    "fr": "Français",
    "en": "English",
    "nl": "Nederlands",
    "de": "Deutsch",
    "es": "Español",
}

# Mots-clés déclenchant une redirection vers l'accueil
MOTS_CLES_URGENCE = [
    "urgence", "urgent", "problème", "probleme", "panne", "fuite", "casse",
    "blessé", "blessure", "accident", "vol", "annuler", "annulation",
    "remboursement", "rembourser", "mécontent", "mecontent", "plainte",
    "inacceptable", "scandale", "police", "pompier", "médecin", "docteur",
    "broken", "emergency", "cancel", "refund", "complaint", "injured",
    "kapot", "annuleren", "Notfall", "stornieren",
]
