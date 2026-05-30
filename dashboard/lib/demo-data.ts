export type Decision = 'BUY' | 'SELL' | 'WAIT';
export type Status = 'APPROVED' | 'REJECTED' | 'WAIT';

export type AgentScore = {
  name: string;
  score: number;
  note: string;
};

export type TradeCard = {
  symbol: string;
  displayName: string;
  decision: Decision;
  status: Status;
  entry: string;
  stopLoss: string;
  takeProfit: string;
  riskReward: string;
  lotSize: string;
  riskCad: string;
  agentScores: AgentScore[];
};

export const accountSettings = {
  currency: 'CAD',
  location: 'Alberta, Canada',
  demoCapital: '10 000 CAD',
  mode: 'COPILOT',
  riskPerTrade: '0,5 %',
  maxRisk: '1 %',
  monthlyObjective: '2 % à 5 % maximum, sans promesse de profit',
};

export const tradeCards: TradeCard[] = [
  {
    symbol: 'EURUSD',
    displayName: 'EUR/USD',
    decision: 'WAIT',
    status: 'WAIT',
    entry: '1.08500',
    stopLoss: '—',
    takeProfit: '—',
    riskReward: '—',
    lotSize: '0.00',
    riskCad: '0 CAD',
    agentScores: [
      { name: 'Technique', score: 2, note: 'RSI/MACD légèrement positifs' },
      { name: 'Fondamental', score: 0, note: 'API macro non connectée' },
      { name: 'News', score: 0, note: 'Calendrier simulé' },
      { name: 'Sentiment', score: 0, note: 'Neutre' },
      { name: 'Corrélation', score: 0, note: 'Neutre' },
    ],
  },
  {
    symbol: 'USDCAD',
    displayName: 'USD/CAD',
    decision: 'SELL',
    status: 'APPROVED',
    entry: '1.36500',
    stopLoss: '1.37000',
    takeProfit: '1.35500',
    riskReward: '2.0',
    lotSize: '0.01',
    riskCad: '50 CAD',
    agentScores: [
      { name: 'Technique', score: -5, note: 'Signal demo baissier' },
      { name: 'Fondamental', score: 0, note: 'FED/BOC non connecté' },
      { name: 'News', score: 0, note: 'Pas de blocage simulé' },
      { name: 'Sentiment', score: 0, note: 'Neutre' },
      { name: 'Corrélation', score: -1, note: 'Placeholder DXY' },
    ],
  },
  {
    symbol: 'GBPUSD',
    displayName: 'GBP/USD',
    decision: 'WAIT',
    status: 'REJECTED',
    entry: '1.27500',
    stopLoss: '—',
    takeProfit: '—',
    riskReward: '—',
    lotSize: '0.00',
    riskCad: '0 CAD',
    agentScores: [
      { name: 'Technique', score: 1, note: 'Signal trop faible' },
      { name: 'Fondamental', score: 0, note: 'Neutre' },
      { name: 'News', score: -10, note: 'News majeure simulée proche' },
      { name: 'Sentiment', score: 0, note: 'Non connecté' },
      { name: 'Corrélation', score: 0, note: 'Neutre' },
    ],
  },
];
