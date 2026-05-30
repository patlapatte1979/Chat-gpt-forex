"""Source quality agent for demo decisions."""
from __future__ import annotations

from dataclasses import dataclass

from agents.reference_catalog import SourceStatus, SourceType, get_sources_by_type


@dataclass(frozen=True)
class SourceQualitySignal:
    score: int
    details: dict[str, object]


class SourceQualityAgent:
    """Checks whether outside references are only planned or already connected."""

    name = "source_quality"

    def analyze(self, require_connected_references: bool = False) -> SourceQualitySignal:
        news_sources = get_sources_by_type(SourceType.NEWS)
        calendar_sources = get_sources_by_type(SourceType.ECONOMIC_CALENDAR)
        connected = [source.name for source in (*news_sources, *calendar_sources) if source.status == SourceStatus.CONNECTED]
        planned = [source.name for source in (*news_sources, *calendar_sources) if source.status == SourceStatus.PLANNED_ADAPTER]

        if require_connected_references and not connected:
            score = -3
            reason = "connected_reference_required_but_not_available"
        else:
            score = 0
            reason = "reference_catalog_ready"

        return SourceQualitySignal(
            score=score,
            details={
                "reason": reason,
                "connected_references": connected,
                "planned_references": planned,
                "rule": "Only connected adapters can be used as current external confirmation.",
            },
        )
