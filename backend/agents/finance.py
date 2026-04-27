from .base_agent import BaseAgent


class FinanceAgent(BaseAgent):
    id = "finance"
    name = "Comptable & Finance"
    role = "Expert financier"
    description = "Analyse financière, budgets, rentabilité, investissements et trésorerie."
    expertise = ["Analyse financière", "Budget & prévisions", "Rentabilité", "Investissement", "Trésorerie"]
    color = "emerald"
    icon = "TrendingUp"
    keywords = [
        "budget", "coût", "revenu", "rentabilité", "investissement", "trésorerie",
        "prix", "tarif", "marge", "financement", "emprunt", "bénéfice", "dépense",
        "chiffre d'affaires", "ca", "résultat", "comptabilité", "fiscal", "taxe",
        "charge", "recette", "prévision", "cash", "retour sur investissement", "roi",
        "amortissement", "dette", "capitaux", "financer", "rembourser",
    ]
    system_prompt = (
        "Tu es l'expert Comptable et Finance d'un entrepreneur qui gère le Camping Saint Lambert (Millau) "
        "et développe le concept Vanéa (aires camping-car premium). "
        "Tu analyses les aspects financiers avec précision : rentabilité, budgets, trésorerie, investissements. "
        "Tu utilises des chiffres, métriques et indicateurs concrets (RevPASite, taux d'occupation, marge brute...). "
        "Tes réponses sont structurées, directes, orientées décision. "
        "Tu proposes toujours des actions concrètes avec des ordres de grandeur chiffrés."
    )

    def _mock_response(self, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["rentabilité", "rentable", "bénéfice", "profit", "marge"]):
            return """## Analyse de rentabilité

**Indicateurs clés à suivre :**
- **RevPASite** (Revenue per Available Site) : revenu total / nombre d'emplacements / jours de saison
- **Taux d'occupation** : cible 85%+ en haute saison (juillet-août), 50-60% en mi-saison
- **Marge brute** : revenus - charges variables (eau, électricité, consommables)
- **Panier moyen par séjour** : hébergement + services (bar, épicerie, vélos...)

**Points de vigilance :**
1. Comparer les revenus directs vs OTA (économiser les 15-20% de commission)
2. Analyser la contribution de chaque catégorie (emplacements, locations, services)
3. Calculer le seuil de rentabilité par type d'hébergement

**Actions recommandées :**
1. Mettre en place un tableau de bord financier mensuel
2. Identifier les 3 postes de dépenses les plus optimisables
3. Calculer le RevPASite hebdomadaire pour ajuster les tarifs

> 💡 *Configurez votre clé API OpenAI dans les Paramètres pour une analyse personnalisée de vos chiffres réels.*"""

        if any(k in msg for k in ["investissement", "investir", "financer", "emprunt", "crédit"]):
            return """## Analyse d'investissement

**Méthode d'évaluation recommandée :**
1. **VAN** (Valeur Actuelle Nette) : flux futurs actualisés - investissement initial
2. **ROI** : (gain net / coût investissement) × 100
3. **Délai de récupération** : durée pour récupérer l'investissement

**Questions clés avant tout investissement :**
- Quel est le montant exact de l'investissement ?
- Quels revenus supplémentaires génère-t-il (et sur combien d'années) ?
- Quel est le coût du financement (taux d'emprunt) ?
- Y a-t-il des aides ou subventions disponibles ? (ADEME, Région Occitanie, BPI)

**Pour Vanéa spécifiquement :**
- Coût de création d'une aire premium : 200-500k€ selon la taille
- Revenus potentiels : 10-25€/nuit × capacité × taux d'occupation
- Subventions possibles : ADEME mobilité, tourisme durable, région

> 💡 *Précisez les chiffres de votre projet pour une analyse détaillée avec la clé API OpenAI.*"""

        if any(k in msg for k in ["budget", "prévision", "planifier"]):
            return """## Budget & Prévisions

**Structure de budget recommandée pour un camping :**

| Poste | % du CA typique |
|-------|----------------|
| Charges de personnel | 30-35% |
| Charges d'exploitation | 15-20% |
| Marketing & distribution | 8-12% |
| Maintenance & travaux | 5-8% |
| Assurances & admin | 3-5% |
| **Résultat net cible** | **15-25%** |

**Exercice de planification :**
1. Définir le CA cible par mois (courbe saisonnière)
2. Allouer les charges fixes et variables
3. Identifier les leviers d'optimisation
4. Prévoir un fonds de réserve (10% du CA) pour imprévus

> 💡 *Partagez votre CA actuel pour affiner ces ratios à votre situation.*"""

        return """## Analyse Financière

Je suis votre expert Finance & Comptabilité. Voici les domaines où je peux vous aider :

**Mes domaines d'intervention :**
- 📊 Analyse de rentabilité (Camping Saint Lambert, Vanéa)
- 💰 Optimisation budgétaire et réduction des coûts
- 📈 Évaluation d'investissements et calcul de ROI
- 🔮 Prévisions et planification financière
- 💳 Gestion de trésorerie et cash-flow

**Pour commencer, dites-moi :**
- Quel aspect financier souhaitez-vous analyser ?
- Avez-vous des chiffres actuels à partager ?

> 💡 *Avec la clé API OpenAI, je pourrai analyser vos données financières réelles et produire des rapports personnalisés.*"""
