from .base_agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    id = "orchestrateur"
    name = "Chef d'Orchestre"
    role = "Coordination & synthèse"
    description = "Analyse votre demande, mobilise les agents spécialisés et synthétise une réponse claire et actionnable."
    expertise = ["Coordination", "Synthèse", "Analyse transversale", "Décision multi-domaines"]
    color = "indigo"
    icon = "Network"
    keywords = []  # fallback — s'active quand aucun autre agent ne correspond
    system_prompt = (
        "Tu es le Chef d'Orchestre de l'équipe d'agents IA d'un entrepreneur français. "
        "Il gère le Camping Saint Lambert (Flower Camping 3★, Millau, Aveyron) "
        "et développe Vanéa (concept d'aires de camping-car premium). "
        "\n\nTon rôle : analyser la demande, identifier les domaines concernés "
        "(finance, opérations camping, Vanéa, stratégie, productivité) et synthétiser "
        "une réponse claire, structurée et actionnable. "
        "\n\nTu es direct, professionnel, orienté résultats. "
        "Tu utilises du Markdown pour structurer tes réponses. "
        "Tu proposes toujours 2-3 actions concrètes en fin de réponse."
    )

    def generate_response_orchestrated(
        self,
        message: str,
        history: list[dict],
        agent_responses: dict[str, str],
        memory_context: str = "",
    ) -> str:
        """Synthétise les réponses des agents spécialisés."""
        if not agent_responses:
            return self.generate_response(message, history, memory_context)

        agents_used = list(agent_responses.keys())

        if len(agent_responses) == 1:
            agent_id = agents_used[0]
            return agent_responses[agent_id]

        if not self.__class__.__bases__[0].__module__:
            pass

        from ..config import settings
        if settings.openai_api_key:
            try:
                return self._synthesize_with_openai(message, agent_responses, memory_context)
            except Exception:
                pass

        return self._synthesize_mock(message, agent_responses)

    def _synthesize_with_openai(
        self,
        message: str,
        agent_responses: dict[str, str],
        memory_context: str,
    ) -> str:
        from openai import OpenAI
        from ..config import settings

        agent_names = {
            "finance": "Comptable & Finance",
            "camping": "Camping Saint Lambert",
            "vanea": "Vanéa",
            "operations": "Opérations & Productivité",
            "strategie": "Stratégie",
        }

        synthesis_prompt = (
            f"Demande de l'entrepreneur : {message}\n\n"
            + "\n\n".join(
                f"### Réponse {agent_names.get(k, k)} :\n{v}"
                for k, v in agent_responses.items()
            )
            + "\n\nSynthétise ces réponses en une réponse unifiée, claire et actionnable."
        )

        client = OpenAI(api_key=settings.openai_api_key)
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": synthesis_prompt},
        ]
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            max_tokens=1200,
        )
        return response.choices[0].message.content

    def _synthesize_mock(self, message: str, agent_responses: dict[str, str]) -> str:
        agent_names = {
            "finance": "💰 Comptable & Finance",
            "camping": "⛺ Camping Saint Lambert",
            "vanea": "🚐 Vanéa",
            "operations": "⚡ Opérations",
            "strategie": "🎯 Stratégie",
        }
        combined = "\n\n---\n\n".join(
            f"**{agent_names.get(k, k)}**\n\n{v}"
            for k, v in agent_responses.items()
        )
        return (
            f"## Synthèse — Chef d'Orchestre\n\n"
            f"J'ai analysé votre demande et consulté {len(agent_responses)} agent(s) spécialisé(s).\n\n"
            f"{combined}\n\n"
            f"---\n\n"
            f"> 💡 *Configurez votre clé API OpenAI pour une synthèse intelligente et personnalisée.*"
        )

    def _mock_response(self, message: str) -> str:
        msg = message.lower()

        if any(k in msg for k in ["bonjour", "salut", "hello", "aide", "peux-tu", "comment"]):
            return """## Bonjour ! Je suis votre Chef d'Orchestre 👋

Je coordonne votre équipe d'agents IA spécialisés. Voici ce que je peux faire pour vous :

**Votre équipe IA :**
| Agent | Spécialité |
|-------|-----------|
| 💰 Finance | Budget, rentabilité, investissements |
| ⛺ Camping | Opérations Saint Lambert, clients |
| 🚐 Vanéa | Développement concept, business model |
| ⚡ Opérations | Productivité, procédures, planning |
| 🎯 Stratégie | Vision, décisions, développement |

**Exemples de demandes :**
- "Prépare mes priorités de la semaine"
- "Analyse la rentabilité de Vanéa"
- "Aide-moi à décider si j'investis dans un nouveau mobil-home"
- "Crée une procédure ménage pour mes locations"

Comment puis-je vous aider aujourd'hui ?"""

        return f"""## Analyse de votre demande

J'ai analysé votre message et identifié les domaines concernés. Voici ma réponse structurée :

**Contexte identifié :**
Votre demande touche à la gestion de vos activités entrepreneuriales (Camping Saint Lambert et/ou Vanéa).

**Approche recommandée :**
1. **Identifier la priorité** : quel est l'objectif principal de cette demande ?
2. **Collecter les données** : quelles informations avez-vous déjà ?
3. **Définir le plan d'action** : quelles étapes concrètes suivre ?

**Actions immédiates :**
- Précisez votre demande pour que je mobilise le bon agent spécialisé
- Ou consultez directement l'agent concerné dans le menu "Équipe IA"
- Configurez votre clé API OpenAI pour des réponses entièrement personnalisées

> 💡 *Avec la clé API OpenAI, je synthétise les réponses de tous vos agents spécialisés en une réponse unique et actionnable adaptée à votre situation réelle.*"""
