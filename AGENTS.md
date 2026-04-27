# Documentation des Agents IA

## Chef d'Orchestre (`orchestrateur`)

**Rôle** : Coordonne l'équipe, route les demandes, synthétise les réponses.

**Comportement** :
- Analyse chaque message entrant
- Identifie les agents spécialisés à mobiliser (via mots-clés)
- Si un seul agent correspond : retourne sa réponse directement
- Si plusieurs agents correspondent : synthétise leurs réponses
- Fallback : répond lui-même si aucun agent spécifique ne correspond

**Personnalité** : Direct, professionnel, orienté action.

---

## Finance & Comptabilité (`finance`)

**Rôle** : Expert financier de l'entreprise.

**Mots-clés** : budget, coût, revenu, rentabilité, investissement, trésorerie, marge, ROI, etc.

**Domaines** :
- Analyse de rentabilité (RevPASite, taux d'occupation, marge)
- Planification budgétaire et prévisions
- Évaluation d'investissements
- Trésorerie et cash-flow

**System prompt** : Axé sur les métriques camping (RevPASite, occupation), les indicateurs financiers concrets et les décisions chiffrées.

---

## Camping Saint Lambert (`camping`)

**Rôle** : Expert opérationnel du Camping Saint Lambert.

**Mots-clés** : camping, saint-lambert, emplacement, mobil-home, saisonnier, réservation, client, etc.

**Domaines** :
- Procédures opérationnelles (ménage, entretien, check-in/out)
- Gestion et satisfaction clients
- Planning et organisation de saison
- Management d'équipe saisonnière

**Contexte intégré** : 141 emplacements, 32 premium, Flower Camping 3★, Millau, Aveyron.

---

## Vanéa (`vanea`)

**Rôle** : Expert développement du concept Vanéa.

**Mots-clés** : vanéa, camping-car, aire, premium, motorhome, borne, concept, etc.

**Domaines** :
- Définition et développement du concept
- Business model et modèle économique
- Stratégie de déploiement
- Services et expérience client premium

**Contexte** : Marché camping-car en croissance (+15%/an), 4M+ camping-caristes en France.

---

## Opérations & Productivité (`operations`)

**Rôle** : Expert en organisation et efficacité.

**Mots-clés** : procédure, planning, tâche, équipe, organisation, productivité, etc.

**Domaines** :
- Structuration des priorités (méthode Eisenhower)
- Création de procédures et checklists
- Organisation d'équipe et délégation
- Time management pour entrepreneur

---

## Stratégie (`strategie`)

**Rôle** : Conseiller stratégique.

**Mots-clés** : stratégie, croissance, concurrent, marché, développement, décision, etc.

**Domaines** :
- Aide à la décision (méthode DECIDE)
- Analyse SWOT
- Plans marketing et développement
- Vision et roadmap long terme

---

## Routage des messages

Le service de routage (`backend/services/router_service.py`) analyse chaque message :

1. Score chaque agent selon le nombre de mots-clés détectés
2. Sélectionne les 1-2 agents avec les meilleurs scores
3. Si aucun agent ne correspond → Chef d'Orchestre par défaut
4. Si l'utilisateur a sélectionné un agent explicitement → cet agent est prioritaire

## Ajouter un agent

```python
# backend/agents/mon_agent.py
from .base_agent import BaseAgent

class MonAgent(BaseAgent):
    id = "mon_agent"
    name = "Mon Agent"
    role = "Description du rôle"
    description = "Description longue pour la carte agent"
    expertise = ["Domaine 1", "Domaine 2", "Domaine 3"]
    color = "teal"           # indigo|emerald|amber|blue|orange|violet
    icon = "Briefcase"       # icône lucide-react
    keywords = ["mot1", "mot2", "mot3"]
    system_prompt = "Tu es..."

    def _mock_response(self, message: str) -> str:
        return "## Réponse\n\nContenu de la réponse mock."
```

Puis dans `backend/agents/__init__.py` :
```python
from .mon_agent import MonAgent
AGENTS["mon_agent"] = MonAgent()
```
