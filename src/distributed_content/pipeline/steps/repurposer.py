"""
Content Pipeline Step 7: Content Repurposing and Owned Audience Syndication.
"""

from typing import List
from ...models.content import ContentItem, RepurposedArtifact, ContentState


class RepurposerStep:
    """
    Transforms published pillar content into derivative formats across owned and rented channels.
    Feeds owned audience acquisition (newsletters, email lists) and expands algorithmic reach.
    """

    def repurpose(self, content: ContentItem) -> List[RepurposedArtifact]:
        """
        Generates multi-platform derivative assets from a published content piece.
        """
        artifacts = []
        kw = content.brief.target_keyword if content.brief else content.title

        # 1. Newsletter Edition (Owned Audience Channel)
        newsletter = RepurposedArtifact(
            channel="newsletter",
            summary_text=(
                f"Subject: The Real Cost of {kw} (Field Report)\n\n"
                f"Hey everyone,\n\n"
                f"Most guides on {kw} overlook the hidden infrastructure costs and integration bottlenecks. "
                f"We just published our benchmark teardown. Here is the tl;dr of what we learned..."
            ),
            call_to_action="Read the full benchmark analysis on our site or reply with your experience.",
            published=True,
        )
        artifacts.append(newsletter)

        # 2. Executive Social Thread (Algorithmic Top-of-Funnel)
        thread = RepurposedArtifact(
            channel="social_thread",
            summary_text=(
                f"1/6 Most teams approach {kw} backwards.\n\n"
                f"Here are 3 critical failure points to avoid if you want break-even ROI in under 60 days 🧵👇\n"
                f"2/6 Pitfall #1: Relying on outdated vendor documentation...\n"
                f"3/6 Pitfall #2: Skipping end-to-end attribution hooks...\n"
                f"6/6 Full walkthrough & downloadable checklist linked below."
            ),
            call_to_action="Bookmark this thread and check the link for our implementation cheatsheet.",
            published=True,
        )
        artifacts.append(thread)

        # 3. Short Video Script (YouTube Shorts / TikTok)
        video_script = RepurposedArtifact(
            channel="short_video_script",
            summary_text=(
                f"[Hook - 0-3s]: Stop making this costly mistake with {kw}!\n"
                f"[Problem - 3-15s]: 80% of setups fail because of configuration drift.\n"
                f"[Solution - 15-45s]: Here are the 3 settings you must toggle immediately.\n"
                f"[CTA - 45-60s]: Grab the free pre-flight checklist in bio."
            ),
            call_to_action="Link in bio for full architecture breakdown.",
            published=True,
        )
        artifacts.append(video_script)

        content.repurposed_items.extend(artifacts)
        content.state = ContentState.REPURPOSED

        return artifacts
