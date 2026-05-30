import type { AgentScore } from '../lib/demo-data';

export function AgentScoreList({ scores }: { scores: AgentScore[] }) {
  return (
    <div className="agentGrid">
      {scores.map((agent) => (
        <div className="agentPill" key={agent.name}>
          <span>{agent.name}</span>
          <strong>{agent.score > 0 ? `+${agent.score}` : agent.score}</strong>
          <small>{agent.note}</small>
        </div>
      ))}
    </div>
  );
}
