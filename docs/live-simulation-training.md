# Architecture d'entraînement live simulé

Objectif : permettre aux agents de s'entraîner comme dans un marché réel, mais uniquement en simulation/paper-trading. L'agent ne doit jamais voir le futur du graphique. Il reçoit seulement les ticks/chandelles déjà arrivés, prend une décision, puis le simulateur avance ensuite dans le temps.

## But du système

L'application doit devenir un cockpit d'entraînement pour agents de trading capables de comparer plusieurs marchés :

- Forex : EUR/USD, USD/CAD, GBP/USD, USD/JPY, AUD/USD, etc.
- Métaux : XAU/USD/or, XAG/USD/argent.
- Énergie : pétrole WTI, Brent, gaz naturel si une source fiable est ajoutée.
- Indices : US30, NAS100, SPX500, DAX, etc. selon le broker ou la source de données.
- Crypto en option, seulement si on ajoute une source fiable et des règles de risque séparées.

Le compte de départ reste en CAD, avec capital démo et aucune promesse de profit.

## Styles de trading à supporter

- Scalping : M1 à M5, décisions rapides, coûts de spread très importants.
- Day trading : M15 à H1, positions fermées dans la journée.
- Swing trading : H4 à D1, positions sur plusieurs jours.
- Position trading : D1 à W1, décisions plus lentes et macro.

Chaque agent doit pouvoir recevoir le style demandé et adapter ses règles : timeframe, stop loss, take profit, durée maximale, spread acceptable, volatilité minimale, période de news à éviter.

## Règle critique : aucun accès au futur

Le simulateur doit appliquer ces règles :

1. Les chandelles sont triées par temps croissant.
2. À chaque étape, le moteur libère seulement la prochaine chandelle ou le prochain tick.
3. L'agent reçoit seulement l'historique déjà libéré.
4. Les indicateurs sont calculés seulement avec cet historique visible.
5. Le prix d'entrée est le prix disponible après la décision, pas un prix futur parfait.
6. Stop loss, take profit, spread, slippage et frais doivent être appliqués par le paper broker.
7. Les métriques finales sont calculées après coup, jamais données à l'agent pendant la décision.

Cette règle évite le look-ahead bias : l'agent ne peut pas apprendre en connaissant la suite du graphique.

## Pipeline recommandé

```text
Market Data Adapter
  -> Live/Replay Clock
  -> Visible Market Window
  -> Feature Builder
  -> Agents spécialisés
  -> MasterAgent
  -> RiskManager
  -> PaperBroker
  -> Journal/Memory
  -> Dashboard
```

### 1. Market Data Adapter

Responsable de transformer les sources externes en format commun :

```text
time, symbol, timeframe, open, high, low, close, volume, bid, ask, spread
```

Sources possibles :

- Démo locale avec CSV/JSON.
- MetaTrader 5 demo via bridge Python.
- API broker practice/paper-trading.
- TradingView seulement pour visualisation si aucune API officielle de trading n'est disponible dans notre setup.

### 2. Live/Replay Clock

C'est le coeur du mode réaliste. Le clock avance une chandelle à la fois. En mode replay rapide, il peut avancer plus vite, mais il doit respecter l'ordre réel du temps.

### 3. Visible Market Window

La fenêtre visible contient seulement les dernières chandelles déjà libérées : par exemple les 200 dernières M1 ou les 500 dernières M5. Les agents ne peuvent lire que cette fenêtre.

### 4. Feature Builder

Calcule RSI, MACD, moyennes mobiles, Bollinger, ATR, ADX, structure de marché, support/résistance, volatilité, session Londres/New York, spread, volume/tick-volume et distance aux news majeures.

### 5. Agents spécialisés

- TechnicalAgent : graphique et indicateurs.
- RiskAgent/RiskManager : position size, stop, limites.
- NewsAgent : bloque ou réduit le risque autour des news.
- Macro/FundamentalAgent : taux, inflation, banque centrale, pétrole, or, DXY.
- SentimentAgent : seulement quand source fiable et datée.
- MarketSelectorAgent : choisit quel marché regarder en priorité.
- StyleSelectorAgent : scalping, day, swing ou position selon volatilité et contexte.

### 6. PaperBroker

Simule les ordres comme un broker démo :

- balance et equity en CAD;
- positions ouvertes;
- spread;
- slippage;
- frais/commission;
- stop loss;
- take profit;
- margin/marge;
- fermeture partielle future si nécessaire.

Aucun ordre réel ne doit être envoyé par ce module.

## Mémoire et entraînement

L'agent doit journaliser :

- timestamp de décision;
- marché;
- timeframe;
- style;
- données visibles au moment de la décision;
- décision BUY/SELL/WAIT;
- raison de chaque agent;
- score total;
- stop loss/take profit;
- risque CAD;
- résultat après coup;
- erreur reconnue;
- leçon apprise.

Pour l'entraînement sérieux, utiliser une méthode walk-forward :

```text
Période A : entraînement
Période B : validation
Période C : test jamais vu
Puis on décale la fenêtre et on recommence.
```

Le test final doit rester intouché jusqu'à la fin. Sinon l'agent risque de devenir bon seulement sur le passé connu.

## Dashboard voulu

Le dashboard doit afficher :

- mode courant : COPILOT / PAPER DEMO / AUTONOMOUS DEMO LOCKED;
- compte démo CAD;
- marchés surveillés;
- graphique chandelles;
- style choisi;
- décision actuelle;
- raisons des agents;
- historique des décisions;
- equity curve;
- drawdown;
- win rate;
- profit factor;
- pertes consécutives;
- bouton emergency stop.

## Règles de sécurité conservées

- Trading réel désactivé par défaut.
- Mode autonome autorisé seulement sur compte démo confirmé.
- Kill switch obligatoire.
- Stop loss obligatoire.
- Take profit obligatoire.
- RR minimum 2:1 par défaut.
- Risque par trade 0,5 %, maximum 1 %.
- Limite de perte quotidienne et hebdomadaire.
- Pause après pertes consécutives.
- Blocage autour des news majeures.

## Prochaine étape technique

Implémenter dans cet ordre :

1. `simulation/market_universe.py` : marchés et styles supportés.
2. `simulation/no_lookahead_replay.py` : replay de chandelles sans futur visible.
3. `simulation/paper_broker.py` : compte démo et exécution simulée.
4. Connecter `MasterAgent.decide()` au replay pour tester une chandelle à la fois.
5. Ajouter une page dashboard avec graphique chandelles et journal des décisions.
6. Ajouter plus tard un connecteur MT5 demo/practice, sans activer d'ordre réel.
