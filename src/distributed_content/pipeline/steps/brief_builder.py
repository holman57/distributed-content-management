"""
Content Pipeline Step 2: Strategic Content Brief Generation.
"""

from typing import List, Optional
from ...models.content import ContentBrief
from ...models.monetization import MonetizationProfile, MonetizationType


class BriefBuilderStep:
    """
    Synthesizes competitive gaps, search intent, and monetization hooks into an actionable Content Brief.
    """

    def build_brief(
        self,
        target_keyword: str,
        search_intent: str,
        topic_cluster: str,
        monetization_profile: Optional[MonetizationProfile] = None,
        custom_pain_points: Optional[List[str]] = None,
        custom_competitor_gaps: Optional[List[str]] = None,
    ) -> ContentBrief:
        """
        Creates a structured ContentBrief with audience pain points and monetization hooks.
        """
        pain_points = custom_pain_points or [
            f"Overwhelmed by conflicting advice regarding {target_keyword}",
            "Lacks clear benchmarks or direct cost comparisons",
            "Fear of vendor lock-in or fragile configurations",
        ]

        competitor_gaps = custom_competitor_gaps or [
            "Incumbent articles contain outdated 2023 pricing and deprecated APIs",
            "Superficial overview lacking practical step-by-step setup guides",
            "Missing real-world performance benchmarks and teardowns",
        ]

        # Configure CTA and monetization hook based on monetization profile
        cta = "Subscribe to our weekly intelligence dispatch for in-depth teardowns."
        monetization_hook = "Contextual recommendation with curated vendor alternatives."

        if monetization_profile:
            mtype = monetization_profile.primary.model_type
            if mtype == MonetizationType.AFFILIATE:
                monetization_hook = f"Affiliate comparison matrix highlighting top-rated solution for '{target_keyword}'."
                cta = "Check current discount pricing via our vetted partner links."
            elif mtype == MonetizationType.DIGITAL_PRODUCT:
                monetization_hook = f"Downloadable production checklist and configuration boilerplate for '{target_keyword}'."
                cta = "Download the complete production-ready toolkit ($49)."
            elif mtype == MonetizationType.LEAD_GENERATION:
                monetization_hook = f"Complimentary architecture audit & quote estimation for enterprise '{target_keyword}'."
                cta = "Schedule a 15-minute diagnostic call with our engineering leads."
            elif mtype == MonetizationType.NEWSLETTER_SUB:
                monetization_hook = f"Exclusive deep-dive teardowns on '{target_keyword}' delivered bi-weekly."
                cta = "Join 12,000+ practitioners on our free Substack newsletter."
            elif mtype == MonetizationType.PROGRAMMATIC_ADS:
                monetization_hook = "High-dwell time interactive guide with media asset breaks."
                cta = "Bookmark this comprehensive resource and explore related guides."

        return ContentBrief(
            target_keyword=target_keyword,
            search_intent=search_intent,
            topic_cluster=topic_cluster,
            target_audience_pain_points=pain_points,
            competitor_gaps_to_exploit=competitor_gaps,
            call_to_action=cta,
            monetization_hook=monetization_hook,
        )
