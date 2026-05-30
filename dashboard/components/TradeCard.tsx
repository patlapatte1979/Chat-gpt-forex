import type { TradeCard as TradeCardType } from '../lib/demo-data';
import { AgentScoreList } from './AgentScoreList';

const statusClass = {
  APPROVED: 'approved',
  REJECTED: 'rejected',
  WAIT: 'waiting',
};

export function TradeCard({ trade }: { trade: TradeCardType }) {
  return (
    <article className="tradeCard">
      <div className="cardHeader">
        <div>
          <p className="symbolCode">{trade.symbol}</p>
          <h2>{trade.displayName}</h2>
        </div>
        <div className="decisionBlock">
          <span className={`statusBadge ${statusClass[trade.status]}`}>{trade.status}</span>
          <strong>{trade.decision}</strong>
        </div>
      </div>

      <div className="tradeMetrics">
        <span>Entrée <strong>{trade.entry}</strong></span>
        <span>Stop loss <strong>{trade.stopLoss}</strong></span>
        <span>Take profit <strong>{trade.takeProfit}</strong></span>
        <span>RR <strong>{trade.riskReward}</strong></span>
        <span>Lot <strong>{trade.lotSize}</strong></span>
        <span>Risque <strong>{trade.riskCad}</strong></span>
      </div>

      <AgentScoreList scores={trade.agentScores} />
    </article>
  );
}
