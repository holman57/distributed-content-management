"""
Tests for LifecycleGovernor data-driven spin-up, scale, pivot, and wind-down logic.
"""

import unittest
from src.distributed_content.models import (
    Niche,
    NicheLifecycleState,
    OpportunityScore,
    MonetizationType,
    PerformanceMetrics,
    LifecycleAction,
)
from src.distributed_content.decision_engine import LifecycleGovernor, GovernanceThresholds


class TestDecisionGovernor(unittest.TestCase):

    def setUp(self):
        self.governor = LifecycleGovernor()

    def test_candidate_spin_up_approval(self):
        niche = Niche(
            id="niche-valid",
            name="AI Tooling",
            description="B2B developer tooling",
            vertical="Software",
            opportunity_score=OpportunityScore(
                composite_score=78.0,
                demand_index=80.0,
                intent_index=85.0,
                competition_barrier=40.0,
                projected_roi_pct=65.0,
                recommended_monetization=MonetizationType.LEAD_GENERATION,
                confidence=0.9,
            )
        )
        decision = self.governor.evaluate_candidate(niche)
        self.assertEqual(decision.action, LifecycleAction.SPIN_UP)
        self.assertIn("Approved for spin-up", decision.rationale)

    def test_candidate_spin_up_rejected(self):
        niche = Niche(
            id="niche-poor",
            name="Generic Memes",
            description="Low intent entertainment",
            vertical="Entertainment",
            opportunity_score=OpportunityScore(
                composite_score=42.0,
                demand_index=50.0,
                intent_index=20.0,
                competition_barrier=80.0,
                projected_roi_pct=-15.0,
                recommended_monetization=MonetizationType.PROGRAMMATIC_ADS,
                confidence=0.8,
            )
        )
        decision = self.governor.evaluate_candidate(niche)
        self.assertEqual(decision.action, LifecycleAction.HOLD)
        self.assertIn("did not clear spin-up hurdles", decision.rationale)

    def test_active_pipeline_scale_decision(self):
        niche = Niche(id="niche-scaled", name="SaaS Reviews", description="Testing", vertical="Tech")
        metrics = PerformanceMetrics(
            total_pieces_published=8,
            monthly_impressions=25000,
            monthly_clicks=1200,
            avg_dwell_time_seconds=95.0,
            conversions=36,
            total_cost=480.0,
            total_revenue=1800.0,
            traffic_growth_rate=0.25,
            indexation_rate=1.0,
        )
        decision = self.governor.evaluate_active_pipeline(niche, metrics)
        self.assertEqual(decision.action, LifecycleAction.SCALE)
        self.assertIn("Unit economics validated for scale", decision.rationale)

    def test_active_pipeline_pivot_decision(self):
        niche = Niche(id="niche-pivot", name="Linux Desktop", description="Testing", vertical="Tech")
        metrics = PerformanceMetrics(
            total_pieces_published=6,
            monthly_impressions=50000,
            monthly_clicks=2200,
            avg_dwell_time_seconds=110.0,
            conversions=4,     # Conversion rate = 4 / 2200 = 0.18% (< 0.5%)
            total_cost=360.0,
            total_revenue=80.0,
            traffic_growth_rate=0.08,
            indexation_rate=1.0,
        )
        decision = self.governor.evaluate_active_pipeline(niche, metrics)
        self.assertEqual(decision.action, LifecycleAction.PIVOT)
        self.assertIn("Audience interest is healthy", decision.rationale)

    def test_active_pipeline_wind_down_traffic_decay(self):
        niche = Niche(id="niche-decay", name="Outdated Framework", description="Testing", vertical="Tech")
        metrics = PerformanceMetrics(
            total_pieces_published=6,
            monthly_impressions=1000,
            monthly_clicks=40,
            avg_dwell_time_seconds=25.0,
            conversions=0,
            total_cost=360.0,
            total_revenue=0.0,
            traffic_growth_rate=-0.40,  # Collapsing search interest (-40%)
            indexation_rate=0.9,
        )
        decision = self.governor.evaluate_active_pipeline(niche, metrics)
        self.assertEqual(decision.action, LifecycleAction.WIND_DOWN)
        self.assertIn("Traffic collapse", decision.rationale)

    def test_active_pipeline_wind_down_indexation_failure(self):
        niche = Niche(id="niche-penalty", name="Spammy Keyword", description="Testing", vertical="Tech")
        metrics = PerformanceMetrics(
            total_pieces_published=6,
            monthly_impressions=500,
            monthly_clicks=10,
            avg_dwell_time_seconds=15.0,
            conversions=0,
            total_cost=360.0,
            total_revenue=0.0,
            traffic_growth_rate=-0.05,
            indexation_rate=0.30,       # Severe de-indexing penalty (30% indexation)
        )
        decision = self.governor.evaluate_active_pipeline(niche, metrics)
        self.assertEqual(decision.action, LifecycleAction.WIND_DOWN)
        self.assertIn("Indexation rate", decision.rationale)


if __name__ == "__main__":
    unittest.main()
