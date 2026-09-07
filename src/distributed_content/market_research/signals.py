"""
Market signal collection for niche discovery and competitive intelligence.
"""

from typing import List, Dict, Any
from ..models.niche import MarketSignal


class MarketSignalCollector:
    """
    Collects quantitative demand metrics and qualitative sentiment signals.
    In live environments, this queries Google Trends, SERP APIs, Reddit/Forums, and CPC indices.
    """

    def __init__(self, data_source_adapter: Any = None):
        self.adapter = data_source_adapter

    def collect_signals_for_niche(self, niche_name: str, seed_keywords: List[str]) -> List[MarketSignal]:
        """
        Gathers search volume, trend velocity, CPC, competition DA, and pain-point sentiment.
        """
        # If external adapter is provided, query it; otherwise generate standard calibrated signals.
        if self.adapter:
            return self.adapter.fetch(niche_name, seed_keywords)

        signals = []
        for kw in seed_keywords:
            signal = self._evaluate_keyword_signal(kw)
            signals.append(signal)
        return signals

    def _evaluate_keyword_signal(self, keyword: str) -> MarketSignal:
        """
        Evaluates a keyword using heuristics simulating search engine and community data.
        Recognizes buyer-intent triggers: 'best', 'vs', 'review', 'pricing', 'alternative', 'how to fix'.
        """
        kw_lower = keyword.lower()
        
        # Detect commercial / transactional intent
        high_intent_tokens = ["best", "vs", "versus", "review", "pricing", "alternative", "tool", "software"]
        is_high_intent = any(token in kw_lower for token in high_intent_tokens)
        
        problem_tokens = ["fix", "error", "broken", "issue", "struggle", "troubleshoot", "why does"]
        is_problem = any(token in kw_lower for token in problem_tokens)

        # Baseline parameters
        if is_high_intent:
            buyer_intent_ratio = 0.85
            average_cpc = 3.50
            difficulty = 0.55
            growth = 0.35
            volume = 4500
            pain_density = 0.60
            comp_da = 48.0
        elif is_problem:
            buyer_intent_ratio = 0.60
            average_cpc = 1.80
            difficulty = 0.35
            growth = 0.40
            volume = 6200
            pain_density = 0.88
            comp_da = 35.0
        else:
            # Informational general interest
            buyer_intent_ratio = 0.25
            average_cpc = 0.60
            difficulty = 0.65
            growth = 0.10
            volume = 12000
            pain_density = 0.30
            comp_da = 62.0

        return MarketSignal(
            keyword=keyword,
            monthly_search_volume=volume,
            trend_growth_pct=growth,
            average_cpc=average_cpc,
            buyer_intent_ratio=buyer_intent_ratio,
            difficulty_score=difficulty,
            competition_da_avg=comp_da,
            sentiment_pain_density=pain_density,
        )
