export function ModeBanner() {
  return (
    <section className="modeBanner" aria-label="Mode de trading">
      <div>
        <p className="eyebrow">Mode initial</p>
        <h1>Forex Multi‑Agent COPILOT</h1>
        <p>
          Tableau de bord mobile-first pour TradingView + MT5, en simulation avec capital démo de 10 000 CAD.
        </p>
      </div>
      <div className="modeActions">
        <span className="activeMode">COPILOT actif</span>
        <button className="disabledButton" disabled title="Disponible seulement après confirmation des garde-fous démo">
          AUTONOMOUS DEMO
        </button>
      </div>
    </section>
  );
}
