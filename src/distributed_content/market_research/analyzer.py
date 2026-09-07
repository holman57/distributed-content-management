"""
Competitor and monetization feasibility analysis.
"""

from typing import List, Tuple
from ..models.niche import MarketSignal
from ..models.monetization import MonetizationType, MonetizationConfig


class MarketFeasibilityAnalyzer:
    """
    Evaluates market signals to determine optimal monetization alignment and competitive entry barriers.
    """

    @staticmethod
    def select_best_monetization_model(signals: List[MarketSignal]) -> Tuple[MonetizationType, MonetizationConfig]:
        """
        Determines the most lucrative monetization vehicle based on search intent, volume, and CPC.
        """
        if not signals:
            return MonetizationType.AFFILIATE, MonetizationConfig(
                model_type=MonetizationType.AFFILIATE,
                target_rpm=25.0,
                avg_order_value_or_bounty=40.0,
                conversion_rate_benchmark=0.02,
                minimum_monthly_volume=1000,
                description="Default affiliate baseline",
            )

        avg_cpc = sum(s.average_cpc for s in signals) / len(signals)
        avg_intent = sum(s.buyer_intent_ratio for s in signals) / len(signals)
        avg_pain = sum(s.sentiment_pain_density for s in signals) / len(signals)
        total_vol = sum(s.monthly_search_volume for s in signals)

        # 1. B2B / High-ticket Lead Generation
        if avg_cpc > 4.50 and avg_intent > 0.65:
            return MonetizationType.LEAD_GENERATION, MonetizationConfig(
                model_type=MonetizationType.LEAD_GENERATION,
                target_rpm=95.0,
                avg_order_value_or_bounty=150.0,
                conversion_rate_benchmark=0.015,
                minimum_monthly_volume=1500,
                description="B2B Qualified Lead Capture & Agency Referrals",
            )

        # 2. Digital Products / Problem-Solving Toolkits
        if avg_pain > 0.70 and avg_intent > 0.50:
            return MonetizationType.DIGITAL_PRODUCT, MonetizationConfig(
                model_type=MonetizationType.DIGITAL_PRODUCT,
                target_rpm=60.0,
                avg_order_value_or_bounty=49.0,
                conversion_rate_benchmark=0.025,
                minimum_monthly_volume=2000,
                description="Self-serve downloadable guides, templates, and boilerplates",
            )

        # 3. Affiliate / SaaS & Tech Product Comparisons
        if avg_intent > 0.60 or avg_cpc > 2.00:
            return MonetizationType.AFFILIATE, MonetizationConfig(
                model_type=MonetizationType.AFFILIATE,
                target_rpm=35.0,
                avg_order_value_or_bounty=65.0,
                conversion_rate_benchmark=0.02,
                minimum_monthly_volume=2500,
                description="Affiliate commissions via reviews and 'best-of' roundups",
            )

        # 4. Programmatic Ads (High volume, general consumer)
        if total_vol > 50000:
            return MonetizationType.PROGRAMMATIC_ADS, MonetizationConfig(
                model_type=MonetizationType.PROGRAMMATIC_ADS,
                target_rpm=18.0,
                avg_order_value_or_bounty=0.0,
                conversion_rate_benchmark=1.0,
                minimum_monthly_volume=10000,
                description="Display network and premium ad exchange monetization",
            )

        # 5. Newsletter & Community Subscriptions
        return MonetizationType.NEWSLETTER_SUB, MonetizationConfig(
            model_type=MonetizationType.NEWSLETTER_SUB,
            target_rpm=30.0,
            avg_order_value_or_bounty=10.0,
            conversion_rate_benchmark=0.03,
            minimum_monthly_volume=1500,
            description="Owned audience newsletter sponsorships and premium tier",
        )

    @staticmethod
    def evaluate_competitor_vulnerability(signals: List[MarketSignal]) -> float:
        """
        Calculates a 0.0 - 1.0 vulnerability score for ranking competitors.
        Higher score means competitors are more easily displaced (lower DA, outdated coverage).
        """
        if not signals:
            return 0.5
        avg_da = sum(s.competition_da_avg for s in signals) / len(signals)
        avg_difficulty = sum(s.difficulty_score for s in signals) / len(signals)

        # If average DA is < 40 and difficulty is < 0.4, vulnerability is high (~0.8)
        barrier = (avg_da / 100.0) * 0.6 + avg_difficulty * 0.4
        vulnerability = max(0.0, min(1.0, 1.0 - barrier))
        return vulnerability
