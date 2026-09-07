"""
Lifecycle Governor for data-driven spin-up, scale, pivot, and wind-down decisions.
"""

from typing import Optional
from ..models.niche import Niche, NicheLifecycleState
from ..models.metrics import PerformanceMetrics, LifecycleAction, LifecycleDecision
from .rules import GovernanceThresholds


class LifecycleGovernor:
    """
    Autonomous decision engine governing the lifecycle of niche content pipelines.
    Evaluates market signals and operational telemetry against rigorous economic hurdles.
    """

    def __init__(self, thresholds: Optional[GovernanceThresholds] = None):
        self.thresholds = thresholds or GovernanceThresholds()

    def evaluate_candidate(self, niche: Niche) -> LifecycleDecision:
        """
        Determines whether a researched niche qualifies for pipeline spin-up.
        """
        if not niche.opportunity_score:
            return LifecycleDecision(
                action=LifecycleAction.HOLD,
                niche_id=niche.id,
                rationale="Candidate lacks complete market research opportunity score.",
                confidence=0.5,
                evaluation_metrics={},
            )

        score = niche.opportunity_score.composite_score
        roi = niche.opportunity_score.projected_roi_pct
        intent = niche.opportunity_score.intent_index

        metrics = {
            "composite_score": score,
            "projected_roi_pct": roi,
            "intent_index": intent,
            "score_hurdle": self.thresholds.spin_up_min_opportunity_score,
            "roi_hurdle": self.thresholds.spin_up_min_projected_roi,
        }

        if (
            score >= self.thresholds.spin_up_min_opportunity_score
            and roi >= self.thresholds.spin_up_min_projected_roi
        ):
            return LifecycleDecision(
                action=LifecycleAction.SPIN_UP,
                niche_id=niche.id,
                rationale=(
                    f"Approved for spin-up. Opportunity score ({score}) and projected ROI "
                    f"({roi}%) cleared hurdle rates ({self.thresholds.spin_up_min_opportunity_score} score, "
                    f"{self.thresholds.spin_up_min_projected_roi}% ROI)."
                ),
                confidence=0.92,
                evaluation_metrics=metrics,
            )

        return LifecycleDecision(
            action=LifecycleAction.HOLD,
            niche_id=niche.id,
            rationale=(
                f"Candidate did not clear spin-up hurdles. Composite score {score} vs "
                f"{self.thresholds.spin_up_min_opportunity_score}, ROI {roi}% vs "
                f"{self.thresholds.spin_up_min_projected_roi}%."
            ),
            confidence=0.85,
            evaluation_metrics=metrics,
        )

    def evaluate_active_pipeline(self, niche: Niche, metrics: PerformanceMetrics) -> LifecycleDecision:
        """
        Monitors active telemetry to decide whether to scale, pivot, maintain, or wind down the niche pipeline.
        """
        metrics.calculate_derived()
        eval_data = {
            "published_pieces": metrics.total_pieces_published,
            "monthly_clicks": metrics.monthly_clicks,
            "ctr": round(metrics.ctr, 4),
            "conversion_rate": round(metrics.conversion_rate, 4),
            "roi_pct": round(metrics.roi_pct, 2),
            "growth_rate": round(metrics.traffic_growth_rate, 2),
            "indexation_rate": round(metrics.indexation_rate, 2),
            "dwell_time": round(metrics.avg_dwell_time_seconds, 1),
        }

        # 1. Check for WIND_DOWN triggers first (Capital preservation & risk mitigation)
        if metrics.total_pieces_published >= self.thresholds.wind_down_min_runway_pieces:
            # Check 1a: Severe indexation penalty (Google sandbox or algorithmic block)
            if metrics.indexation_rate < self.thresholds.wind_down_min_indexation_rate:
                return LifecycleDecision(
                    action=LifecycleAction.WIND_DOWN,
                    niche_id=niche.id,
                    rationale=(
                        f"Indexation rate ({metrics.indexation_rate*100:.1f}%) fell below floor "
                        f"({self.thresholds.wind_down_min_indexation_rate*100:.1f}%). Triggering wind-down "
                        "due to search engine distribution penalty."
                    ),
                    confidence=0.95,
                    evaluation_metrics=eval_data,
                )

            # Check 1b: Traffic collapse and negative ROI
            if (
                metrics.traffic_growth_rate <= self.thresholds.wind_down_traffic_decay_rate
                and metrics.roi_pct <= self.thresholds.wind_down_max_roi
            ):
                return LifecycleDecision(
                    action=LifecycleAction.WIND_DOWN,
                    niche_id=niche.id,
                    rationale=(
                        f"Traffic collapse ({metrics.traffic_growth_rate*100:.1f}%) combined with negative ROI "
                        f"({metrics.roi_pct:.1f}%) breached exit threshold. De-escalating pipeline."
                    ),
                    confidence=0.94,
                    evaluation_metrics=eval_data,
                )

            # Check 1c: Chronic unprofitability past pilot phase
            if metrics.roi_pct <= -50.0 and metrics.monthly_clicks < 200:
                return LifecycleDecision(
                    action=LifecycleAction.WIND_DOWN,
                    niche_id=niche.id,
                    rationale=(
                        f"Deeply unprofitable unit economics (ROI {metrics.roi_pct:.1f}%) with sub-target "
                        f"click volume ({metrics.monthly_clicks} clicks). Triggering wind-down."
                    ),
                    confidence=0.90,
                    evaluation_metrics=eval_data,
                )

        # 2. Check for PIVOT triggers (Audience interest exists, but monetization conversion failed)
        if (
            metrics.monthly_clicks >= self.thresholds.pivot_min_traffic_volume
            and metrics.avg_dwell_time_seconds >= self.thresholds.pivot_min_dwell_time
            and metrics.conversion_rate < self.thresholds.pivot_max_conversion_rate
        ):
            return LifecycleDecision(
                action=LifecycleAction.PIVOT,
                niche_id=niche.id,
                rationale=(
                    f"Audience interest is healthy ({metrics.monthly_clicks} clicks, {metrics.avg_dwell_time_seconds}s "
                    f"dwell time) but conversion rate ({metrics.conversion_rate*100:.2f}%) is below hurdle "
                    f"({self.thresholds.pivot_max_conversion_rate*100:.2f}%). Recommending monetization model pivot."
                ),
                confidence=0.88,
                evaluation_metrics=eval_data,
            )

        # 3. Check for SCALE triggers (Proven unit economics ready for capital acceleration)
        if (
            metrics.total_pieces_published >= self.thresholds.scale_min_published_pieces
            and metrics.roi_pct >= self.thresholds.scale_min_roi
            and metrics.ctr >= self.thresholds.scale_min_ctr
            and metrics.conversion_rate >= self.thresholds.scale_min_conversion_rate
            and metrics.traffic_growth_rate >= self.thresholds.scale_min_traffic_growth_rate
        ):
            return LifecycleDecision(
                action=LifecycleAction.SCALE,
                niche_id=niche.id,
                rationale=(
                    f"Unit economics validated for scale: ROI {metrics.roi_pct:.1f}% >= "
                    f"{self.thresholds.scale_min_roi}%, CTR {metrics.ctr*100:.2f}%, and MoM growth "
                    f"+{metrics.traffic_growth_rate*100:.1f}%. Increasing publishing velocity."
                ),
                confidence=0.96,
                evaluation_metrics=eval_data,
            )

        # 4. Default: HOLD current operations
        return LifecycleDecision(
            action=LifecycleAction.HOLD,
            niche_id=niche.id,
            rationale="Pipeline metrics within standard operational tolerances. Maintaining cadence.",
            confidence=0.80,
            evaluation_metrics=eval_data,
        )
