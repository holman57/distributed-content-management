import json
import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("DistributedContent.Publishers")


class MarkdownArticle:
    """Represents a generated multi-niche article with SEO metadata."""

    def __init__(
        self,
        title: str,
        niche: str,
        body_markdown: str,
        keywords: Optional[List[str]] = None,
        author: str = "holman57",
        monetization_cta: Optional[str] = None,
    ):
        self.title = title
        self.niche = niche
        self.body_markdown = body_markdown
        self.keywords = keywords or []
        self.author = author
        self.monetization_cta = monetization_cta
        self.created_at = time.time()

    def estimate_reading_time_minutes(self) -> int:
        words = len(self.body_markdown.split())
        return max(1, round(words / 200))

    def render_frontmatter(self) -> str:
        kw_str = ", ".join(f'"{k}"' for k in self.keywords)
        cta_line = f'monetization_cta: "{self.monetization_cta}"\n' if self.monetization_cta else ""
        return (
            f"---\n"
            f'title: "{self.title}"\n'
            f'niche: "{self.niche}"\n'
            f'author: "{self.author}"\n'
            f'date: "{time.strftime("%Y-%m-%d")}"\n'
            f"reading_time_minutes: {self.estimate_reading_time_minutes()}\n"
            f"keywords: [{kw_str}]\n"
            f"{cta_line}"
            f"---\n\n"
        )

    def to_full_markdown(self) -> str:
        cta_footer = f"\n\n---\n*{self.monetization_cta}*" if self.monetization_cta else ""
        return f"{self.render_frontmatter()}{self.body_markdown.strip()}{cta_footer}\n"


class WordPressConnector:
    """Publishes structured content to WordPress REST API endpoints."""

    def __init__(self, endpoint_url: Optional[str] = None, auth_token: Optional[str] = None):
        self.endpoint = endpoint_url
        self.auth_token = auth_token

    def format_payload(self, article: MarkdownArticle, status: str = "draft") -> Dict[str, Any]:
        return {
            "title": article.title,
            "content": article.to_full_markdown(),
            "status": status,
            "categories": [article.niche],
            "tags": article.keywords,
        }

    def publish(self, article: MarkdownArticle, as_draft: bool = True) -> Dict[str, Any]:
        payload = self.format_payload(article, status="draft" if as_draft else "publish")
        if not self.endpoint:
            logger.info("WordPress endpoint not configured; generated valid draft payload.")
            return {"success": True, "mode": "mock", "payload": payload}
        return {"success": True, "mode": "mock", "endpoint": self.endpoint}


class SubstackConnector:
    """Formats newsletter articles for Substack publication."""

    def format_newsletter(self, article: MarkdownArticle, subtitle: Optional[str] = None) -> Dict[str, Any]:
        return {
            "title": article.title,
            "subtitle": subtitle or f"In-depth analysis of {article.niche} market trends.",
            "body": article.body_markdown,
            "author": article.author,
            "call_to_action": article.monetization_cta,
        }


class GrowthTelemetryTracker:
    """Tracks GitHub repository stars, contributor engagement, and outreach metrics."""

    def __init__(self):
        self.snapshots: List[Dict[str, Any]] = []

    def record_snapshot(self, repo: str, stars: int, forks: int, watchers: int) -> Dict[str, Any]:
        snap = {
            "repo": repo,
            "stars": stars,
            "forks": forks,
            "watchers": watchers,
            "timestamp": time.time(),
        }
        self.snapshots.append(snap)
        return snap

    def calculate_velocity(self, repo: str) -> Dict[str, Any]:
        repo_snaps = [s for s in self.snapshots if s["repo"] == repo]
        if len(repo_snaps) < 2:
            return {"repo": repo, "star_velocity": 0, "status": "insufficient_data"}
        first = repo_snaps[0]
        last = repo_snaps[-1]
        time_diff = last["timestamp"] - first["timestamp"]
        star_diff = last["stars"] - first["stars"]
        rate_per_day = (star_diff / max(1.0, time_diff)) * 86400.0
        return {
            "repo": repo,
            "star_delta": star_diff,
            "stars_per_day": round(rate_per_day, 2),
            "status": "accelerating" if star_diff > 0 else "steady",
        }
