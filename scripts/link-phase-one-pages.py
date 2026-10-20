#!/usr/bin/env python3
"""Add discoverable, idempotent links from existing hubs to the Phase 1 library."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

SECTOR_GUIDES = {
    "education": [
        ("Foundational literacy and numeracy tracking software", "/education/guides/foundational-literacy-and-numeracy-tracking-software/"),
        ("School attendance and dropout early-warning systems", "/education/guides/school-attendance-and-dropout-early-warning-systems/"),
    ],
    "youth-employability": [
        ("Placement verification and retention systems for skilling programmes", "/youth-employability/guides/placement-verification-and-retention-systems-for-skilling-programmes/"),
    ],
    "livelihoods": [
        ("Household graduation tracking systems", "/livelihoods/guides/household-graduation-tracking-systems/"),
    ],
    "health": [
        ("Community health worker case management systems", "/health/guides/community-health-worker-case-management-systems/"),
    ],
    "maternal-child-health": [
        ("Pregnancy and antenatal care tracking systems", "/maternal-child-health/guides/pregnancy-and-antenatal-care-tracking-systems/"),
    ],
    "child-protection": [
        ("Child protection case management systems", "/child-protection/guides/child-protection-case-management-systems/"),
    ],
    "gender": [
        ("Women's collective and group management systems", "/gender/guides/womens-collective-and-group-management-systems/"),
    ],
    "disability": [
        ("Disability inclusion case management systems", "/disability/guides/disability-inclusion-case-management-systems/"),
    ],
    "community-development": [
        ("Community needs and household profiling systems", "/community-development/guides/community-needs-and-household-profiling-systems/"),
    ],
}


def sector_block(links):
    cards = "".join(
        f'<a class="phase-guide-card" href="{href}"><span>Implementation guide</span><strong>{title}</strong><b>Read the guide →</b></a>'
        for title, href in links
    )
    return (
        '<!-- phase-one-guides:start -->'
        '<section class="band phase-guides" aria-labelledby="phase-guides-title"><div class="wrap">'
        '<div class="sec-head"><div class="eyebrow">Go deeper</div>'
        '<h2 id="phase-guides-title">Practical guides for this programme context.</h2>'
        '<p>Use these focused implementation guides alongside the sector playbook.</p></div>'
        f'<div class="phase-guide-grid">{cards}</div>'
        '</div></section>'
        '<!-- phase-one-guides:end -->\n'
    )


def link_sector_guides():
    marker = '<section class="band" id="talk"'
    for sector, links in SECTOR_GUIDES.items():
        path = ROOT / sector / "index.html"
        html = path.read_text()
        if "<!-- phase-one-guides:start -->" in html:
            html = re.sub(
                r"<!-- phase-one-guides:start -->.*?<!-- phase-one-guides:end -->\n?",
                sector_block(links),
                html,
                count=1,
                flags=re.S,
            )
            path.write_text(html)
            continue
        if marker not in html:
            raise RuntimeError(f"Could not find talk section in {path}")
        path.write_text(html.replace(marker, sector_block(links) + marker, 1))


def link_programme_vertical():
    path = ROOT / "verticals/programme-evidence-systems/index.html"
    html = path.read_text()
    old = (
        '<a class="resource" href="https://www.edzola.com/post/what-is-a-management-information-system-mis-for-nonprofits-the-complete-2026-guide" '
        'target="_blank" rel="noopener noreferrer"><small>Complete guide</small><h3>What is a nonprofit MIS?</h3>'
        '<p>A practical 2026 guide to the purpose and structure of management information systems.</p><b>Read on edzola.com ↗</b></a>'
    )
    new = (
        '<a class="resource" href="/solutions/nonprofit-mis-software/"><small>Complete guide</small><h3>Nonprofit MIS software</h3>'
        '<p>Records, workflows, indicators, permissions and implementation decisions for a useful nonprofit MIS.</p><b>Read the guide →</b></a>'
        '<a class="resource" href="/solutions/"><small>Solution library</small><h3>Explore programme-system solutions</h3>'
        '<p>Compare MIS, M&amp;E, CRM, privacy, voice AI and workflow-automation approaches.</p><b>Explore solutions →</b></a>'
    )
    if new in html:
        return
    if old not in html:
        raise RuntimeError(f"Could not find legacy MIS resource in {path}")
    path.write_text(html.replace(old, new, 1))


if __name__ == "__main__":
    link_sector_guides()
    link_programme_vertical()
    print("Linked Phase 1 pages from 9 sector hubs and the programme-evidence vertical.")
