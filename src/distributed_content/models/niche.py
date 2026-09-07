"""
Niche and Market Signal data models for distributed content management.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from .monetization import MonetizationType, MonetizationProfile


class NicheLifecycleState(str, Enum):
    """
    Higher-order lifecycle states for an individual niche pipeline.
    """
    DISCOVERY = "discovery"          # Market research active, gathering signals
    CANDIDATE = "candidate"          # Scored and qualified for portfolio consideration
    INCUBATING = "incubating"        # Spun up with pilot batch (proving phase)
    SCALED = "scaled"                # Breakout performance, high publishing velocity
    PIVOTING = "pivoting"            # Restructuring monetization or content angle
    WINDING_DOWN = "winding_down"    # De-escalating production, harvesting evergreen value
    SUNSET = "sunset"                # Pipeline de-provisioned, links/leads archived


@dataclass
class MarketSignal:
    """
    Quantitative & qualitative indicators for a keyword or topic cluster.
    """
    keyword: str
    monthly_search_volume: int
    trend_growth_pct: float       # e.g., +0.45 for +45% YoY/90-day growth
    average_cpc: float            # Cost-per-click in USD (high cpc = high commercial intent)
    buyer_intent_ratio: float     # Ratio of commercial/transactional queries (0.0 - 1.0)
    difficulty_score: float       # SEO / SERP difficulty barrier (0.0 to 1.0)
    competition_da_avg: float     # Average Domain Authority of top 10 ranking sites
    sentiment_pain_density: float # Forum/Reddit problem/unmet need density (0.0 to 1.0)


@dataclass
class OpportunityScore:
    """
    Algorithmic evaluation of a niche's commercial viability and expected ROI.
    """
    composite_score: float                     # 0 - 100 overall attractiveness score
    demand_index: float                        # Scaled 0 - 100 volume & velocity
    intent_index: float                        # Scaled 0 - 100 commercial monetization potency
    competition_barrier: float                 # Scaled 0 - 100 difficulty penalty
    projected_roi_pct: float                   # Expected annual Return on Content Investment
    recommended_monetization: MonetizationType # Primary revenue model indicated by signals
    confidence: float                          # 0.0 - 1.0 confidence in underlying data
    thesis_notes: List[str] = field(default_factory=list)


@dataclass
class Niche:
    """
    A distinct topic vertical / domain managed as an autonomous business unit.
    """
    id: str
    name: str
    description: str
    vertical: str
    signals: List[MarketSignal] = field(default_factory=list)
    opportunity_score: Optional[OpportunityScore] = None
    state: NicheLifecycleState = NicheLifecycleState.DISCOVERY
    allocated_budget: float = 0.0
    monetization_profile: Optional[MonetizationProfile] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def is_viable_candidate(self, minimum_score: float = 65.0) -> bool:
        """Returns True if the niche meets the hurdle rate for incubation."""
        return (
            self.opportunity_score is not None
            and self.opportunity_score.composite_score >= minimum_score
            and self.opportunity_score.projected_roi_pct > 20.0
        )
