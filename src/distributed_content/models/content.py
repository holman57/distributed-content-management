"""
Content item and lower-order pipeline models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class ContentState(str, Enum):
    """
    Individual content item lifecycle states matching the repository state machine.
    """
    IDLE = "idle"
    RESEARCH = "research"
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    REPURPOSED = "repurposed"
    ARCHIVED = "archived"


@dataclass
class ContentBrief:
    """
    Strategic blueprint for a single piece of content.
    """
    target_keyword: str
    search_intent: str             # e.g., "Commercial Investigation", "Transactional", "Informational"
    topic_cluster: str             # e.g., "Self-Hosted Cloud Pillar", "Comparative Review"
    target_audience_pain_points: List[str] = field(default_factory=list)
    competitor_gaps_to_exploit: List[str] = field(default_factory=list)
    call_to_action: str = ""
    monetization_hook: str = ""    # Specific affiliate product or lead-magnet offer


@dataclass
class Asset:
    """
    Visual, code, or downloadable media artifact paired with the written content.
    """
    asset_type: str                # e.g., "thumbnail", "infographic", "comparison_matrix", "cheatsheet"
    title: str
    content_payload: str
    status: str = "generated"


@dataclass
class SEOReport:
    """
    Quality gate validation verifying search engine optimization.
    """
    primary_keyword: str
    keyword_density: float
    readability_score: float       # Flesch-Kincaid style score
    title_hook_grade: str          # e.g., "A", "B", "C"
    internal_links_count: int
    has_meta_description: bool
    passed: bool = True
    feedback: List[str] = field(default_factory=list)


@dataclass
class RepurposedArtifact:
    """
    Derivative content asset generated from a published pillar piece.
    """
    channel: str                   # "newsletter", "twitter_thread", "linkedin_post", "youtube_short_script"
    summary_text: str
    call_to_action: str
    published: bool = False


@dataclass
class ContentItem:
    """
    A single content unit moving through the 7-step Content Pipeline.
    """
    id: str
    niche_id: str
    title: str
    state: ContentState = ContentState.IDLE
    brief: Optional[ContentBrief] = None
    draft_body: str = ""
    assets: List[Asset] = field(default_factory=list)
    seo_report: Optional[SEOReport] = None
    repurposed_items: List[RepurposedArtifact] = field(default_factory=list)
    published_url: Optional[str] = None
    cost_to_produce: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = None
