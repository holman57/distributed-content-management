"""
Distributed Content Management - Autonomous Niche Portfolio Engine.
"""

from .models import (
    Niche,
    NicheLifecycleState,
    MarketSignal,
    OpportunityScore,
    MonetizationType,
    MonetizationConfig,
    MonetizationProfile,
    ContentItem,
    ContentState,
    ContentBrief,
    Asset,
    SEOReport,
    RepurposedArtifact,
    PerformanceMetrics,
    LifecycleAction,
    LifecycleDecision,
)
from .market_research import (
    MarketSignalCollector,
    MarketFeasibilityAnalyzer,
    OpportunityScorer,
)
from .decision_engine import (
    GovernanceThresholds,
    LifecycleGovernor,
)
from .pipeline import (
    NichePipelineInstance,
    KeywordResearchStep,
    BriefBuilderStep,
    DraftGeneratorStep,
    AssetsAndSEOStep,
    PublisherStep,
    RepurposerStep,
)
from .orchestrator import (
    PipelineRegistry,
    PortfolioManager,
    MetaOrchestrator,
)

__all__ = [
    "Niche",
    "NicheLifecycleState",
    "MarketSignal",
    "OpportunityScore",
    "MonetizationType",
    "MonetizationConfig",
    "MonetizationProfile",
    "ContentItem",
    "ContentState",
    "ContentBrief",
    "Asset",
    "SEOReport",
    "RepurposedArtifact",
    "PerformanceMetrics",
    "LifecycleAction",
    "LifecycleDecision",
    "MarketSignalCollector",
    "MarketFeasibilityAnalyzer",
    "OpportunityScorer",
    "GovernanceThresholds",
    "LifecycleGovernor",
    "NichePipelineInstance",
    "KeywordResearchStep",
    "BriefBuilderStep",
    "DraftGeneratorStep",
    "AssetsAndSEOStep",
    "PublisherStep",
    "RepurposerStep",
    "PipelineRegistry",
    "PortfolioManager",
    "MetaOrchestrator",
]
