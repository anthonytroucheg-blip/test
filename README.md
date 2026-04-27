# AI Agent Platform — Camping Saint Lambert & Vanéa

Interface web d'équipe d'agents IA pour entrepreneur, avec Chef d'Orchestre, spécialistes Finance, Camping, Vanéa, Opérations et Stratégie.

## Stack

- **Backend** : Python 3.11+ · FastAPI · SQLite (SQLAlchemy) · OpenAI SDK
- **Frontend** : React 18 · Vite · Tailwind CSS · React Router

---

## Prérequis

- Python 3.11+
- Node.js 18+

---

## Installation

### 1. Backend

```bash
cd /chemin/du/projet

# Créer et activer l'environnement virtuel
python -m venv venv
source venv/bin/activate   # Windows : venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditez .env et renseignez vos valeurs
```

### 2. Frontend

```bash
cd frontend
npm install
```

---

## Lancement

### Backend (terminal 1)

```bash
source venv/bin/activate
uvicorn backend.main:app --reload --port 8000
```

### Frontend (terminal 2)

```bash
cd frontend
npm run dev
```

Ouvrez **http://localhost:5173**

---

## Configuration

Copiez `.env.example` vers `.env` et renseignez :

| Variable | Description | Obligatoire |
|----------|-------------|-------------|
| `OPENAI_API_KEY` | Clé API OpenAI (platform.openai.com) | Non (mode mock sinon) |
| `OPENAI_MODEL` | Modèle à utiliser | Non (défaut: gpt-4o) |
| `COMPANY_NAME` | Nom de votre entreprise | Non |
| `DATABASE_URL` | Chemin SQLite | Non (défaut: data/platform.db) |

Vous pouvez aussi configurer la clé API directement dans l'interface : **Paramètres → OpenAI**.

---

## Fonctionnement

### Sans clé API (mode Mock)
Les agents répondent avec des réponses structurées pré-définies, utiles et contextualisées.
Idéal pour explorer et tester l'interface.

### Avec clé API OpenAI
Les agents utilisent GPT-4o pour générer des réponses personnalisées à votre situation réelle.
Le Chef d'Orchestre synthétise les réponses de tous les agents consultés.

---

## Pages disponibles

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Vue d'ensemble, suggestions, stats |
| Équipe IA | `/agents` | Cartes de tous les agents |
| Chat | `/chat` | Interface messagerie avec les agents |
| Tâches | `/tasks` | Liste d'actions avec priorités |
| Mémoire | `/memory` | Contexte entreprise pour les agents |
| Paramètres | `/settings` | Clé API, modèle, préférences |

---

## Architecture

```
backend/
├── main.py              # FastAPI app + CORS + démarrage DB
├── config.py            # Variables d'environnement (pydantic-settings)
├── database.py          # SQLAlchemy engine + seed initial
├── models.py            # Tables SQLite
├── schemas.py           # Schémas Pydantic v2
├── agents/
│   ├── base_agent.py    # Classe abstraite (mock + OpenAI)
│   ├── orchestrateur.py # Chef d'Orchestre + synthèse
│   ├── finance.py       # Agent Finance
│   ├── camping.py       # Agent Camping Saint Lambert
│   ├── vanea.py         # Agent Vanéa
│   ├── operations.py    # Agent Opérations
│   └── strategie.py     # Agent Stratégie
├── services/
│   ├── router_service.py  # Routage par mots-clés
│   ├── chat_service.py    # Logique de conversation
│   └── memory_service.py  # Contexte mémoire
└── api/
    ├── chat_routes.py     # Conversations & messages
    ├── agent_routes.py    # Infos agents
    ├── task_routes.py     # CRUD tâches
    ├── memory_routes.py   # CRUD mémoire
    └── settings_routes.py # Paramètres

frontend/src/
├── pages/               # Dashboard, Agents, Chat, Tasks, Memory, Settings
├── components/          # Sidebar, AgentCard, ChatWindow, etc.
└── services/api.js      # Client API centralisé
```

---

## API REST

```
GET    /health
GET    /api/agents
GET    /api/conversations
POST   /api/conversations
GET    /api/conversations/{id}
DELETE /api/conversations/{id}
POST   /api/conversations/{id}/messages
GET    /api/tasks
POST   /api/tasks
PUT    /api/tasks/{id}
DELETE /api/tasks/{id}
GET    /api/memory
POST   /api/memory
PUT    /api/memory/{id}
DELETE /api/memory/{id}
GET    /api/settings
PUT    /api/settings
```

Documentation interactive disponible sur **http://localhost:8000/docs**

---

## Ajouter un agent

1. Créer `backend/agents/mon_agent.py` en héritant de `BaseAgent`
2. Définir : `id`, `name`, `role`, `keywords`, `system_prompt`, `_mock_response()`
3. L'ajouter dans `backend/agents/__init__.py`

---

## Données initiales

Au premier démarrage, la base de données est pré-remplie avec :
- Fiche identité du Camping Saint Lambert
- Présentation du concept Vanéa
- Objectifs stratégiques
- Contraintes business
