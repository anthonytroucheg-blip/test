from .base_agent import BaseAgent


class VaneaAgent(BaseAgent):
    id = "vanea"
    name = "Vanéa"
    role = "Expert concept Vanéa"
    description = "Développement du concept Vanéa : aires premium camping-car, stratégie et opérations."
    expertise = ["Concept Vanéa", "Aires camping-car", "Développement produit", "Business model", "Expérience client"]
    color = "blue"
    icon = "MapPin"
    keywords = [
        "vanéa", "vanea", "camping-car", "aire", "motorhome", "premium", "service",
        "borne", "électrique", "concept", "label", "stationnement", "camping-cariste",
        "aire de service", "vidange", "eau", "bornes de recharge", "nuit", "étape",
        "accueil camping-car", "van", "fourgon aménagé",
    ]
    system_prompt = (
        "Tu es l'expert développement du concept Vanéa, un projet d'aires de camping-car premium. "
        "Tu aides à développer le concept, le business model, les services proposés, "
        "la stratégie de déploiement et l'expérience client. "
        "Tu connais le marché du camping-car en France (en forte croissance) et les attentes "
        "des camping-caristes modernes en termes de qualité et de services. "
        "Tes conseils sont innovants, pragmatiques et orientés différenciation."
    )

    def _mock_response(self, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["rentabilité", "rentable", "business model", "revenus", "modèle"]):
            return """## Business Model Vanéa

### Sources de revenus potentielles

| Service | Tarif estimé | Volume/an |
|---------|-------------|-----------|
| Nuitée emplacement premium | 18-28€ | 1 500-2 000 nuits |
| Services (électricité, eau, wifi) | 5-8€ | inclus ou option |
| Prestations (lavage, vidange) | 8-15€ | 500-800 utilisations |
| Accès douches/sanitaires | 3-5€ | 200-400 utilisations |
| Partenariats locaux (restaurants, activités) | commission 10-15% | variable |

**Estimation CA premier exercice (20 emplacements) :**
- Taux d'occupation cible : 60% mai-sept, 30% hors saison
- CA estimé : **80 000 - 120 000€**

### Différenciation vs aires municipales
1. **Qualité premium** : sanitaires haut de gamme, bornes rapides, connexion fibre
2. **Expérience locale** : partenariats restaurants/activités, guide local fourni
3. **Services additionnels** : conciergerie, réservation activités, épicerie locale
4. **Application mobile** : réservation en ligne, check-in/out digital

> 💡 *Configurez la clé API OpenAI pour une analyse financière détaillée avec vos hypothèses réelles.*"""

        if any(k in msg for k in ["service", "équipement", "offre", "concept", "prestations"]):
            return """## Concept Vanéa — Offre de services

### Socle premium incontournable
- ✅ Emplacements grands formats (12m minimum)
- ✅ Borne électrique 10A/16A sécurisée
- ✅ Eau potable à chaque emplacement
- ✅ Vidange eaux grises/noires centralisée
- ✅ Sanitaires propres et chauffés (douches incluses)
- ✅ WiFi fibre sur tout le site
- ✅ Sécurité (éclairage, vidéosurveillance)
- ✅ Réservation en ligne obligatoire (limiter les passages nocturnes)

### Services différenciants
- 🌟 Accueil physique (vs distributeur automatique)
- 🌟 Partenariats locaux (restaurants, activités, producteurs)
- 🌟 Guide local exclusif (circuits, bons plans)
- 🌟 Bornes de recharge véhicules électriques
- 🌟 Livraison pain/viennoiseries le matin
- 🌟 Location vélos/trottinettes

### Positionnement tarifaire
- Zone A (touristique) : 20-28€/nuit
- Zone B (passage) : 15-22€/nuit
- Abonnement Vanéa Club : 10% de réduction, réservation prioritaire

> 💡 *Précisez votre localisation pour des recommandations adaptées au territoire.*"""

        if any(k in msg for k in ["lancer", "démarrer", "créer", "ouvrir", "développer"]):
            return """## Plan de lancement Vanéa

### Phase 1 : Validation du concept (3 mois)
1. **Étude de marché locale** : fréquentation camping-cars dans la zone cible
2. **Benchmark** : visiter 5 aires premium concurrentes (France)
3. **Business plan détaillé** : investissement, financement, projection 5 ans
4. **Choix du site pilote** : critères (accessibilité, visibilité, tourisme local)

### Phase 2 : Montage du projet (6 mois)
1. **Financement** : fonds propres, emprunt, subventions (ADEME, Région)
2. **Permis et autorisations** : PLU, autorisation d'exploitation
3. **Design & construction** : architecte paysagiste, prestataires
4. **Partenariats** : acteurs locaux, OTA camping-car (Camperstop, Park4night)

### Phase 3 : Lancement (3 mois avant ouverture)
1. **Communication** : site web, réseaux sociaux, forums camping-car
2. **Référencement** : Park4night, Camperstop, ACSI, FFCC
3. **Tarification** : soft opening avec prix d'inauguration
4. **Process opérationnels** : recrutement, formation, procédures

**Budget de lancement estimé : 250-600k€** selon l'envergure

> 💡 *Je peux construire un plan de lancement personnalisé avec la clé API OpenAI.*"""

        return """## Vanéa — Concept premium camping-car

Je suis votre expert dédié au développement du concept Vanéa. Voici comment je peux vous aider :

**Mes domaines :**
- 🚐 Définition et affinage du concept (services, positionnement)
- 💡 Business model et modèle économique
- 🗺️ Stratégie de déploiement et choix des sites
- 🌟 Expérience client et différenciation
- 📊 Études de marché et analyse concurrentielle

**Exemples de demandes :**
- "Aide-moi à décider si je dois investir dans une nouvelle aire Vanéa"
- "Quels services proposer pour se différencier ?"
- "Crée un plan de lancement pour Vanéa"

> 💡 *Avec la clé API OpenAI, les conseils seront adaptés en temps réel à votre avancement.*"""
