"""
Governance thresholds and evaluation criteria for data-driven lifecycle transitions.
"""

from dataclasses import dataclass


@dataclass
class GovernanceThresholds:
    """
    Quantitative benchmark hurdle rates for spin-up, scale, pivot, and wind-down decisions.
    """
    # Spin-Up Hurdle Rates (Pre-launch validation)
    spin_up_min_opportunity_score: float = 55.0    # Minimum composite score (0-100)
    spin_up_min_projected_roi: float = 25.0        # Minimum projected 1st-year ROI %
    spin_up_min_buyer_intent: float = 0.45         # Minimum commercial keyword ratio

    # Scale Hurdle Rates (Expanding from Pilot to Growth)
    scale_min_published_pieces: int = 3            # Minimum pieces required before scale evaluation
    scale_min_roi: float = 40.0                    # Positive ROI % threshold to scale
    scale_min_ctr: float = 0.025                   # Minimum Click-Through Rate (2.5%)
    scale_min_conversion_rate: float = 0.015       # Minimum 1.5% conversion rate
    scale_min_traffic_growth_rate: float = 0.10    # Minimum +10% MoM growth

    # Pivot Triggers (Traffic viable, but monetization misaligned)
    pivot_min_traffic_volume: int = 1500           # Has substantial traffic
    pivot_max_conversion_rate: float = 0.005       # But conversion rate is abysmal (<0.5%)
    pivot_min_dwell_time: float = 60.0             # Engaged readership (readers stay > 60s)

    # Wind-Down / Exit Triggers (Capital protection & resource reallocation)
    wind_down_min_runway_pieces: int = 3           # Must have published enough to validate
    wind_down_max_roi: float = -35.0               # Bleeding cash (-35% net loss)
    wind_down_traffic_decay_rate: float = -0.25    # Traffic collapsing by >25%
    wind_down_min_indexation_rate: float = 0.50    # Search engine penalty / indexation failure (<50%)
