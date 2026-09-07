"""
End-to-End Demonstration: Autonomous Niche Discovery, Spawning Systems,
and Data-Driven Lifecycle Governance across Multiple Monetization Streams.
"""

import json
import os
import sys

# Ensure repository root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.distributed_content.orchestrator import MetaOrchestrator
from src.distributed_content.models import (
    NicheLifecycleState,
    LifecycleAction,
    MonetizationType,
    MonetizationConfig,
)


def print_header(title: str):
    print("\n" + "=" * 80)
    print(f"  {title.upper()}")
    print("=" * 80)


def print_step(step_name: str, description: str):
    print(f"\n[STEP] {step_name}")
    print(f"       -> {description}")


def main():
    print_header("Distributed Content Management: Autonomous Niche Portfolio Engine")
    print("Initializing Meta-Orchestrator, Market Research Engine, and Portfolio Allocator...")

    orchestrator = MetaOrchestrator()

    # =========================================================================
    # PHASE 1: Autonomous Market Research & Niche Discovery
    # =========================================================================
    print_header("Phase 1: Autonomous Market Research & Niche Discovery")

    discovery_targets = [
        {
            "id": "niche-devtools",
            "name": "B2B AI Agent Tooling",
            "vertical": "Enterprise Software",
            "keywords": [
                "best enterprise ai coding agent comparison",
                "autonomous coding platform review",
                "ai code review tool pricing",
            ],
        },
        {
            "id": "niche-homelab",
            "name": "Self-Hosted Private Cloud",
            "vertical": "Privacy & DevOps",
            "keywords": [
                "best self-hosted cloud storage for privacy",
                "nextcloud vs owncloud benchmarks",
                "how to fix nextcloud sync error",
            ],
        },
        {
            "id": "niche-templates",
            "name": "Prompt Engineering Systems",
            "vertical": "Productivity & AI",
            "keywords": [
                "best prompt management tool for teams",
                "prompt engineering course pricing",
                "prompt testing tool review",
            ],
        },
        {
            "id": "niche-legacy",
            "name": "Deprecated Framework Migrations",
            "vertical": "Legacy Tech",
            "keywords": [
                "obsolete framework v1 maintenance",
                "legacy framework error 404 troubleshoot",
            ],
        },
    ]

    candidates = []
    for target in discovery_targets:
        niche = orchestrator.discover_niche(
            niche_id=target["id"],
            name=target["name"],
            vertical=target["vertical"],
            seed_keywords=target["keywords"],
        )
        candidates.append(niche)
        opp = niche.opportunity_score
        print(f"\n> Scanned: {niche.name} ({niche.vertical})")
        print(f"  Composite Opportunity Score: {opp.composite_score}/100 | Projected 1st-Yr ROI: {opp.projected_roi_pct}%")
        print(f"  Recommended Monetization:   {opp.recommended_monetization.value.upper()}")
        print(f"  Primary Demand Signals:     Volume={sum(s.monthly_search_volume for s in niche.signals):,}, "
              f"Avg CPC=${sum(s.average_cpc for s in niche.signals)/len(niche.signals):.2f}")
        for note in opp.thesis_notes:
            print(f"    * {note}")

    # =========================================================================
    # PHASE 2: Data-Driven Spin-Up & System Spawning
    # =========================================================================
    print_header("Phase 2: Higher-Order Spin-Up Decisions & System Spawning")

    spawned_instances = []
    for candidate in candidates:
        print(f"\nEvaluating candidate '{candidate.name}' against governance hurdle rates...")
        decision = orchestrator.governor.evaluate_candidate(candidate)
        print(f"  Action: {decision.action.value.upper()}")
        print(f"  Rationale: {decision.rationale}")

        if decision.action == LifecycleAction.SPIN_UP:
            instance = orchestrator.spawn_pipeline_instance(candidate, initial_budget=600.0)
            if instance:
                spawned_instances.append(instance)
                print(f"  [SUCCESS] Spawned autonomous NichePipelineInstance for '{candidate.name}'")
                print(f"            Allocated Budget: ${candidate.allocated_budget:.2f} | Topic Clusters: {len(instance.topic_roadmap)}")

    # =========================================================================
    # PHASE 3: Content Pipeline & Content Lifecycle In Action
    # =========================================================================
    print_header("Phase 3: Encapsulated Content Pipeline & Lifecycle Execution")
    print("Each spawned subsystem executes the 7-step Content Pipeline autonomously:")
    print("Keyword Research -> Brief -> Draft -> Assets / SEO Pass -> Publish -> Repurpose\n")

    for instance in spawned_instances:
        print(f"--- Subsystem: {instance.niche.name} ---")
        print(f"Initial Pilot Batch: {len(instance.content_items)} pieces published.")
        for item in instance.content_items:
            print(f"  * [{item.state.value.upper()}] '{item.title}'")
            print(f"    - Brief Hook:   {item.brief.monetization_hook}")
            print(f"    - Assets:       {[a.asset_type for a in item.assets]}")
            print(f"    - SEO Grade:    {item.seo_report.title_hook_grade} (Density: {item.seo_report.keyword_density}%)")
            print(f"    - URL:          {item.published_url}")
            print(f"    - Repurposed:   {[r.channel for r in item.repurposed_items]}")
        print()

    # =========================================================================
    # PHASE 4: Telemetry Simulation Across Monetization Channels
    # =========================================================================
    print_header("Phase 4: Telemetry Ingestion Across Monetization Channels")
    print("Simulating 60 days of real-world operational telemetry...\n")

    # Instance 1 (B2B Tooling): Breakout performer (Lead Generation)
    inst_b2b = orchestrator.registry.get("niche-devtools")
    if inst_b2b:
        inst_b2b.update_telemetry(
            simulated_impressions=28000,
            simulated_clicks=1400,
            simulated_conversions=32,      # 32 enterprise leads @ $150
            revenue_per_conversion=150.0,
        )
        inst_b2b.metrics.traffic_growth_rate = 0.28
        inst_b2b.metrics.avg_dwell_time_seconds = 115.0
        print(f"> Telemetry: {inst_b2b.niche.name}")
        print(f"  Impressions: {inst_b2b.metrics.monthly_impressions:,} | Clicks: {inst_b2b.metrics.monthly_clicks:,} "
              f"| CTR: {inst_b2b.metrics.ctr*100:.2f}% | Conv: {inst_b2b.metrics.conversions}")
        print(f"  Spend: ${inst_b2b.metrics.total_cost:.2f} | Revenue: ${inst_b2b.metrics.total_revenue:.2f} | ROI: +{inst_b2b.metrics.roi_pct:.1f}%")

    # Instance 2 (Self-Hosted Cloud): High traffic, but low affiliate conversion (Pivot candidate)
    inst_homelab = orchestrator.registry.get("niche-homelab")
    if inst_homelab:
        inst_homelab.update_telemetry(
            simulated_impressions=42000,
            simulated_clicks=2100,
            simulated_conversions=4,       # Weak conversion (0.19% < 0.5% hurdle)
            revenue_per_conversion=25.0,
        )
        inst_homelab.metrics.traffic_growth_rate = 0.12
        inst_homelab.metrics.avg_dwell_time_seconds = 85.0
        print(f"\n> Telemetry: {inst_homelab.niche.name}")
        print(f"  Impressions: {inst_homelab.metrics.monthly_impressions:,} | Clicks: {inst_homelab.metrics.monthly_clicks:,} "
              f"| CTR: {inst_homelab.metrics.ctr*100:.2f}% | Conv: {inst_homelab.metrics.conversions}")
        print(f"  Spend: ${inst_homelab.metrics.total_cost:.2f} | Revenue: ${inst_homelab.metrics.total_revenue:.2f} | ROI: {inst_homelab.metrics.roi_pct:.1f}%")

    # Instance 3 (Prompt Systems): Digital product sales performing steadily
    inst_templates = orchestrator.registry.get("niche-templates")
    if inst_templates:
        inst_templates.update_telemetry(
            simulated_impressions=18000,
            simulated_clicks=720,
            simulated_conversions=18,      # 18 template kits @ $49
            revenue_per_conversion=49.0,
        )
        inst_templates.metrics.traffic_growth_rate = 0.15
        inst_templates.metrics.avg_dwell_time_seconds = 75.0
        print(f"\n> Telemetry: {inst_templates.niche.name}")
        print(f"  Impressions: {inst_templates.metrics.monthly_impressions:,} | Clicks: {inst_templates.metrics.monthly_clicks:,} "
              f"| CTR: {inst_templates.metrics.ctr*100:.2f}% | Conv: {inst_templates.metrics.conversions}")
        print(f"  Spend: ${inst_templates.metrics.total_cost:.2f} | Revenue: ${inst_templates.metrics.total_revenue:.2f} | ROI: +{inst_templates.metrics.roi_pct:.1f}%")

    # Instance 4: Experimental niche that experiences market decay & penalty (Wind-Down candidate)
    print("\nSimulating an experimental pilot pipeline encountering traffic decay and algorithmic penalty...")
    exp_niche = orchestrator.discover_niche(
        niche_id="niche-experimental-feed",
        name="Micro-Arbitrage Bots",
        vertical="FinTech",
        seed_keywords=[
            "best crypto arbitrage bot comparison",
            "crypto bot review pricing",
            "how to fix arbitrage bot latency",
        ],
    )
    inst_decay = orchestrator.spawn_pipeline_instance(exp_niche, initial_budget=600.0)
    if inst_decay:
        inst_decay.update_telemetry(
            simulated_impressions=600,
            simulated_clicks=15,
            simulated_conversions=0,
            revenue_per_conversion=0.0,
        )
        inst_decay.metrics.traffic_growth_rate = -0.42
        inst_decay.metrics.indexation_rate = 0.35  # Penalty: only 35% indexation
        print(f"> Telemetry: {inst_decay.niche.name}")
        print(f"  Impressions: {inst_decay.metrics.monthly_impressions} | Clicks: {inst_decay.metrics.monthly_clicks} "
              f"| Growth: {inst_decay.metrics.traffic_growth_rate*100:.1f}% | Indexation: {inst_decay.metrics.indexation_rate*100:.1f}%")
        print(f"  Spend: ${inst_decay.metrics.total_cost:.2f} | Revenue: ${inst_decay.metrics.total_revenue:.2f} | ROI: {inst_decay.metrics.roi_pct:.1f}%")

    # =========================================================================
    # PHASE 5: Higher-Order Governance (Scale, Pivot, Wind-Down)
    # =========================================================================
    print_header("Phase 5: Higher-Order Portfolio Governance Execution")

    decisions = orchestrator.evaluate_and_govern_active_pipelines()
    for d in decisions:
        print(f"\n> Subsystem: {d.niche_id}")
        print(f"  Action:    {d.action.value.upper()}")
        print(f"  Rationale: {d.rationale}")

    # Sunset execution on wound-down instance
    print("\nExecuting sunset and link equity harvesting on wound-down pipeline...")
    sunset_report = orchestrator.sunset_pipeline("niche-experimental-feed")
    if sunset_report:
        print(f"  Status: {sunset_report['status'].upper()} | Pieces Harvested: {sunset_report['pieces_harvested']}")
        print(f"  Redirects Configured: {len(sunset_report['redirect_map'])} URLs mapped to portfolio hub.")

    # =========================================================================
    # PHASE 6: Portfolio Health & Diversification Summary
    # =========================================================================
    print_header("Phase 6: Consolidated Portfolio Ledger & Risk Diversification")

    summary = orchestrator.get_portfolio_summary()
    print(f"Active Pipeline Subsystems: {summary['total_active_pipelines']}")
    print(f"Total Content Published:    {summary['total_pieces_published']} pieces across portfolio")
    print(f"Consolidated Traffic:       {summary['monthly_clicks']:,} clicks / {summary['monthly_impressions']:,} impressions")
    print(f"Gross Portfolio Revenue:    ${summary['total_revenue']:,.2f}")
    print(f"Total Production Costs:     ${summary['total_cost']:,.2f}")
    print(f"Net Operating Profit:       ${summary['net_profit']:,.2f}")
    print(f"Blended Portfolio ROI:      +{summary['blended_roi_pct']:.1f}%")
    print(f"Unallocated Capital Pool:   ${summary['unallocated_capital']:,.2f} of ${summary['total_capital_pool']:,.2f}")

    print("\nMonetization Stream Diversification Breakdown:")
    div = summary["diversification"]
    for stream, share in div["percentage_share"].items():
        rev = div["revenue_by_stream"].get(stream, 0.0)
        print(f"  - {stream.upper():<20}: {share:5.1f}% of pipelines | ${rev:8.2f} revenue generated")

    if div["concentration_warning"]:
        print(f"\n[ALERT] Risk Management: {div['concentration_warning']}")
    else:
        print("\n[OK] Portfolio risk is well diversified across multiple monetization vehicles.")


if __name__ == "__main__":
    main()
