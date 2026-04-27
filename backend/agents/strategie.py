from .base_agent import BaseAgent


class StrategieAgent(BaseAgent):
    id = "strategie"
    name = "Stratégie"
    role = "Conseiller stratégique"
    description = "Vision, développement business, décisions stratégiques et positionnement."
    expertise = ["Stratégie business", "Développement", "Positionnement", "Décision", "Vision long terme"]
    color = "violet"
    icon = "Target"
    keywords = [
        "stratégie", "croissance", "concurrent", "marché", "développement", "partenariat",
        "expansion", "objectif", "vision", "positionnement", "swot", "pivot",
        "décision", "investir", "lancer", "opportunité", "risque", "analyse",
        "long terme", "business plan", "modèle économique", "différenciation",
        "avantage concurrentiel", "benchmark", "tendance",
    ]
    system_prompt = (
        "Tu es le conseiller stratégique d'un entrepreneur qui gère le Camping Saint Lambert (Millau) "
        "et développe Vanéa (aires camping-car premium). "
        "Tu l'aides à prendre les bonnes décisions, à développer sa vision long terme "
        "et à saisir les opportunités de croissance. "
        "Tu analyses les forces, faiblesses, opportunités et menaces avec lucidité. "
        "Tu es direct, sans filtre, orienté résultats. "
        "Tu proposes des cadres de décision clairs et des scénarios concrets."
    )

    def _mock_response(self, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["décision", "investir", "choisir", "faut-il", "dois-je"]):
            return """## Cadre de décision stratégique

### Méthode DECIDE en 6 étapes

**D — Définir la décision**
Quelle est exactement la décision à prendre ? (Soyez précis)

**E — Établir les critères**
Sur quelles bases allez-vous décider ?
- Critères financiers (ROI, délai récupération)
- Critères opérationnels (faisabilité, ressources)
- Critères stratégiques (alignement vision, différenciation)

**C — Collecter l'information**
- Données disponibles
- Ce qui manque et doit être cherché
- Expériences comparables

**I — Identifier les alternatives**
Minimum 3 options : faire / ne pas faire / faire autrement

**D — Décider**
Pondérer chaque critère et noter chaque option (1-5)

**E — Évaluer les résultats**
Définir des indicateurs de succès et un point de revue à 3 mois

---

**Question pour affiner mon analyse :**
- Quelle est la décision spécifique que vous devez prendre ?
- Quel est votre horizon de décision ?

> 💡 *Décrivez votre situation précise et j'analyse les options avec la clé API OpenAI.*"""

        if any(k in msg for k in ["swot", "analyse", "forces", "faiblesses", "opportunités"]):
            return """## Analyse SWOT — Camping Saint Lambert & Vanéa

### Camping Saint Lambert

| Forces 💪 | Faiblesses ⚠️ |
|-----------|--------------|
| Localisation Millau (Viaduc, Gorges du Tarn) | Forte saisonnalité |
| Label Flower Camping (réseau national) | Dépendance OTA |
| Cadre naturel exceptionnel (Dourbie) | Ressources humaines limitées HS |
| 3 étoiles, 141 emplacements | Marketing digital à renforcer |

| Opportunités 🚀 | Menaces 🔴 |
|----------------|-----------|
| Tourisme naturel en hausse | Météo imprévisible |
| Clientèle nord-européenne croissante | Concurrence campings proches |
| Digitalisation (IA, automatisation) | Inflation charges (énergie, salaires) |
| Restauration locale en tendance | Réglementations environnementales |

### Vanéa

| Forces 💪 | Faiblesses ⚠️ |
|-----------|--------------|
| Marché camping-car en forte croissance | Concept à créer de zéro |
| Positionnement premium différenciant | Investissement initial important |
| Complémentaire au camping | Expertise à acquérir |

| Opportunités 🚀 | Menaces 🔴 |
|----------------|-----------|
| 4M+ camping-caristes en France | Multiplication des aires municipales gratuites |
| Tourisme itinérant post-COVID | Copie facile du concept |
| Subventions mobilité/tourisme durable | Réglementation stationnement |

> 💡 *Avec la clé API OpenAI, j'approfondis chaque quadrant avec vos données réelles.*"""

        if any(k in msg for k in ["marketing", "communication", "plan", "attractivité", "notoriété"]):
            return """## Plan marketing stratégique

### Camping Saint Lambert — Axes prioritaires

**1. Référencement direct (réduire les OTA)**
- Site web optimisé SEO (mots-clés : camping Millau, Aveyron, Dourbie)
- Partenariat Flower Camping (trafic réseau)
- Programme fidélité clients directs (-5% sur réservation directe)

**2. Contenu digital (coût faible, impact fort)**
- Instagram : photos qualité pro des paysages, activités, hébergements
- YouTube : visite virtuelle 360° des hébergements
- Blog : "Que faire à Millau", "Guide Gorges du Tarn" (SEO)

**3. Marchés prioritaires**
- Néerlandais et Belges : fort potentiel, aiment Aveyron
- Familles françaises (Île-de-France, Rhône-Alpes)
- Seniors actifs (hors saison, mai-juin, septembre)

**4. Partenariats locaux**
- Office de tourisme Millau Grands Causses
- Sites d'activités (Roquefort, Viaduc, canoë)
- Restaurants partenaires

**Budget marketing recommandé : 8-12% du CA**

> 💡 *Je développe un plan marketing complet et personnalisé avec la clé API OpenAI.*"""

        return """## Stratégie & Développement

Je suis votre conseiller stratégique. Voici mes domaines d'intervention :

**Ce que je fais :**
- 🎯 Aide à la décision stratégique (investir, développer, pivoter)
- 📊 Analyse SWOT et benchmarks concurrentiels
- 🚀 Plans de développement (Camping, Vanéa, nouveaux projets)
- 💡 Identification d'opportunités de croissance
- 🗺️ Vision et roadmap long terme

**Exemples de demandes :**
- "Aide-moi à décider si je dois investir dans une nouvelle aire Vanéa"
- "Prépare un plan marketing pour le Camping Saint Lambert"
- "Analyse les forces et faiblesses de mon positionnement"

> 💡 *Avec la clé API OpenAI, les analyses s'appuient sur votre contexte réel.*"""
