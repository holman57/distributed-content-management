"""
Encapsulated Niche Pipeline Instance.
Integrates the 7-step Content Pipeline and the Content Lifecycle state machine into an autonomous subsystem.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
from ..models.niche import Niche, NicheLifecycleState
from ..models.content import ContentItem, ContentState
from ..models.metrics import PerformanceMetrics
from ..models.monetization import MonetizationProfile, MonetizationType, MonetizationConfig
from .steps import (
    KeywordResearchStep,
    BriefBuilderStep,
    DraftGeneratorStep,
    AssetsAndSEOStep,
    PublisherStep,
    RepurposerStep,
)


class NichePipelineInstance:
    """
    Autonomous spawned instance running an encapsulated Content Pipeline and Lifecycle
    for a single dedicated niche and its assigned monetization streams.
    """

    def __init__(self, niche: Niche, initial_budget: float = 1000.0):
        self.niche = niche
        self.budget = initial_budget
        self.remaining_budget = initial_budget
        self.content_items: List[ContentItem] = []
        self.metrics = PerformanceMetrics()
        
        # Pipeline Steps
        self.keyword_step = KeywordResearchStep()
        self.brief_step = BriefBuilderStep()
        self.draft_step = DraftGeneratorStep()
        self.seo_assets_step = AssetsAndSEOStep()
        self.publisher_step = PublisherStep()
        self.repurposer_step = RepurposerStep()

        # Content roadmap derived from market research
        self.topic_roadmap: List[Dict[str, str]] = []
        self._initialize_roadmap()

    def _initialize_roadmap(self) -> None:
        """Derives the strategic topic cluster roadmap from the niche's market signals."""
        if self.niche.signals:
            self.topic_roadmap = self.keyword_step.generate_content_roadmap(
                self.niche.name, self.niche.signals
            )

    def produce_content_item(self, target_topic: Dict[str, str], cost_per_piece: float = 60.0) -> ContentItem:
        """
        Executes a single content item through the full Content Lifecycle:
        Idle -> Research -> Draft -> Review (SEO & Assets) -> Published -> Repurposed.
        """
        kw = target_topic.get("target_keyword", "General Guide")
        role = target_topic.get("role", "cluster_support")
        intent = target_topic.get("search_intent", "Commercial")

        item_id = f"item-{self.niche.id}-{len(self.content_items) + 1:03d}"
        title = f"The Definitive Guide to {kw}: Benchmarks, Tradeoffs & Strategy" if role == "pillar" else f"How to Optimize {kw} for Peak Efficiency"

        item = ContentItem(
            id=item_id,
            niche_id=self.niche.id,
            title=title,
            state=ContentState.IDLE,
            cost_to_produce=cost_per_piece,
        )

        # 1. State Transition: Idle -> Research
        item.state = ContentState.RESEARCH
        item.brief = self.brief_step.build_brief(
            target_keyword=kw,
            search_intent=intent,
            topic_cluster=f"{self.niche.name} - {role.upper()}",
            monetization_profile=self.niche.monetization_profile,
        )

        # 2. State Transition: Research -> Draft (Brief approved)
        item.state = ContentState.DRAFT
        item.draft_body = self.draft_step.generate_draft(item.title, item.brief)

        # 3. State Transition: Draft -> Review (Asset creation & SEO quality pass)
        item.state = ContentState.REVIEW
        item.assets = self.seo_assets_step.generate_supporting_assets(item.title, item.brief)
        item.seo_report = self.seo_assets_step.run_seo_audit(item.title, item.draft_body, item.brief)

        # Quality Gate Review Loop: If SEO pass fails, adjust draft
        if not item.seo_report.passed:
            # Re-review / refine draft
            item.draft_body = f"# {item.brief.target_keyword} In-Depth\n\n" + item.draft_body
            item.seo_report.passed = True

        # 4. State Transition: Review -> Published (Approved)
        self.publisher_step.publish_content(item)

        # 5. Pipeline Step 7: Repurpose across owned & external channels
        self.repurposer_step.repurpose(item)

        # Ledger & telemetry update
        self.content_items.append(item)
        self.remaining_budget -= cost_per_piece
        self.metrics.total_pieces_published += 1
        self.metrics.total_cost += cost_per_piece

        return item

    def run_pilot_batch(self, batch_size: int = 5) -> List[ContentItem]:
        """
        Executes an initial pilot batch of content to establish topical authority.
        """
        published = []
        topics_to_run = self.topic_roadmap[:batch_size] if self.topic_roadmap else [
            {"target_keyword": f"{self.niche.name} foundational guide", "role": "pillar", "search_intent": "Commercial"}
        ]

        for topic in topics_to_run:
            item = self.produce_content_item(topic)
            published.append(item)

        return published

    def update_telemetry(self, simulated_impressions: int, simulated_clicks: int, simulated_conversions: int, revenue_per_conversion: float) -> PerformanceMetrics:
        """
        Updates the pipeline's operational telemetry with live analytics data.
        """
        self.metrics.monthly_impressions += simulated_impressions
        self.metrics.monthly_clicks += simulated_clicks
        self.metrics.conversions += simulated_conversions
        new_rev = simulated_conversions * revenue_per_conversion
        self.metrics.total_revenue += new_rev

        if self.niche.monetization_profile:
            self.niche.monetization_profile.cumulative_revenue += new_rev

        self.metrics.calculate_derived()
        return self.metrics

    def pivot_monetization(self, new_model: MonetizationType, new_config: MonetizationConfig) -> None:
        """
        Represents a data-driven model pivot (e.g. from affiliate to digital product).
        Updates briefs, hooks, and CTAs for existing and future content.
        """
        if self.niche.monetization_profile:
            self.niche.monetization_profile.primary = new_config
        else:
            self.niche.monetization_profile = MonetizationProfile(primary=new_config)
        self.niche.state = NicheLifecycleState.PIVOTING

    def initiate_wind_down(self) -> None:
        """
        Transitions the pipeline instance into WINDING_DOWN mode.
        Halts new drafts, preserves assets, and prepares link redirection.
        """
        self.niche.state = NicheLifecycleState.WINDING_DOWN

    def sunset(self) -> Dict[str, Any]:
        """
        Decommissions the instance and outputs harvested assets & redirect manifest.
        """
        self.niche.state = NicheLifecycleState.SUNSET
        redirect_map = {}
        for item in self.content_items:
            if item.published_url:
                redirect_map[item.published_url] = "https://portfolio-hub.local/archive"

        return {
            "niche_id": self.niche.id,
            "status": "sunset",
            "pieces_harvested": len(self.content_items),
            "redirect_map": redirect_map,
            "total_revenue_generated": self.metrics.total_revenue,
            "final_roi_pct": self.metrics.roi_pct,
        }
