"""
Tests for encapsulated NichePipelineInstance execution and content lifecycle transitions.
"""

import unittest
from src.distributed_content.models import (
    Niche,
    NicheLifecycleState,
    MarketSignal,
    ContentState,
    MonetizationType,
    MonetizationConfig,
    MonetizationProfile,
)
from src.distributed_content.pipeline import NichePipelineInstance


class TestPipelineInstance(unittest.TestCase):

    def setUp(self):
        self.signal = MarketSignal(
            keyword="best self-hosted cloud storage",
            monthly_search_volume=5000,
            trend_growth_pct=0.30,
            average_cpc=2.50,
            buyer_intent_ratio=0.80,
            difficulty_score=0.45,
            competition_da_avg=42.0,
            sentiment_pain_density=0.65,
        )
        self.niche = Niche(
            id="niche-storage",
            name="Self-Hosted Storage",
            description="Private personal cloud infrastructure",
            vertical="DevOps & Privacy",
            signals=[self.signal],
            state=NicheLifecycleState.INCUBATING,
            monetization_profile=MonetizationProfile(
                primary=MonetizationConfig(
                    model_type=MonetizationType.AFFILIATE,
                    target_rpm=35.0,
                    avg_order_value_or_bounty=50.0,
                    conversion_rate_benchmark=0.02,
                    minimum_monthly_volume=1000,
                )
            )
        )
        self.instance = NichePipelineInstance(niche=self.niche, initial_budget=600.0)

    def test_pipeline_executes_full_lifecycle(self):
        target_topic = {
            "target_keyword": "best self-hosted cloud storage",
            "role": "pillar",
            "search_intent": "Commercial",
        }
        item = self.instance.produce_content_item(target_topic, cost_per_piece=60.0)

        # Verify Content Item Lifecycle State reached REPURPOSED
        self.assertEqual(item.state, ContentState.REPURPOSED)
        self.assertIsNotNone(item.brief)
        self.assertIn("best self-hosted cloud storage", item.draft_body.lower())
        self.assertTrue(len(item.assets) >= 2)
        self.assertIsNotNone(item.seo_report)
        self.assertTrue(item.seo_report.passed)
        self.assertIsNotNone(item.published_url)
        self.assertTrue(len(item.repurposed_items) >= 2)

        # Verify instance ledger and budget decrement
        self.assertEqual(len(self.instance.content_items), 1)
        self.assertEqual(self.instance.remaining_budget, 540.0)
        self.assertEqual(self.instance.metrics.total_pieces_published, 1)

    def test_run_pilot_batch(self):
        items = self.instance.run_pilot_batch(batch_size=1)
        self.assertEqual(len(items), 1)
        self.assertEqual(self.instance.metrics.total_pieces_published, 1)

    def test_telemetry_and_sunset(self):
        self.instance.run_pilot_batch(batch_size=1)
        self.instance.update_telemetry(
            simulated_impressions=5000,
            simulated_clicks=150,
            simulated_conversions=5,
            revenue_per_conversion=50.0,
        )
        self.assertEqual(self.instance.metrics.monthly_clicks, 150)
        self.assertEqual(self.instance.metrics.total_revenue, 250.0)
        self.assertGreater(self.instance.metrics.roi_pct, 0.0)

        manifest = self.instance.sunset()
        self.assertEqual(self.instance.niche.state, NicheLifecycleState.SUNSET)
        self.assertEqual(manifest["status"], "sunset")
        self.assertIn("redirect_map", manifest)


if __name__ == "__main__":
    unittest.main()
