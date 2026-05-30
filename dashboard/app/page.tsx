import { LegalWarning } from '../components/LegalWarning';
import { ModeBanner } from '../components/ModeBanner';
import { TradeCard } from '../components/TradeCard';
import { accountSettings, tradeCards } from '../lib/demo-data';

export default function Home() {
  return (
    <main className="pageShell">
      <ModeBanner />
      <LegalWarning />

      <section className="settingsGrid" aria-label="Paramètres du compte démo">
        <div><span>Devise</span><strong>{accountSettings.currency}</strong></div>
        <div><span>Localisation</span><strong>{accountSettings.location}</strong></div>
        <div><span>Capital démo</span><strong>{accountSettings.demoCapital}</strong></div>
        <div><span>Risque/trade</span><strong>{accountSettings.riskPerTrade}</strong></div>
        <div><span>Risque max</span><strong>{accountSettings.maxRisk}</strong></div>
        <div><span>Objectif prudent</span><strong>{accountSettings.monthlyObjective}</strong></div>
      </section>

      <section className="sectionHeader">
        <p className="eyebrow">Priorité</p>
        <h2>EUR/USD · USD/CAD · GBP/USD</h2>
        <p>XAU/USD est gardé comme actif secondaire pour une future étape.</p>
      </section>

      <section className="cardsGrid" aria-label="Décisions multi-agents">
        {tradeCards.map((trade) => (
          <TradeCard key={trade.symbol} trade={trade} />
        ))}
      </section>

      <section className="guardrails">
        <h2>Garde-fous obligatoires</h2>
        <ul>
          <li>Mode COPILOT par défaut : l’humain valide chaque idée.</li>
          <li>Mode AUTONOMOUS uniquement sur compte démo confirmé.</li>
          <li>Risque par trade 0,5 %, maximum 1 %, RR minimum 2:1.</li>
          <li>Blocage si news majeure, kill switch ou limites de pertes atteintes.</li>
        </ul>
      </section>
    </main>
  );
}
