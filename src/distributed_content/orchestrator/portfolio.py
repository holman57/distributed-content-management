"""
Portfolio Manager for multi-stream monetization diversification and capital allocation.
"""

from typing import Dict, List, Any
from ..pipeline.instance import NichePipelineInstance
from ..models.monetization import MonetizationType


class PortfolioManager:
    """
    Supervises portfolio-level capital allocation and monetization stream diversification.
    Ensures the business is not over-exposed to any single monetization model or platform risk.
    """

    def __init__(self, total_capital_pool: float = 10000.0):
        self.total_capital_pool = total_capital_pool
        self.allocated_capital: float = 0.0

    @property
    def unallocated_capital(self) -> float:
        return max(0.0, self.total_capital_pool - self.allocated_capital)

    def allocate_budget_to_niche(self, amount: float) -> bool:
        """Allocates budget from capital pool to a new or scaling niche."""
        if amount <= self.unallocated_capital:
            self.allocated_capital += amount
            return True
        return False

    def reclaim_capital(self, amount: float) -> None:
        """Returns unused or harvested capital from a winding-down niche to the pool."""
        self.allocated_capital = max(0.0, self.allocated_capital - amount)

    def compute_monetization_diversification(self, instances: List[NichePipelineInstance]) -> Dict[str, Any]:
        """
        Analyzes the distribution of active niches and revenue across different monetization models.
        """
        counts: Dict[str, int] = {}
        revenue_by_stream: Dict[str, float] = {}

        for inst in instances:
            mtype = (
                inst.niche.monetization_profile.primary.model_type.value
                if inst.niche.monetization_profile
                else "unassigned"
            )
            counts[mtype] = counts.get(mtype, 0) + 1
            rev = inst.metrics.total_revenue
            revenue_by_stream[mtype] = revenue_by_stream.get(mtype, 0.0) + rev

        total_active = len(instances)
        stream_shares = {
            k: (v / total_active * 100.0) if total_active > 0 else 0.0
            for k, v in counts.items()
        }

        # Check for over-concentration risk (>50% dependent on single model)
        concentration_warning = None
        for stream, share in stream_shares.items():
            if share > 50.0:
                concentration_warning = f"High portfolio concentration in {stream.upper()} ({share:.1f}% of active niches)."

        return {
            "niche_counts_by_stream": counts,
            "revenue_by_stream": revenue_by_stream,
            "percentage_share": stream_shares,
            "concentration_warning": concentration_warning,
            "total_active_pipelines": total_active,
        }
