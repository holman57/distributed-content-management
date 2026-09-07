"""
Tests for MetaOrchestrator multi-niche discovery, spawning, and portfolio governance.
"""

import unittest
from src.distributed_content.orchestrator import MetaOrchestrator
from src.distributed_content.models import NicheLifecycleState, LifecycleAction


class TestOrchestrator(unittest.TestCase):

    def setUp(self):
        self.orchestrator = MetaOrchestrator()

    def test_multi_niche_spawning_and_lifecycle_governance(self):
        # 1. Discover high-potential B2B niche (High intent, high CPC)
        niche_b2b = self.orchestrator.discover_niche(
            niche_id="niche-b2b-agents",
            name="AI Developer Agents",
            vertical="Enterprise DevTools",
            seed_keywords=[
                "best enterprise ai coding agent comparison",
                "ai code review tool pricing",
                "b2b autonomous coding platform review",
            ]
        )
        self.assertEqual(niche_b2b.state, NicheLifecycleState.CANDIDATE)

        # 2. Spawn pipeline instance for qualifying niche
        instance_b2b = self.orchestrator.spawn_pipeline_instance(niche_b2b, initial_budget=600.0)
        self.assertIsNotNone(instance_b2b)
        self.assertEqual(niche_b2b.state, NicheLifecycleState.INCUBATING)
        self.assertGreater(instance_b2b.metrics.total_pieces_published, 0)

        # 3. Simulate high-converting breakout performance
        instance_b2b.update_telemetry(
            simulated_impressions=20000,
            simulated_clicks=1000,
            simulated_conversions=25,
            revenue_per_conversion=120.0, # $3,000 revenue
        )
        instance_b2b.metrics.traffic_growth_rate = 0.35

        # 4. Discover and spawn a decaying niche
        niche_decay = self.orchestrator.discover_niche(
            niche_id="niche-fading-trend",
            name="Deprecated Framework Plugins",
            vertical="Legacy Tech",
            seed_keywords=["best framework v1 plugins", "framework v1 migration tool"]
        )
        instance_decay = self.orchestrator.spawn_pipeline_instance(niche_decay, initial_budget=600.0)
        self.assertIsNotNone(instance_decay)

        # Simulate collapsing traffic and zero conversions on the decaying niche
        instance_decay.metrics.total_pieces_published = 5
        instance_decay.metrics.monthly_impressions = 400
        instance_decay.metrics.monthly_clicks = 12
        instance_decay.metrics.traffic_growth_rate = -0.35
        instance_decay.metrics.conversions = 0
        instance_decay.metrics.total_revenue = 0.0

        # 5. Run higher-order portfolio governance
        decisions = self.orchestrator.evaluate_and_govern_active_pipelines()
        self.assertEqual(len(decisions), 2)

        decision_map = {d.niche_id: d.action for d in decisions}
        self.assertEqual(decision_map["niche-b2b-agents"], LifecycleAction.SCALE)
        self.assertEqual(decision_map["niche-fading-trend"], LifecycleAction.WIND_DOWN)

        # Check that B2B niche was promoted to SCALED
        self.assertEqual(niche_b2b.state, NicheLifecycleState.SCALED)
        # Check that decaying niche was set to WINDING_DOWN
        self.assertEqual(niche_decay.state, NicheLifecycleState.WINDING_DOWN)

        # 6. Check portfolio summary & diversification
        summary = self.orchestrator.get_portfolio_summary()
        self.assertGreater(summary["total_revenue"], 2500.0)
        self.assertGreater(summary["blended_roi_pct"], 100.0)
        self.assertIn("diversification", summary)


if __name__ == "__main__":
    unittest.main()
