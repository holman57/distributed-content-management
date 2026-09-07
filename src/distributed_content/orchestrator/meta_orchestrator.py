"""
Higher-Order Meta-Orchestrator: The System of Spawning Systems.
Coordinates autonomous niche discovery, lifecycle governance, and multi-stream portfolio management.
"""

from typing import List, Dict, Any, Optional
from ..models.niche import Niche, NicheLifecycleState
from ..models.monetization import MonetizationProfile
from ..models.metrics import LifecycleAction, LifecycleDecision
from ..market_research.signals import MarketSignalCollector
from ..market_research.scorer import OpportunityScorer
from ..market_research.analyzer import MarketFeasibilityAnalyzer
from ..decision_engine.governor import LifecycleGovernor
from ..pipeline.instance import NichePipelineInstance
from .registry import PipelineRegistry
from .portfolio import PortfolioManager


class MetaOrchestrator:
    """
    Higher-order portfolio engine that continuously discovers niches, spawns autonomous
    content pipeline subsystems, monitors their performance telemetry, and dynamically
    allocates capital or triggers spin-up / wind-down actions.
    """

    def __init__(
        self,
        signal_collector: Optional[MarketSignalCollector] = None,
        scorer: Optional[OpportunityScorer] = None,
        governor: Optional[LifecycleGovernor] = None,
        portfolio_manager: Optional[PortfolioManager] = None,
        registry: Optional[PipelineRegistry] = None,
    ):
        self.collector = signal_collector or MarketSignalCollector()
        self.scorer = scorer or OpportunityScorer()
        self.governor = governor or LifecycleGovernor()
        self.portfolio = portfolio_manager or PortfolioManager(total_capital_pool=15000.0)
        self.registry = registry or PipelineRegistry()
        self.candidates: Dict[str, Niche] = {}
        self.decision_history: List[LifecycleDecision] = []

    def discover_niche(self, niche_id: str, name: str, vertical: str, seed_keywords: List[str]) -> Niche:
        """
        Conducts autonomous market research across seed keywords, scoring demand, competition, and monetization.
        """
        signals = self.collector.collect_signals_for_niche(name, seed_keywords)
        opp_score = self.scorer.score_niche(name, signals)
        best_model, config = MarketFeasibilityAnalyzer.select_best_monetization_model(signals)

        profile = MonetizationProfile(primary=config)
        niche = Niche(
            id=niche_id,
            name=name,
            description=f"Automated niche pipeline for {name} ({vertical})",
            vertical=vertical,
            signals=signals,
            opportunity_score=opp_score,
            state=NicheLifecycleState.CANDIDATE if opp_score.composite_score >= 55.0 else NicheLifecycleState.DISCOVERY,
            monetization_profile=profile,
        )

        self.candidates[niche.id] = niche
        return niche

    def spawn_pipeline_instance(self, niche: Niche, initial_budget: float = 600.0) -> Optional[NichePipelineInstance]:
        """
        Evaluates the candidate against spin-up hurdle rates and spawns a new autonomous
        content pipeline subsystem if approved.
        """
        decision = self.governor.evaluate_candidate(niche)
        self.decision_history.append(decision)

        if decision.action != LifecycleAction.SPIN_UP:
            return None

        # Check portfolio capital allocation
        if not self.portfolio.allocate_budget_to_niche(initial_budget):
            decision.rationale += " [Blocked by portfolio capital limit]."
            return None

        # Instantiate encapsulated pipeline subsystem
        niche.state = NicheLifecycleState.INCUBATING
        niche.allocated_budget = initial_budget
        instance = NichePipelineInstance(niche=niche, initial_budget=initial_budget)

        # Register instance in the active subsystem directory
        self.registry.register(instance)

        # Run initial pilot batch to launch the content lifecycle
        instance.run_pilot_batch(batch_size=min(5, len(instance.topic_roadmap)))

        return instance

    def evaluate_and_govern_active_pipelines(self) -> List[LifecycleDecision]:
        """
        Iterates across all active spawned pipelines, evaluates their performance metrics,
        and executes data-driven scale, pivot, hold, or wind-down actions.
        """
        decisions: List[LifecycleDecision] = []

        for instance in self.registry.list_active():
            niche = instance.niche
            metrics = instance.metrics

            decision = self.governor.evaluate_active_pipeline(niche, metrics)
            decisions.append(decision)
            self.decision_history.append(decision)

            # Execute the decision
            if decision.action == LifecycleAction.SCALE:
                # Inject growth capital and double publishing velocity
                scale_capital = 1200.0
                if self.portfolio.allocate_budget_to_niche(scale_capital):
                    instance.budget += scale_capital
                    instance.remaining_budget += scale_capital
                    niche.state = NicheLifecycleState.SCALED
                    # Produce expanded cluster content
                    if len(instance.topic_roadmap) > len(instance.content_items):
                        remaining_topics = instance.topic_roadmap[len(instance.content_items):]
                        for topic in remaining_topics:
                            instance.produce_content_item(topic)

            elif decision.action == LifecycleAction.PIVOT:
                # Reposition monetization model (e.g., from low-converting affiliate to digital product)
                from ..models.monetization import MonetizationType, MonetizationConfig
                pivot_config = MonetizationConfig(
                    model_type=MonetizationType.DIGITAL_PRODUCT,
                    target_rpm=55.0,
                    avg_order_value_or_bounty=39.0,
                    conversion_rate_benchmark=0.03,
                    minimum_monthly_volume=1000,
                    description="Pivoted to owned digital template & guide",
                )
                instance.pivot_monetization(MonetizationType.DIGITAL_PRODUCT, pivot_config)

            elif decision.action == LifecycleAction.WIND_DOWN:
                # Halt production, reclaim remaining unspent capital, initiate link redirection
                unspent = max(0.0, instance.remaining_budget)
                self.portfolio.reclaim_capital(unspent)
                instance.initiate_wind_down()

        return decisions

    def sunset_pipeline(self, niche_id: str) -> Optional[Dict[str, Any]]:
        """
        Completes the wind-down protocol: permanently decommissions the instance and harvests assets.
        """
        instance = self.registry.get(niche_id)
        if not instance:
            return None
        return instance.sunset()

    def get_portfolio_summary(self) -> Dict[str, Any]:
        """
        Aggregates comprehensive portfolio health, monetization stream breakdown, and financial ROI.
        """
        all_instances = self.registry.list_all()
        total_pieces = sum(inst.metrics.total_pieces_published for inst in all_instances)
        total_impressions = sum(inst.metrics.monthly_impressions for inst in all_instances)
        total_clicks = sum(inst.metrics.monthly_clicks for inst in all_instances)
        total_revenue = sum(inst.metrics.total_revenue for inst in all_instances)
        total_cost = sum(inst.metrics.total_cost for inst in all_instances)
        net_profit = total_revenue - total_cost
        blended_roi = (net_profit / total_cost * 100.0) if total_cost > 0 else 0.0

        diversification = self.portfolio.compute_monetization_diversification(self.registry.list_active())

        state_counts = {}
        for inst in all_instances:
            st = inst.niche.state.value
            state_counts[st] = state_counts.get(st, 0) + 1

        return {
            "total_active_pipelines": len(self.registry.list_active()),
            "total_pieces_published": total_pieces,
            "monthly_impressions": total_impressions,
            "monthly_clicks": total_clicks,
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "net_profit": round(net_profit, 2),
            "blended_roi_pct": round(blended_roi, 1),
            "pipeline_states": state_counts,
            "diversification": diversification,
            "total_capital_pool": self.portfolio.total_capital_pool,
            "unallocated_capital": self.portfolio.unallocated_capital,
        }
