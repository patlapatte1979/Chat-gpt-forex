"""Reference catalog used by demo trading agents.

These are allowed knowledge/source categories inspired by the project brief.
They are metadata only. A source marked as planned is not live-connected until a
proper adapter with credentials, rate limits and safety rules is implemented.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SourceType(str, Enum):
    EDUCATION = "education"
    NEWS = "news"
    ECONOMIC_CALENDAR = "economic_calendar"
    MACRO_DATA = "macro_data"
    MARKET_DATA = "market_data"
    SENTIMENT = "sentiment"
    TOOL = "tool"


class SourceStatus(str, Enum):
    REFERENCE_ONLY = "reference_only"
    PLANNED_ADAPTER = "planned_adapter"
    CONNECTED = "connected"


@dataclass(frozen=True)
class ReferenceSource:
    name: str
    source_type: SourceType
    status: SourceStatus
    usage: str
    caution: str = ""


REFERENCE_CATALOG: tuple[ReferenceSource, ...] = (
    ReferenceSource(
        name="John J. Murphy - Technical Analysis of the Financial Markets",
        source_type=SourceType.EDUCATION,
        status=SourceStatus.REFERENCE_ONLY,
        usage="Technical analysis concepts: trend, support/resistance, indicators and chart patterns.",
        caution="Book knowledge only; not a live signal source.",
    ),
    ReferenceSource(
        name="IG Academy",
        source_type=SourceType.EDUCATION,
        status=SourceStatus.REFERENCE_ONLY,
        usage="Educational material for trading basics, risk and market mechanics.",
    ),
    ReferenceSource(
        name="BabyPips",
        source_type=SourceType.EDUCATION,
        status=SourceStatus.REFERENCE_ONLY,
        usage="Forex education, pips, lots, margin and basic strategy vocabulary.",
    ),
    ReferenceSource(
        name="Reuters",
        source_type=SourceType.NEWS,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Professional news confirmation when a licensed/API source is available.",
        caution="Do not scrape or claim real-time connection without an approved adapter.",
    ),
    ReferenceSource(
        name="Bloomberg",
        source_type=SourceType.NEWS,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Professional market news context when an authorized source is available.",
        caution="Premium source; use only via allowed access methods.",
    ),
    ReferenceSource(
        name="Trading Economics calendar",
        source_type=SourceType.ECONOMIC_CALENDAR,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Economic events, country data, expected impact and macro context.",
    ),
    ReferenceSource(
        name="ForexFactory calendar",
        source_type=SourceType.ECONOMIC_CALENDAR,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Forex event timing and high-impact news avoidance.",
    ),
    ReferenceSource(
        name="FRED macro data",
        source_type=SourceType.MACRO_DATA,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Rates, inflation, unemployment and macro series where available.",
    ),
    ReferenceSource(
        name="MetaTrader 5 demo data",
        source_type=SourceType.MARKET_DATA,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Historical candles and demo/paper market stream for replay simulations.",
        caution="Real order execution remains disabled by default.",
    ),
    ReferenceSource(
        name="OANDA practice data",
        source_type=SourceType.MARKET_DATA,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Practice account candles/prices if the user chooses this route.",
    ),
    ReferenceSource(
        name="TradingView charts",
        source_type=SourceType.TOOL,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Chart visualization and manual/paper analysis workflow.",
        caution="TradingView should not be treated as a secret-free autonomous execution source.",
    ),
    ReferenceSource(
        name="Selected public analyst/social feeds",
        source_type=SourceType.SENTIMENT,
        status=SourceStatus.PLANNED_ADAPTER,
        usage="Sentiment only after credibility scoring, timestamp checks and duplicate filtering.",
        caution="Never trust unverified social signals or profit promises.",
    ),
)


def get_sources_by_type(source_type: SourceType) -> tuple[ReferenceSource, ...]:
    return tuple(source for source in REFERENCE_CATALOG if source.source_type == source_type)


def summarize_reference_status() -> dict[str, list[str]]:
    summary: dict[str, list[str]] = {status.value: [] for status in SourceStatus}
    for source in REFERENCE_CATALOG:
        summary[source.status.value].append(source.name)
    return summary
