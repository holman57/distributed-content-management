"""
Monetization stream models and strategy profiles.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class MonetizationType(str, Enum):
    """Supported monetization channels across the content portfolio."""
    AFFILIATE = "affiliate"                  # Amazon, high-ticket SaaS, affiliate networks
    DIGITAL_PRODUCT = "digital_product"      # eBooks, courses, templates, toolkits, boilerplates
    PROGRAMMATIC_ADS = "programmatic_ads"    # Display ads, video pre-roll (needs scale)
    LEAD_GENERATION = "lead_generation"      # B2B buyer leads, client inquiries, quote requests
    NEWSLETTER_SUB = "newsletter_sub"        # Substack/Beehiiv paid tiers, sponsored blasts
    SPONSORSHIP = "sponsorship"              # Direct brand integration, banner sponsorships


@dataclass
class MonetizationConfig:
    """Configuration & benchmark parameters for a monetization stream."""
    model_type: MonetizationType
    target_rpm: float                  # Revenue per 1,000 visitors ($)
    avg_order_value_or_bounty: float   # Commission per conversion or product price ($)
    conversion_rate_benchmark: float   # Expected conversion rate (e.g. 0.02 = 2%)
    minimum_monthly_volume: int        # Minimum traffic threshold before activating
    description: str = ""


@dataclass
class MonetizationProfile:
    """Monetization status and multi-stream allocation for a niche."""
    primary: MonetizationConfig
    secondary: Optional[MonetizationConfig] = None
    email_capture_enabled: bool = True
    total_leads_captured: int = 0
    cumulative_revenue: float = 0.0

    def calculate_projected_revenue(self, estimated_traffic: int) -> float:
        """Projects expected monthly revenue given estimated traffic volume."""
        primary_rev = (estimated_traffic / 1000.0) * self.primary.target_rpm
        secondary_rev = 0.0
        if self.secondary and estimated_traffic >= self.secondary.minimum_monthly_volume:
            secondary_rev = (estimated_traffic / 1000.0) * self.secondary.target_rpm
        return primary_rev + secondary_rev
