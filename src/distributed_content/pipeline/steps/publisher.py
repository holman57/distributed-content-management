"""
Content Pipeline Step 6: Multi-Channel Publishing and Attribution Instrumentation.
"""

from datetime import datetime
from ...models.content import ContentItem, ContentState


class PublisherStep:
    """
    Handles deployment to target CMS/static host and instruments UTM tracking for attribution.
    """

    def publish_content(self, content: ContentItem, base_domain: str = "https://intelligence.local") -> str:
        """
        Publishes content piece, updates item state to PUBLISHED, and assigns instrumented URL.
        """
        slug = content.title.lower().replace(" ", "-").replace(":", "").replace("/", "")
        published_url = f"{base_domain}/{content.niche_id}/{slug}?utm_source=organic&utm_medium=content&utm_campaign={content.niche_id}"
        
        content.published_url = published_url
        content.published_at = datetime.utcnow()
        content.state = ContentState.PUBLISHED

        return published_url
