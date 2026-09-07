"""
Algorithmic Opportunity Scorer and ROI projection engine.
"""

import math
from typing import List
from ..models.niche import MarketSignal, OpportunityScore
from ..models.monetization import MonetizationType
from .analyzer import MarketFeasibilityAnalyzer


class OpportunityScorer:
    """
    Computes rigorous, data-driven opportunity indices and financial projections for candidate niches.
    """

    def score_niche(self, niche_name: str, signals: List[MarketSignal]) -> OpportunityScore:
        """
        Calculates composite opportunity score (0 - 100) and projected ROI for a niche.
        """
        if not signals:
            return OpportunityScore(
                composite_score=0.0,
                demand_index=0.0,
                intent_index=0.0,
                competition_barrier=100.0,
                projected_roi_pct=0.0,
                recommended_monetization=MonetizationType.AFFILIATE,
                confidence=0.0,
                thesis_notes=["Insufficient market signals to evaluate niche."],
            )

        # 1. Compute aggregate signal metrics
        total_volume = sum(s.monthly_search_volume for s in signals)
        avg_growth = sum(s.trend_growth_pct for s in signals) / len(signals)
        avg_cpc = sum(s.average_cpc for s in signals) / len(signals)
        avg_intent = sum(s.buyer_intent_ratio for s in signals) / len(signals)
        avg_pain = sum(s.sentiment_pain_density for s in signals) / len(signals)
        avg_difficulty = sum(s.difficulty_score for s in signals) / len(signals)
        avg_da = sum(s.competition_da_avg for s in signals) / len(signals)

        # 2. Demand Index (0 - 100): Volume + Growth Velocity
        volume_norm = min(100.0, max(10.0, (math.log10(max(100, total_volume)) / 5.0) * 100.0))
        growth_multiplier = max(0.5, min(2.0, 1.0 + avg_growth))
        demand_index = min(100.0, volume_norm * growth_multiplier)

        # 3. Intent & Monetizability Index (0 - 100)
        cpc_norm = min(100.0, (avg_cpc / 6.0) * 100.0)
        intent_index = (avg_intent * 60.0) + (cpc_norm * 0.40)

        # 4. Competition Barrier (0 - 100)
        da_norm = min(100.0, avg_da)
        competition_barrier = (avg_difficulty * 60.0) + (da_norm * 0.40)

        # 5. Determine recommended monetization model and benchmarks
        rec_model, config = MarketFeasibilityAnalyzer.select_best_monetization_model(signals)

        # 6. Financial Simulation (Pilot unit economics: 5 pillar pieces @ $60 compute/editorial cost = $300)
        pilot_batch_size = 5
        cost_per_piece = 60.0
        total_pilot_cost = pilot_batch_size * cost_per_piece

        # Estimate organic capture across topic cluster: 10% - 18% of aggregate search volume
        capture_rate = min(0.20, max(0.08, 0.08 * (len(signals) ** 0.5)))
        estimated_monthly_traffic = total_volume * capture_rate

        # Effective RPM considering affiliate/lead bounty conversion or standard RPM
        effective_rpm = max(
            config.target_rpm,
            (config.avg_order_value_or_bounty * config.conversion_rate_benchmark * 1000.0 * 0.25)
        )
        estimated_monthly_revenue = (estimated_monthly_traffic / 1000.0) * effective_rpm
        annual_projected_revenue = estimated_monthly_revenue * 12.0

        projected_roi_pct = 0.0
        if total_pilot_cost > 0:
            net_first_year_profit = annual_projected_revenue - total_pilot_cost
            projected_roi_pct = (net_first_year_profit / total_pilot_cost) * 100.0

        # 7. Composite Opportunity Score (0 - 100)
        numerator = (demand_index * 0.35) + (intent_index * 0.40) + (avg_pain * 25.0)
        denominator = 1.0 + (competition_barrier / 100.0) * 0.5
        composite_score = round(max(0.0, min(100.0, numerator / denominator)), 1)

        # 8. Investment Thesis Notes
        thesis = []
        if avg_growth > 0.25:
            thesis.append(f"Accelerating trend velocity: +{avg_growth*100:.1f}% recent growth")
        if avg_intent > 0.65:
            thesis.append("High buyer-intent concentration with commercial search syntax")
        if competition_barrier < 45.0:
            thesis.append(f"Low competition barrier (DA ~{avg_da:.0f}), fast indexation expected")
        else:
            thesis.append(f"Established SERP authority required (DA ~{avg_da:.0f})")
        thesis.append(f"Optimal vehicle: {rec_model.value.upper()} (Target RPM: ${effective_rpm:.2f})")

        return OpportunityScore(
            composite_score=composite_score,
            demand_index=round(demand_index, 1),
            intent_index=round(intent_index, 1),
            competition_barrier=round(competition_barrier, 1),
            projected_roi_pct=round(projected_roi_pct, 1),
            recommended_monetization=rec_model,
            confidence=0.88,
            thesis_notes=thesis,
        )
