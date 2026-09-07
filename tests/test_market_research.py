"""
Tests for market research signal collection, feasibility analysis, and opportunity scoring.
"""

import unittest
from src.distributed_content.market_research import (
    MarketSignalCollector,
    MarketFeasibilityAnalyzer,
    OpportunityScorer,
)
from src.distributed_content.models import MarketSignal, MonetizationType


class TestMarketResearch(unittest.TestCase):

    def setUp(self):
        self.collector = MarketSignalCollector()
        self.analyzer = MarketFeasibilityAnalyzer()
        self.scorer = OpportunityScorer()

    def test_signal_collector_identifies_buyer_intent(self):
        signals = self.collector.collect_signals_for_niche(
            "Self-Hosted Storage",
            ["best self-hosted cloud storage for privacy", "how to fix nextcloud sync error"]
        )
        self.assertEqual(len(signals), 2)
        best_sig = signals[0]
        fix_sig = signals[1]

        self.assertGreater(best_sig.buyer_intent_ratio, 0.7)
        self.assertGreater(fix_sig.sentiment_pain_density, 0.7)

    def test_feasibility_selects_affiliate_for_comparison_queries(self):
        signals = [
            MarketSignal(
                keyword="best cold plunge tub for athletes",
                monthly_search_volume=8000,
                trend_growth_pct=0.45,
                average_cpc=3.20,
                buyer_intent_ratio=0.85,
                difficulty_score=0.40,
                competition_da_avg=45.0,
                sentiment_pain_density=0.50,
            )
        ]
        mtype, config = self.analyzer.select_best_monetization_model(signals)
        self.assertEqual(mtype, MonetizationType.AFFILIATE)
        self.assertGreater(config.target_rpm, 20.0)

    def test_opportunity_scorer_calculates_high_score_for_lucrative_niche(self):
        signals = [
            MarketSignal(
                keyword="b2b vector database comparison",
                monthly_search_volume=12000,
                trend_growth_pct=0.55,
                average_cpc=5.50,
                buyer_intent_ratio=0.80,
                difficulty_score=0.35,
                competition_da_avg=40.0,
                sentiment_pain_density=0.75,
            )
        ]
        score = self.scorer.score_niche("Vector Databases", signals)
        self.assertGreater(score.composite_score, 65.0)
        self.assertGreater(score.projected_roi_pct, 50.0)
        self.assertIn("Optimal vehicle:", " ".join(score.thesis_notes))


if __name__ == "__main__":
    unittest.main()
