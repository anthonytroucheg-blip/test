from .base_agent import BaseAgent


class OperationsAgent(BaseAgent):
    id = "operations"
    name = "Opérations & Productivité"
    role = "Expert organisation et efficacité"
    description = "Optimisation des opérations, procédures, planning et productivité entrepreneuriale."
    expertise = ["Procédures", "Planning", "Organisation", "Productivité", "Management d'équipe"]
    color = "orange"
    icon = "Zap"
    keywords = [
        "procédure", "planning", "staff", "équipe", "tâche", "organisation", "processus",
        "maintenance", "fournisseur", "stock", "recrutement", "formation", "productivité",
        "efficacité", "priorité", "agenda", "semaine", "journée", "routine", "checklist",
        "déléguer", "délégation", "objectif", "kpi", "indicateur", "suivi", "réunion",
        "time management", "gestion du temps",
    ]
    system_prompt = (
        "Tu es l'expert Opérations & Productivité d'un entrepreneur qui gère un camping et développe Vanéa. "
        "Tu optimises les processus, créés des procédures claires, planifies les ressources "
        "et améliores l'efficacité opérationnelle. "
        "Tu es direct, orienté résultats, pragmatique. "
        "Tu fournis des checklists actionnables, des templates prêts à l'emploi et des outils concrets."
    )

    def _mock_response(self, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["priorité", "semaine", "journée", "planning"]):
            return """## Priorités de la semaine — Méthode structurée

### Framework de priorisation (Matrice Eisenhower)

**Zone 1 — URGENT + IMPORTANT (faire maintenant)**
→ Problèmes clients, pannes équipements, situations critiques

**Zone 2 — IMPORTANT + non urgent (planifier)**
→ Développement Vanéa, amélioration processus, formation équipe

**Zone 3 — URGENT + non important (déléguer)**
→ Appels fournisseurs routiniers, tâches administratives répétitives

**Zone 4 — ni urgent, ni important (éliminer)**
→ Réunions sans valeur, vérifications excessives

---

### Routine hebdomadaire recommandée

| Jour | Focus | Durée |
|------|-------|-------|
| Lundi 8h | Revue KPI semaine précédente + plan semaine | 1h |
| Mardi-Jeudi | Bloc opérationnel camping | journée |
| Vendredi AM | Travail stratégique (Vanéa, projets) | 3h |
| Vendredi PM | Bilan, facturation, administratif | 2h |

**Règle des 3 priorités :** Chaque matin, identifier les 3 actions qui feraient avancer le plus votre business aujourd'hui.

> 💡 *Partagez votre agenda actuel, je prépare vos priorités personnalisées avec la clé API OpenAI.*"""

        if any(k in msg for k in ["procédure", "checklist", "process", "protocole"]):
            return """## Création d'une procédure opérationnelle

### Structure type d'une procédure efficace

**1. En-tête**
- Titre : "POP-001 — [Nom de la procédure]"
- Version / Date de mise à jour
- Responsable / Valideur

**2. Objectif** (1 phrase)
> "Cette procédure garantit que [résultat attendu] est réalisé [fréquence] par [qui]."

**3. Déclencheur**
> Quand cette procédure s'applique-t-elle ?

**4. Matériel nécessaire**
- Liste des outils, produits, équipements

**5. Étapes (numérotées)**
1. Action précise → Résultat attendu → Durée
2. ...
3. Point de contrôle ✓

**6. Points de vigilance**
> ⚠️ Erreurs fréquentes à éviter

**7. Validation**
- Critères de succès
- Qui valide ?

---

**Outils recommandés pour vos procédures :**
- Notion (gratuit) : centraliser toutes les procédures
- QR codes dans les hébergements → accès direct à la procédure
- Format PDF imprimable pour l'équipe terrain

> 💡 *Donnez-moi le sujet et je rédige la procédure complète avec la clé API OpenAI.*"""

        if any(k in msg for k in ["recrutement", "embaucher", "saisonnier", "équipe"]):
            return """## Recrutement saisonnier — Guide pratique

### Planning de recrutement camping (saison estivale)

**Novembre-Décembre**
- Définir les postes nécessaires (équivalents temps plein)
- Rédiger les fiches de poste
- Contacter anciens saisonniers satisfaits (priorité)

**Janvier-Février**
- Publier annonces (Indeed, Saison.com, ANPE, réseaux sociaux locaux)
- Premier tri CVs

**Mars**
- Entretiens et sélection finale
- Envoi des contrats (contrats saisonniers, CDD)

### Profils prioritaires pour un camping 3 étoiles
1. **Réceptionniste bilingue** (FR/EN minimum) — clé de la satisfaction client
2. **Agent d'entretien** — rigoureux, autonome, sens du détail
3. **Animateur** (selon animation) — énergie, relationnel
4. **Agent technique** — piscine, maintenance courante

### Réduire le turnover
- Prévoir le logement sur place si possible
- Briefing et formation en début de saison (2 jours)
- Check-in régulier (réunion hebdomadaire 15 min)

> 💡 *Je peux rédiger vos fiches de poste et annonces avec la clé API OpenAI.*"""

        return """## Opérations & Productivité

Je suis votre expert en organisation et efficacité opérationnelle. Voici mes domaines :

**Ce que je fais :**
- ⚡ Structuration de vos priorités hebdomadaires
- 📋 Création de procédures et checklists opérationnelles
- 👥 Organisation d'équipe et délégation
- ⏱️ Optimisation de votre temps et productivité
- 📊 Mise en place d'indicateurs de suivi (KPIs)

**Exemples de demandes :**
- "Prépare mes priorités de la semaine"
- "Crée une procédure ménage pour les mobil-homes"
- "Comment mieux organiser ma journée de gérant de camping ?"

> 💡 *Avec la clé API OpenAI, les réponses seront entièrement adaptées à votre contexte.*"""
