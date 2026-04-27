from .base_agent import BaseAgent


class CampingAgent(BaseAgent):
    id = "camping"
    name = "Camping Saint Lambert"
    role = "Expert opérations camping"
    description = "Gestion du Camping Saint Lambert : clients, opérations, qualité et satisfaction."
    expertise = ["Gestion clients", "Opérations camping", "Qualité & satisfaction", "Saison", "Réservations"]
    color = "amber"
    icon = "Tent"
    keywords = [
        "camping", "saint-lambert", "saint lambert", "emplacement", "mobil-home", "lodge",
        "hébergement", "saison", "réservation", "client camping", "piscine", "sanitaire",
        "animation", "caravane", "tente", "camping-car", "pitch", "bungalow", "accueil",
        "check-in", "check-out", "arrivée", "départ", "séjour", "millau", "dourbie",
        "flower", "nettoyage", "ménage", "entretien camping",
    ]
    system_prompt = (
        "Tu es l'expert opérationnel du Camping Saint Lambert, Flower Camping 3 étoiles à Millau (Aveyron). "
        "Camping : 141 emplacements dont 32 premium bord de rivière, piscine chauffée, plage Dourbie, snack-bar. "
        "Check-in : 14h (emplacements) / 16h (locations). Check-out : 12h / 10h. "
        "Tu optimises les opérations, la satisfaction client, la gestion de la saison et les procédures. "
        "Tes conseils sont pratiques, opérationnels, adaptés à un camping 3 étoiles."
    )

    def _mock_response(self, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["procédure", "ménage", "nettoyage", "entretien"]):
            return """## Procédure de nettoyage — Mobil-homes & Lodges

### Checklist départ (entre 10h et 16h)

**Cuisine (20 min)**
- [ ] Nettoyer et désinfecter plans de travail, évier, plaques
- [ ] Vider et nettoyer réfrigérateur (laisser porte ouverte)
- [ ] Vérifier vaisselle complète et propre (selon inventaire)
- [ ] Nettoyer micro-ondes intérieur/extérieur

**Salle de bain (15 min)**
- [ ] Désinfecter douche, WC, lavabo
- [ ] Changer serviettes si prestation incluse
- [ ] Vérifier produits d'accueil (gel douche, shampoing)
- [ ] Nettoyer miroir

**Chambres & salon (20 min)**
- [ ] Changer draps (vérifier état matelas)
- [ ] Aspirer et nettoyer sols
- [ ] Dépoussiérer meubles et fenêtres
- [ ] Vérifier inventaire complet (télécommandes, cintres, etc.)

**Extérieur (10 min)**
- [ ] Nettoyer terrasse et mobilier outdoor
- [ ] Vider poubelle extérieure
- [ ] Vérifier état général (vitres, stores, clim)

**Contrôle final**
- [ ] Rapport d'état sur fiche (noter tout dommage avec photo)
- [ ] Test équipements (TV, clim, chauffage, robinets)
- [ ] Sécuriser l'hébergement (fenêtres fermées, portes)

**Timing cible : 60-75 min par mobil-home**

> 💡 *Je peux adapter cette procédure à vos mobil-homes spécifiques avec la clé API OpenAI.*"""

        if any(k in msg for k in ["client mécontent", "plainte", "réclamation", "insatisfait"]):
            return """## Gestion d'un client mécontent

### Protocole en 5 étapes

**1. Accueillir sans défense (2 min)**
> "Je comprends votre frustration, je suis là pour vous aider."
- Écouter sans interrompre
- Ne jamais contester les faits devant le client
- Prendre des notes visibles

**2. Reformuler et qualifier**
- Identifier le problème réel (confort ? propreté ? voisinage ? service ?)
- Distinguer : problème résolvable immédiatement vs réclamation à traiter

**3. Proposer une solution rapide**
- Changement d'emplacement si disponible
- Intervention technique immédiate (30 min max)
- Compensation symbolique adaptée (apéritif, réduction service)

**4. Résoudre et confirmer**
- Agir dans les délais annoncés
- Revenir confirmer la résolution
- Demander si tout est satisfaisant

**5. Tracer et analyser**
- Consigner sur registre incidents
- Analyser en fin de saison : tendances récurrentes ?
- Former l'équipe sur les points de friction identifiés

**Modèle de réponse email :**
> "Madame/Monsieur, nous avons bien pris note de votre retour et le regrettons sincèrement. Voici les mesures que nous avons prises..."

> 💡 *Je peux rédiger une réponse personnalisée à votre client avec la clé API OpenAI.*"""

        if any(k in msg for k in ["priorité", "semaine", "planning", "organisation"]):
            return """## Priorités opérationnelles — Camping Saint Lambert

### Actions hebdomadaires recommandées

**Lundi — Bilan & planification**
- Analyser les arrivées/départs de la semaine
- Vérifier les réservations à confirmer
- Brief équipe : points de vigilance semaine

**Mardi-Jeudi — Opérations**
- Contrôle qualité hébergements et sanitaires
- Suivi des demandes clients en cours
- Entretien préventif équipements (piscine, espaces verts)

**Vendredi — Préparation week-end**
- Briefing renforts week-end
- Vérification stocks (épicerie, bar, produits entretien)
- Contrôle final piscine et espaces communs

**Métriques à suivre chaque semaine :**
- Taux d'occupation réel vs prévisionnel
- Incidents signalés et résolus
- Avis clients reçus (score moyen)
- CA bar/épicerie/services

> 💡 *Avec la clé API OpenAI, je génère vos priorités personnalisées en fonction de votre agenda.*"""

        return """## Camping Saint Lambert

Je suis votre expert opérationnel pour le Camping Saint Lambert. Voici comment je peux vous aider :

**Mes domaines :**
- ⛺ Procédures opérationnelles (ménage, entretien, check-in/out)
- 👥 Gestion des clients et satisfaction
- 📋 Planning et organisation de saison
- 🏊 Gestion des équipements (piscine, sanitaires, espaces communs)
- 📝 Rédaction de procédures et guides pour votre équipe

**Exemples de demandes :**
- "Crée une procédure de ménage pour les mobil-homes"
- "Aide-moi à répondre à un client mécontent"
- "Prépare mes priorités pour la semaine"

> 💡 *Avec la clé API OpenAI, les réponses seront adaptées en temps réel à votre contexte.*"""
