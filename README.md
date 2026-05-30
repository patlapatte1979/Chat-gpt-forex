# Chat-gpt-forex

Application de démonstration pour un système Forex multi-agents, pensée pour un usage **COPILOT** avec TradingView + MT5 et un futur mode **AUTONOMOUS DEMO** strictement limité aux comptes démo.

## Avertissement légal

Ce projet est fourni à des fins éducatives et de simulation. Il ne constitue pas un conseil financier, fiscal ou juridique. Le trading Forex comporte un risque de perte. Aucune performance, aucun rendement et aucun profit ne sont promis. Le trading réel est désactivé par défaut.

## Profil de départ

- Devise du compte : CAD
- Localisation : Alberta, Canada
- Capital démo : 10 000 CAD
- Plateforme visée : TradingView + MT5
- Mode initial : COPILOT
- Mode futur : AUTONOMOUS sur compte démo seulement
- Risque par trade : 0,5 %
- Risque maximum : 1 %
- Objectif prudent : préserver le capital et viser 2 % à 5 % par mois maximum, sans promesse de profit
- Actifs prioritaires : EUR/USD, USD/CAD, GBP/USD
- Actif secondaire : XAU/USD

## Structure

```text
agents/          Agents Python et gestion du risque
strategies/      Indicateurs RSI, MACD, Fibonacci, Bollinger, moyennes mobiles
config/          Configuration risque et agents
dashboard/      Application Next.js TypeScript déployable sur Vercel
mt5_bridge/      API FastAPI préparée pour MT5
journal/        CSV de décisions, erreurs et leçons
```

## Installation locale

### Dashboard Next.js

```bash
cd dashboard
npm install
npm run dev
```

Ouvrir ensuite `http://localhost:3000`.

### Build de production

```bash
cd dashboard
npm run build
```

### Agents Python et MT5 Bridge

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m agents.master_agent
uvicorn mt5_bridge.mt5_api:app --reload --port 8000
```

Tester le bridge :

```bash
curl http://localhost:8000/health
```

## Déploiement Vercel

Option simple depuis Vercel :

1. Importer le dépôt GitHub `patlapatte1979/Chat-gpt-forex`.
2. Garder le projet en mode Next.js.
3. Utiliser les commandes définies dans `vercel.json`.
4. Ajouter les variables d’environnement nécessaires, sans jamais mettre de clé dans le frontend.
5. Déployer.

Commandes utiles avec Vercel CLI :

```bash
npm i -g vercel
vercel
vercel --prod
```

## Architecture multi-agents

Le `MasterAgent` appelle les agents spécialisés, additionne les scores, construit un plan de trade de démonstration et transmet le tout au `RiskManager`.

Agents inclus :

- `TechnicalAgent` : RSI, MACD, MM50/MM200, placeholders ADX/Bollinger/Fibonacci.
- `FundamentalAgent` : placeholder FED/BCE/BOC, neutre sans données connectées.
- `NewsAgent` : bloque si une news majeure proche est signalée.
- `SentimentAgent` : placeholder TradingView/X/Reddit, neutre sans API.
- `CorrelationAgent` : placeholder DXY, or, USD/CAD, EUR/USD.
- `RiskManager` : applique les règles de risque obligatoires.
- `JournalAgent` : écrit les décisions, erreurs et leçons dans `journal/*.csv`.

## Règles de risque obligatoires

- Risque par trade : 0,5 %.
- Maximum : 1 %.
- RR minimum : 2:1.
- Stop loss obligatoire.
- Take profit obligatoire.
- Maximum 2 positions ouvertes.
- Perte journalière max : 1 %.
- Perte hebdomadaire max : 3 %.
- Pause après 3 pertes consécutives.
- Blocage avant news majeures.
- AUTONOMOUS uniquement sur compte démo confirmé.
- Kill switch disponible.

## MT5 Bridge

Le dossier `mt5_bridge/` contient une API FastAPI avec :

- `GET /health`
- `POST /prepare-order`
- `POST /execute-order`
- `POST /emergency-stop`

Par défaut, `AUTONOMOUS_ENABLED=False`. Ainsi, `/execute-order` bloque toute exécution autonome et aucun ordre réel n’est envoyé. Le code est prêt pour intégrer plus tard le package `MetaTrader5`, mais seulement après validation d’un compte démo, des symboles broker, des règles d’exécution et du kill switch.

## Limites actuelles

- Les données de marché affichées dans le dashboard sont simulées.
- Les APIs TradingView, calendrier économique, sentiment et MT5 réel ne sont pas encore connectées.
- Le mode AUTONOMOUS DEMO est visible mais désactivé tant que les garde-fous ne sont pas confirmés.
- Aucun secret ne doit être commité. Utiliser `.env.example` comme modèle uniquement.

## Variables d’environnement

Copier `.env.example` vers `.env.local` ou vers les variables Vercel, puis remplir seulement côté serveur lorsque nécessaire.
