"""
Performance telemetry and lifecycle decision data models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any


class LifecycleAction(str, Enum):
    """Actions the Lifecycle Governor can execute on a niche pipeline."""
    HOLD = "hold"                  # Maintain current operational tempo
    SPIN_UP = "spin_up"            # Deploy and initialize new pipeline instance
    SCALE = "scale"                # Ramp up publishing velocity and resource allocation
    PIVOT = "pivot"                # Reposition monetization model or audience angle
    WIND_DOWN = "wind_down"        # Halt new content drafts, harvest remaining value
    SUNSET = "sunset"              # Permanently deprovision and redirect links/equity


@dataclass
class PerformanceMetrics:
    """Telemetry data capturing performance across content and monetization."""
    total_pieces_published: int = 0
    monthly_impressions: int = 0
    monthly_clicks: int = 0
    ctr: float = 0.0
    avg_dwell_time_seconds: float = 0.0
    conversions: int = 0
    conversion_rate: float = 0.0
    total_cost: float = 0.0
    total_revenue: float = 0.0
    net_profit: float = 0.0
    roi_pct: float = 0.0
    traffic_growth_rate: float = 0.0    # e.g., +0.20 for +20% month-over-month
    email_subscribers: int = 0
    indexation_rate: float = 1.0        # % of published pieces indexed by search engines

    def calculate_derived(self) -> None:
        """Recompute derived fields based on raw figures."""
        if self.monthly_impressions > 0:
            self.ctr = self.monthly_clicks / self.monthly_impressions
        else:
            self.ctr = 0.0

        if self.monthly_clicks > 0:
            self.conversion_rate = self.conversions / self.monthly_clicks
        else:
            self.conversion_rate = 0.0

        self.net_profit = self.total_revenue - self.total_cost
        if self.total_cost > 0:
            self.roi_pct = (self.net_profit / self.total_cost) * 100.0
        else:
            self.roi_pct = 0.0


@dataclass
class LifecycleDecision:
    """Data-driven governance decision emitted by the Lifecycle Governor."""
    action: LifecycleAction
    niche_id: str
    rationale: str
    confidence: float
    evaluation_metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
