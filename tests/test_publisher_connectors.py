import sys
import unittest
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from distributed_content.publisher_connectors import (
    GrowthTelemetryTracker,
    MarkdownArticle,
    SubstackConnector,
    WordPressConnector,
)


class TestPublisherConnectors(unittest.TestCase):

    def setUp(self):
        self.article = MarkdownArticle(
            title="Agentic Coding Workflows in 2026",
            niche="AI Development",
            body_markdown="Autonomous paired programming transforms developer productivity through self-steering loops.",
            keywords=["AI", "Agents", "Productivity"],
            monetization_cta="Subscribe to our technical deep dives.",
        )

    def test_markdown_article_frontmatter_and_reading_time(self):
        md = self.article.to_full_markdown()
        self.assertIn('title: "Agentic Coding Workflows in 2026"', md)
        self.assertIn('niche: "AI Development"', md)
        self.assertIn('reading_time_minutes: 1', md)
        self.assertIn("Subscribe to our technical deep dives.", md)

    def test_wordpress_connector_payload(self):
        wp = WordPressConnector()
        res = wp.publish(self.article, as_draft=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["payload"]["status"], "draft")
        self.assertEqual(res["payload"]["title"], self.article.title)

    def test_substack_connector(self):
        ss = SubstackConnector()
        res = ss.format_newsletter(self.article)
        self.assertEqual(res["title"], self.article.title)
        self.assertIn("AI Development", res["subtitle"])
        self.assertEqual(res["call_to_action"], self.article.monetization_cta)

    def test_growth_telemetry_velocity(self):
        tracker = GrowthTelemetryTracker()
        snap1 = tracker.record_snapshot("holman57/Adrastea", stars=10, forks=2, watchers=5)
        # Advance time by 86400s (1 day) and add 5 stars
        snap1["timestamp"] -= 86400.0
        tracker.record_snapshot("holman57/Adrastea", stars=15, forks=3, watchers=6)

        vel = tracker.calculate_velocity("holman57/Adrastea")
        self.assertEqual(vel["star_delta"], 5)
        self.assertEqual(vel["status"], "accelerating")
        self.assertGreaterEqual(vel["stars_per_day"], 4.5)


if __name__ == "__main__":
    unittest.main()
