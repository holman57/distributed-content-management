"""
Content Pipeline Step 1: Keyword Research and Topic Clustering.
"""

from typing import List, Dict
from ...models.niche import MarketSignal


class KeywordResearchStep:
    """
    Groups market signals into cohesive pillar and cluster topics with buyer-intent prioritization.
    """

    def generate_content_roadmap(self, niche_name: str, signals: List[MarketSignal]) -> List[Dict[str, str]]:
        """
        Transforms raw market signals into an prioritized editorial schedule of target topics.
        """
        roadmap = []
        # Sort keywords by buyer intent and volume
        sorted_signals = sorted(
            signals,
            key=lambda s: (s.buyer_intent_ratio, s.monthly_search_volume),
            reverse=True
        )

        for idx, sig in enumerate(sorted_signals):
            kw = sig.keyword
            # Determine cluster role: first high-volume/intent piece is Pillar, others are Cluster Support
            is_pillar = (idx == 0 or "best" in kw.lower() or "guide" in kw.lower())
            role = "pillar" if is_pillar else "cluster_support"

            intent_label = "Commercial" if sig.buyer_intent_ratio > 0.6 else "Informational"
            if "pricing" in kw.lower() or "discount" in kw.lower():
                intent_label = "Transactional"

            roadmap.append({
                "target_keyword": kw,
                "role": role,
                "search_intent": intent_label,
                "estimated_monthly_volume": str(sig.monthly_search_volume),
                "cpc": f"${sig.average_cpc:.2f}",
            })

        return roadmap
