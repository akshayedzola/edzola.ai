#!/usr/bin/env python3
"""Build the EdZola content-expansion registry and AI question bank.

The script intentionally creates planning records, not publishable page copy. It keeps
one durable source of truth for page intent, URL, evidence status and rollout phase.
"""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "expansion"


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ").replace("'", "").replace("’", "")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


SECTORS = [
    {
        "slug": "education",
        "name": "Education",
        "guides": [
            "Student information management systems for NGOs",
            "Foundational literacy and numeracy tracking software",
            "School attendance and dropout early-warning systems",
            "Teacher observation and coaching MIS",
            "Student learning outcome dashboards",
        ],
        "questions": [
            "How to track learning outcomes in NGO programmes",
            "How to design a student baseline and endline",
            "How to track out-of-school children through enrolment",
            "How to build a teacher observation checklist",
            "What data should an education NGO collect",
        ],
    },
    {
        "slug": "youth-employability",
        "name": "Youth Development and Employability",
        "guides": [
            "Skilling programme MIS for NGOs",
            "Candidate mobilisation and enrolment tracking systems",
            "Attendance assessment and dropout dashboards for skilling programmes",
            "Placement verification and retention systems for skilling programmes",
            "Alumni outcomes and wage progression dashboards",
        ],
        "questions": [
            "How to track candidates from mobilisation to enrolment",
            "How to calculate course completion and dropout rates",
            "How to verify placement outcomes after training",
            "How to measure 90-day and 180-day employment retention",
            "What data should a skilling NGO collect",
        ],
    },
    {
        "slug": "livelihoods",
        "name": "Livelihoods and Economic Empowerment",
        "guides": [
            "Household graduation tracking systems",
            "Self-help group management software for nonprofits",
            "Microenterprise support case management systems",
            "Farmer market-linkage and producer-group MIS",
            "Livelihood income and resilience outcome dashboards",
        ],
        "questions": [
            "How to track household graduation in livelihoods programmes",
            "How to measure changes in household income reliably",
            "How to manage self-help group records and meetings",
            "How to track enterprise survival after programme support",
            "What data should a livelihoods NGO collect",
        ],
    },
    {
        "slug": "health",
        "name": "Health and Wellbeing",
        "guides": [
            "Community health worker case management systems",
            "Patient referral and closure tracking software",
            "Screening treatment and adherence monitoring systems",
            "Community clinic and outreach programme MIS",
            "Population health outcome dashboards for nonprofits",
        ],
        "questions": [
            "How to track a patient from screening to treatment completion",
            "How to design a community health referral workflow",
            "How to calculate treatment adherence and loss to follow-up",
            "How to build a community health worker dashboard",
            "What data should a health nonprofit collect",
        ],
    },
    {
        "slug": "mental-health",
        "name": "Mental Health",
        "guides": [
            "Mental health counselling case management systems",
            "Stepped-care assessment and referral workflows",
            "Counselling session and outcome tracking software",
            "Mental health crisis escalation and safeguarding workflows",
            "Consent privacy and access controls for mental health data",
        ],
        "questions": [
            "How to track mental health outcomes without over-collecting data",
            "How to design a stepped-care referral pathway",
            "How to protect counselling notes in a nonprofit MIS",
            "How to track missed sessions and safe follow-up",
            "What data should a mental health nonprofit collect",
        ],
    },
    {
        "slug": "maternal-child-health",
        "name": "Maternal and Child Health",
        "guides": [
            "Pregnancy and antenatal care tracking systems",
            "High-risk pregnancy referral and follow-up MIS",
            "Birth newborn and postnatal care tracking software",
            "Child immunisation and growth-monitoring dashboards",
            "Frontline maternal health worker caseload systems",
        ],
        "questions": [
            "How to track antenatal care visits and missed follow-ups",
            "How to flag and escalate high-risk pregnancies",
            "How to link mother and child records safely",
            "How to calculate immunisation completion and dropout",
            "What data should a maternal and child health programme collect",
        ],
    },
    {
        "slug": "child-protection",
        "name": "Child Rights and Protection",
        "guides": [
            "Child protection case management systems",
            "Child safeguarding incident and referral workflows",
            "Individual care plan and review tracking software",
            "Child protection risk and caseload dashboards",
            "Care-leaver transition and aftercare tracking systems",
        ],
        "questions": [
            "How to design a child protection case record",
            "How to control access to sensitive child-protection data",
            "How to track referrals without losing case ownership",
            "How to monitor care-plan reviews and overdue actions",
            "What data should a child protection NGO collect",
        ],
    },
    {
        "slug": "gender",
        "name": "Gender Equality and Women's Empowerment",
        "guides": [
            "Women's collective and group management systems",
            "Gender-based violence referral case management software",
            "Women's agency and decision-making outcome dashboards",
            "Safe-space participation and support tracking systems",
            "Women's economic empowerment programme MIS",
        ],
        "questions": [
            "How to measure women's agency in development programmes",
            "How to manage sensitive gender-based violence referral data",
            "How to track participation in women's collectives",
            "How to connect livelihoods and agency outcomes",
            "What data should a gender programme collect",
        ],
    },
    {
        "slug": "disability",
        "name": "Disability and Inclusion",
        "guides": [
            "Disability inclusion case management systems",
            "Assistive-device assessment and fulfilment tracking software",
            "Rehabilitation therapy and progress monitoring systems",
            "Inclusive education accommodation tracking dashboards",
            "Accessibility audit and reasonable-accommodation workflows",
        ],
        "questions": [
            "How to collect disability data using a rights-based approach",
            "How to track assistive devices from assessment to use",
            "How to record reasonable accommodations across programmes",
            "How to measure participation and inclusion outcomes",
            "What data should a disability inclusion NGO collect",
        ],
    },
    {
        "slug": "justice",
        "name": "Human Rights and Access to Justice",
        "guides": [
            "Legal aid case management systems for nonprofits",
            "Grievance intake triage and referral workflows",
            "Court hearing deadline and document tracking software",
            "Community paralegal outreach and case-tracking MIS",
            "Remedy enforcement and case-outcome dashboards",
        ],
        "questions": [
            "How to design a legal-aid case management workflow",
            "How to track court dates deadlines and case documents",
            "How to protect client confidentiality in legal-aid systems",
            "How to measure whether a legal remedy was enforced",
            "What data should an access-to-justice NGO collect",
        ],
    },
    {
        "slug": "environment",
        "name": "Environment and Climate",
        "guides": [
            "Ecological restoration survival tracking systems",
            "Biodiversity observation and monitoring databases",
            "Community conservation participation MIS",
            "Climate adaptation project monitoring dashboards",
            "Environmental grant and field-evidence management systems",
        ],
        "questions": [
            "How to track tree survival instead of only trees planted",
            "How to design a biodiversity monitoring data model",
            "How to combine field observations and geospatial evidence",
            "How to track community participation in conservation",
            "What data should an environmental nonprofit collect",
        ],
    },
    {
        "slug": "waste",
        "name": "Waste Management and Circularity",
        "guides": [
            "Waste collection route and service tracking systems",
            "Waste-worker registration safety and earnings MIS",
            "Material recovery facility operations dashboards",
            "Extended producer responsibility reporting systems",
            "Circular livelihoods and enterprise tracking software",
        ],
        "questions": [
            "How to track waste from collection to recovery",
            "How to measure waste-worker income and safety outcomes",
            "How to reconcile route weights and facility weights",
            "How to build an EPR evidence trail",
            "What data should a waste-management nonprofit collect",
        ],
    },
    {
        "slug": "food-systems",
        "name": "Food Systems and Nutrition",
        "guides": [
            "Farmer advisory and service-delivery MIS",
            "Farm input credit and repayment tracking systems",
            "Producer procurement and market traceability software",
            "School meal kitchen and distribution monitoring systems",
            "Nutrition screening and outcome dashboards",
        ],
        "questions": [
            "How to track farmer services across a crop cycle",
            "How to monitor school-meal delivery and food safety",
            "How to link procurement records to farmer payments",
            "How to measure nutrition outcomes without duplicate records",
            "What data should a food-systems nonprofit collect",
        ],
    },
    {
        "slug": "community-development",
        "name": "Community Development",
        "guides": [
            "Community needs and household profiling systems",
            "Participatory village planning and action tracking software",
            "Community institution and committee management MIS",
            "Government-scheme referral and convergence tracking systems",
            "Community infrastructure and asset maintenance dashboards",
        ],
        "questions": [
            "How to create a community profile without over-collecting data",
            "How to track priorities from community meeting to completion",
            "How to measure who participated in a village plan",
            "How to monitor referrals to government schemes",
            "What data should a community-development NGO collect",
        ],
    },
    {
        "slug": "media",
        "name": "Media and Journalism",
        "guides": [
            "Public-interest journalism story pipeline systems",
            "Source safety consent and contact management workflows",
            "Fact-check correction and editorial review tracking software",
            "Audience engagement and journalism impact dashboards",
            "Media grant deliverable and publication operations MIS",
        ],
        "questions": [
            "How to manage an investigative story pipeline",
            "How to protect source identities in editorial systems",
            "How to track corrections and editorial accountability",
            "How to measure public-interest journalism impact",
            "What data should a media nonprofit collect",
        ],
    },
    {
        "slug": "arts",
        "name": "Arts and Culture",
        "guides": [
            "Artist application grant and residency management systems",
            "Arts programme attendance and participant tracking software",
            "Venue collection and cultural-asset management systems",
            "Digital archive rights and permissions workflows",
            "Artist livelihood audience and career outcome dashboards",
        ],
        "questions": [
            "How to manage artist applications and selection fairly",
            "How to track rights and permissions for a digital archive",
            "How to measure artist livelihood and career outcomes",
            "How to connect audience data across events and programmes",
            "What data should an arts nonprofit collect",
        ],
    },
]


SERVICE_GROUPS = {
    "programme-systems": [
        "Nonprofit MIS software",
        "NGO monitoring and evaluation software",
        "Custom case management for nonprofits",
        "Offline field data collection for nonprofits",
        "Nonprofit dashboard development",
        "Donor reporting automation",
        "Nonprofit CRM implementation",
        "Fundraising CRM for nonprofits",
        "Grant management software for nonprofits",
        "Nonprofit HRMS",
        "NGO data migration services",
        "Nonprofit systems integration",
    ],
    "zolabs": [
        "AI voice surveys for NGOs",
        "Multilingual beneficiary feedback systems",
        "AI-powered baseline and endline interviews",
        "Alumni outcome verification with voice AI",
        "Post-training placement follow-up calls",
        "Voice-based impact evaluations",
        "AI voice interviews in Indian languages",
        "AI phone surveys versus traditional CATI",
    ],
    "zolashield": [
        "DPDP compliance for NGOs",
        "DPDP readiness assessment for nonprofits",
        "Nonprofit data mapping services",
        "Consent management implementation for NGOs",
        "Zoho DPDP compliance implementation",
        "Nonprofit privacy impact assessments",
        "Beneficiary data protection systems",
        "DPDP implementation consulting",
    ],
    "dozai": [
        "AI agents for nonprofits",
        "AI employees for NGOs",
        "Nonprofit workflow automation with AI",
        "AI grant application screening",
        "AI scholarship screening",
        "AI monitoring and evaluation assistants",
        "Custom AI agent development for nonprofits",
        "Human-in-the-loop AI workflows",
    ],
    "audiences": [
        "Technology for CSR teams",
        "Data platforms for foundations",
        "Digital transformation for nonprofit networks",
        "Technology implementation for social enterprises",
    ],
}


MISSION_GROUPS = {
    "scholarships": [
        "Scholarship application eligibility screening",
        "Scholarship document completeness review",
        "Scholarship interview scheduling and preparation",
        "Scholarship shortlist evidence packs",
        "Scholarship exception and appeal review",
    ],
    "placement-retention": [
        "Employment placement verification",
        "90-day and 180-day retention follow-up",
        "Employer confirmation and evidence collection",
        "Alumni employment and wage progression follow-up",
        "Placement exception escalation and review",
    ],
    "grants": [
        "Grant applicant due-diligence preparation",
        "Grantee eligibility and risk screening",
        "Grant reporting completeness review",
        "Grant compliance evidence checks",
        "Grantee monitoring and escalation",
    ],
    "mel": [
        "MEL survey design assistant",
        "MEL data quality assistant",
        "Qualitative interview coding support",
        "Outcome analysis and reporting assistant",
        "Indicator definition and evidence review",
    ],
    "fundraising": [
        "Institutional donor research",
        "Donor qualification and prioritisation",
        "Proposal research and drafting support",
        "Fundraising CRM enrichment",
        "Donor follow-up and next-action preparation",
    ],
    "programme-operations": [
        "Attendance exception review",
        "Programme case follow-up preparation",
        "Referral closure follow-up",
        "Document and consent completeness checks",
        "Field-team action queue preparation",
    ],
    "governance": [
        "Reusable AI skill design",
        "AI mission governance and role design",
        "AI output evaluation and quality assurance",
        "AI audit trail and evidence management",
        "Human escalation and override design",
    ],
}


TECH_GROUPS = {
    "zoho-creator": [
        "Zoho Creator for nonprofits",
        "Building an NGO MIS with Zoho Creator",
        "Offline data collection with Zoho Creator",
        "Case management with Zoho Creator",
        "Zoho Creator permissions for nonprofit teams",
        "Zoho Creator portals for programme partners",
        "Zoho Creator reporting for donor requirements",
        "Zoho Creator versus spreadsheets for NGO operations",
    ],
    "zoho-crm": [
        "Zoho CRM for nonprofits",
        "Nonprofit donor management with Zoho CRM",
        "CSR partnership pipeline in Zoho CRM",
        "Grant opportunity tracking in Zoho CRM",
        "WhatsApp integration with Zoho CRM for nonprofits",
        "Volunteer management with Zoho CRM",
        "Zoho CRM permissions and consent for nonprofits",
        "Migrating nonprofit contacts into Zoho CRM",
    ],
    "zoho-operations": [
        "Zoho People for NGO HRMS",
        "Multi-location nonprofit attendance with Zoho People",
        "Grant expense tracking with Zoho Books",
        "Restricted-fund reporting with Zoho Books",
        "Donor dashboards with Zoho Analytics",
        "Programme dashboards with Zoho Analytics",
        "Connecting Zoho Creator CRM Books and Analytics",
    ],
    "ai-integrations": [
        "Zoho MCP for nonprofit workflows",
        "AI agents connected to nonprofit CRM data",
        "Voice AI integrations for programme MIS",
        "AI-assisted data quality checks in Zoho",
        "Human-reviewed AI workflows in CRM",
        "Claude-managed agents for nonprofit operations",
        "Secure AI integrations for beneficiary data",
    ],
    "architecture-data": [
        "Nonprofit data migration planning",
        "Roles and permissions for nonprofit systems",
        "Nonprofit system integration architecture",
        "Designing a nonprofit programme data model",
        "Master data and unique IDs for nonprofit programmes",
    ],
}


RESOURCE_GROUPS = {
    "template": [
        "Nonprofit MIS requirements template",
        "Education programme indicator tracker",
        "Skilling placement and retention tracker",
        "Livelihoods baseline questionnaire",
        "Donor reporting dashboard template",
        "Nonprofit data dictionary template",
        "Programme risk register template",
        "Grant utilisation reporting template",
        "Nonprofit technology budget template",
        "Field data collection checklist",
    ],
    "tool": [
        "Nonprofit MIS cost estimator",
        "Build versus buy decision tool for nonprofit systems",
        "Nonprofit digital maturity assessment",
        "Nonprofit AI readiness assessment",
        "Placement retention calculator",
        "Survey sample size calculator",
        "Programme data quality scorecard",
        "DPDP readiness checklist for nonprofits",
        "AI voice survey cost calculator",
        "Nonprofit CRM selection scorecard",
    ],
    "framework": [
        "Theory of Change to data model guide",
        "Nonprofit MIS implementation roadmap",
        "Monitoring and evaluation indicator library",
        "Nonprofit CRM migration playbook",
        "Field team digital adoption toolkit",
        "Responsible AI implementation checklist",
        "Data protection and consent checklist",
        "Donor reporting requirements guide",
        "Nonprofit software vendor evaluation scorecard",
        "AI mission design canvas",
    ],
}


COMPARISONS = [
    "Zoho Creator versus Salesforce for nonprofits",
    "Custom MIS versus off-the-shelf NGO software",
    "Zoho CRM versus spreadsheets for donor management",
    "KoboToolbox versus Zoho Creator",
    "AI voice surveys versus human enumerators",
    "Build versus buy for nonprofit data systems",
    "WhatsApp surveys versus phone interviews",
    "Zoho Creator versus Power Apps for nonprofits",
    "Salesforce Nonprofit Cloud versus Zoho CRM",
    "Custom case management versus generic CRM",
    "Mobile apps versus mobile web forms for field data",
    "Centralised versus federated nonprofit data systems",
    "Real-time dashboards versus monthly reporting",
    "Biometric attendance versus privacy-respecting alternatives",
    "AI-assisted data review versus manual quality checks",
    "Voice AI versus IVR for beneficiary follow-up",
    "In-house technology team versus implementation partner",
    "One integrated platform versus specialised tools",
    "Open-source versus commercial nonprofit software",
    "When should an NGO invest in an MIS",
]


IMPLEMENTATION_INSIGHTS = [
    "What we learn before replacing a nonprofit spreadsheet system",
    "Lessons from designing one connected beneficiary record",
    "Why nonprofit MIS projects stall after launch",
    "How field-team adoption changes a data-system design",
    "What multi-state nonprofits need from roles and permissions",
    "Designing donor reports without distorting programme work",
    "What makes a nonprofit dashboard useful in review meetings",
    "Lessons from migrating years of inconsistent programme data",
    "How to introduce unique IDs without disrupting field operations",
    "What good implementation handover looks like",
    "Designing offline workflows for unreliable connectivity",
    "How to keep case-management systems humane",
    "What changes when a programme works through partner NGOs",
    "Building consent and privacy into everyday workflows",
    "How to decide which alerts deserve staff attention",
    "What voice interviews can and cannot verify",
    "Designing AI workflows around evidence and exceptions",
    "How to pilot an AI mission before scaling it",
    "What to measure during the first 90 days of an MIS",
    "How reusable modules reduce risk without forcing sameness",
]


TRUST_PAGES = [
    "How ImpactOS guides EdZola implementations",
    "The MAP framework for nonprofit technology decisions",
    "EdZola data privacy and security principles",
    "Human oversight in EdZola AI systems",
    "Data ownership portability and exit planning",
    "EdZola implementation and quality-assurance method",
    "Accessibility standards for EdZola systems",
    "How EdZola validates AI outputs",
    "EdZola sector experience and evidence standards",
    "How EdZola publishes corrections and content updates",
]


PHASE_ONE_TITLES = {
    "Nonprofit MIS software",
    "NGO monitoring and evaluation software",
    "Offline field data collection for nonprofits",
    "Nonprofit CRM implementation",
    "DPDP compliance for NGOs",
    "AI voice surveys for NGOs",
    "AI agents for nonprofits",
    "Technology for CSR teams",
    "Zoho Creator for nonprofits",
    "Custom MIS versus off-the-shelf NGO software",
    "Foundational literacy and numeracy tracking software",
    "School attendance and dropout early-warning systems",
    "Placement verification and retention systems for skilling programmes",
    "Household graduation tracking systems",
    "Community health worker case management systems",
    "Pregnancy and antenatal care tracking systems",
    "Child protection case management systems",
    "Women's collective and group management systems",
    "Disability inclusion case management systems",
    "Community needs and household profiling systems",
    "Scholarship application eligibility screening",
    "Employment placement verification",
    "90-day and 180-day retention follow-up",
    "MEL data quality assistant",
    "Human escalation and override design",
    "Nonprofit MIS requirements template",
    "Skilling placement and retention tracker",
    "Nonprofit MIS cost estimator",
    "Theory of Change to data model guide",
    "Nonprofit MIS implementation roadmap",
}


def add_page(pages, *, page_id, title, content_type, cluster, path, parent, intent,
             audience, sector="", evidence="internal-review-required", source_pages=""):
    pages.append({
        "page_id": page_id,
        "language": "en",
        "content_type": content_type,
        "cluster": cluster,
        "sector": sector,
        "working_title": title,
        "localized_title": title,
        "path": path,
        "parent_path": parent,
        "primary_intent": intent,
        "primary_audience": audience,
        "rollout_phase": "",
        "priority": "high" if title in PHASE_ONE_TITLES else "medium",
        "source_pages": source_pages,
        "evidence_status": evidence,
        "publication_status": "pilot-built" if title in PHASE_ONE_TITLES else "planned",
        "source_page_id": "",
        "localization_note": "",
    })


def build_english_pages():
    pages = []
    for sector in SECTORS:
        for title in sector["guides"]:
            add_page(
                pages,
                page_id=f"sector-{sector['slug']}-guide-{slugify(title)}",
                title=title,
                content_type="sector-guide",
                cluster="sector-deep-dive",
                sector=sector["name"],
                path=f"/{sector['slug']}/guides/{slugify(title)}/",
                parent=f"/{sector['slug']}/",
                intent="implementation",
                audience="programme and MEL leaders",
                source_pages=f"/{sector['slug']}/",
            )
        for title in sector["questions"]:
            add_page(
                pages,
                page_id=f"sector-{sector['slug']}-question-{slugify(title)}",
                title=title,
                content_type="sector-explainer",
                cluster="sector-question",
                sector=sector["name"],
                path=f"/{sector['slug']}/questions/{slugify(title)}/",
                parent=f"/{sector['slug']}/",
                intent="informational",
                audience="programme and MEL teams",
                source_pages=f"/{sector['slug']}/",
            )

    for group, titles in SERVICE_GROUPS.items():
        for title in titles:
            add_page(
                pages,
                page_id=f"solution-{slugify(title)}",
                title=title,
                content_type="solution-landing",
                cluster=group,
                path=f"/solutions/{slugify(title)}/",
                parent="/solutions/",
                intent="commercial",
                audience="nonprofit, foundation and CSR decision-makers",
                evidence="claims-review-required",
                source_pages="/;/impact-os/;/dozai/;/zolabs/;/zolashield/",
            )

    for group, titles in MISSION_GROUPS.items():
        for title in titles:
            add_page(
                pages,
                page_id=f"mission-{slugify(title)}",
                title=title,
                content_type="dozai-mission",
                cluster=group,
                path=f"/dozai/missions/{slugify(title)}/",
                parent="/dozai/",
                intent="solution-evaluation",
                audience="programme operations and AI leaders",
                evidence="availability-and-claims-review-required",
                source_pages="/dozai/;/dozai/missions/placement-retention/",
            )

    for group, titles in TECH_GROUPS.items():
        for title in titles:
            add_page(
                pages,
                page_id=f"technology-{slugify(title)}",
                title=title,
                content_type="technology-guide",
                cluster=group,
                path=f"/learn/technology/{slugify(title)}/",
                parent="/learn/technology/",
                intent="technology-evaluation",
                audience="nonprofit technology and operations teams",
                evidence="product-capability-verification-required",
                source_pages="/impact-os/",
            )

    for group, titles in RESOURCE_GROUPS.items():
        for title in titles:
            add_page(
                pages,
                page_id=f"resource-{slugify(title)}",
                title=title,
                content_type=f"resource-{group}",
                cluster="resource-library",
                path=f"/resources/{slugify(title)}/",
                parent="/resources/",
                intent="practical-resource",
                audience="nonprofit practitioners",
                evidence="worked-example-required",
                source_pages="/impact-os/;/sectors/",
            )

    for title in COMPARISONS:
        add_page(
            pages,
            page_id=f"comparison-{slugify(title)}",
            title=title,
            content_type="comparison",
            cluster="buying-guide",
            path=f"/learn/compare/{slugify(title)}/",
            parent="/learn/compare/",
            intent="comparison",
            audience="technology buyers and nonprofit leaders",
            evidence="current-product-research-required",
            source_pages="/impact-os/",
        )

    for title in IMPLEMENTATION_INSIGHTS:
        add_page(
            pages,
            page_id=f"insight-{slugify(title)}",
            title=title,
            content_type="implementation-insight",
            cluster="implementation-evidence",
            path=f"/case-studies/implementation-lessons/{slugify(title)}/",
            parent="/case-studies/",
            intent="evidence-and-learning",
            audience="nonprofit and foundation leaders",
            evidence="client-evidence-and-anonymisation-review-required",
            source_pages="/impact-os/;/thinking/",
        )

    for title in TRUST_PAGES:
        add_page(
            pages,
            page_id=f"trust-{slugify(title)}",
            title=title,
            content_type="methodology-trust",
            cluster="trust",
            path=f"/about/methods/{slugify(title)}/",
            parent="/about/",
            intent="trust-and-due-diligence",
            audience="partners, procurement and governance teams",
            evidence="leadership-approval-required",
            source_pages="/about/;/impact-os/;/why/",
        )

    if len(pages) != 350:
        raise ValueError(f"Expected 350 English pages, found {len(pages)}")
    return pages


LANGUAGE_PLANS = {
    "hi": ("Hindi", 40, ["mis", "field", "education", "livelihood", "dpdp", "voice", "health", "community"]),
    "ta": ("Tamil", 30, ["mis", "group", "education", "crm", "field", "health", "livelihood"]),
    "te": ("Telugu", 20, ["skilling", "livelihood", "community", "beneficiary", "placement", "field"]),
    "kn": ("Kannada", 15, ["mis", "donor", "digital", "field", "crm"]),
    "mr": ("Marathi", 15, ["programme", "skilling", "field", "dpdp", "placement"]),
    "bn": ("Bengali", 10, ["education", "livelihood", "community", "monitoring"]),
    "fr": ("French", 10, ["mis", "impact", "grant", "ai", "monitoring"]),
}


def build_localized_pages(english_pages):
    localized = []
    used_by_language = defaultdict(set)
    for code, (language_name, count, focus) in LANGUAGE_PLANS.items():
        def score(page):
            haystack = f"{page['working_title']} {page['cluster']} {page['sector']}".lower()
            focus_score = sum(3 for word in focus if word in haystack)
            priority_score = 5 if page["priority"] == "high" else 0
            type_score = 2 if page["content_type"] in {"solution-landing", "sector-guide", "sector-explainer"} else 0
            return (focus_score + priority_score + type_score, page["page_id"])

        selected = sorted(english_pages, key=score, reverse=True)[:count]
        for source in selected:
            if source["page_id"] in used_by_language[code]:
                raise ValueError("Duplicate localized source selection")
            used_by_language[code].add(source["page_id"])
            localized.append({
                **source,
                "page_id": f"loc-{code}-{source['page_id']}",
                "language": code,
                "localized_title": "",
                "path": f"/{code}{source['path']}",
                "parent_path": f"/{code}{source['parent_path']}",
                "rollout_phase": "4",
                "priority": "medium",
                "publication_status": "localization-planned",
                "source_page_id": source["page_id"],
                "localization_note": (
                    f"Professional {language_name} localisation required; adapt examples, "
                    "programme vocabulary and CTA, then add reciprocal hreflang."
                ),
            })
    if len(localized) != 140:
        raise ValueError(f"Expected 140 localized pages, found {len(localized)}")
    return localized


def assign_rollout(english_pages):
    phase_one = [p for p in english_pages if p["working_title"] in PHASE_ONE_TITLES]
    if len(phase_one) != 30:
        missing = PHASE_ONE_TITLES - {p["working_title"] for p in english_pages}
        raise ValueError(f"Expected 30 phase-one pages, found {len(phase_one)}; missing={missing}")

    def rank(page):
        type_order = {
            "solution-landing": 0,
            "sector-guide": 1,
            "sector-explainer": 2,
            "dozai-mission": 3,
            "technology-guide": 4,
            "resource-template": 5,
            "resource-tool": 5,
            "resource-framework": 5,
            "comparison": 6,
            "implementation-insight": 7,
            "methodology-trust": 8,
        }
        return (type_order.get(page["content_type"], 9), page["page_id"])

    remaining = sorted([p for p in english_pages if not p["rollout_phase"]], key=rank)
    phase_one_ids = {p["page_id"] for p in phase_one}
    for page in english_pages:
        if page["page_id"] in phase_one_ids:
            page["rollout_phase"] = "1"
    remaining = [p for p in remaining if p["page_id"] not in phase_one_ids]
    for i, page in enumerate(remaining):
        page["rollout_phase"] = "2" if i < 70 else "3" if i < 220 else "4"


QUESTION_PATTERNS = {
    "sector-guide": [
        ("implementation", "How should a nonprofit implement {topic}?"),
        ("data-model", "What records and data fields are needed for {topic}?"),
        ("workflow", "Which staff roles and review steps should {topic} include?"),
        ("risk", "What are the most common mistakes when setting up {topic}?"),
        ("scale", "How should {topic} change for a small NGO versus a multi-state programme?"),
    ],
    "sector-explainer": [
        ("direct-answer", "{title}?"),
        ("minimum-viable", "What is the minimum viable way to answer: {title}?"),
        ("indicators", "Which indicators and definitions matter when asking: {title}?"),
        ("exceptions", "How should a nonprofit handle missing data and exceptions when asking: {title}?"),
        ("evidence", "What evidence would make the answer to '{title}?' credible to a donor?"),
    ],
    "solution-landing": [
        ("fit", "What operational problems can {topic} address?"),
        ("requirements", "What should a strong {topic} approach include?"),
        ("cost", "What drives the cost and timeline of {topic}?"),
        ("vendor-selection", "How should an NGO evaluate a partner for {topic}?"),
        ("readiness", "When is a nonprofit ready to invest in {topic}?"),
    ],
    "dozai-mission": [
        ("ai-fit", "Can AI safely help a nonprofit with {topic}?"),
        ("inputs", "What information does an AI mission for {topic} need?"),
        ("human-oversight", "What can AI execute and what must a person decide in {topic}?"),
        ("auditability", "What evidence and audit trail should {topic} produce?"),
        ("limitations", "Where can an AI mission for {topic} fail or require escalation?"),
    ],
    "technology-guide": [
        ("capability", "Can {topic} support a real nonprofit operating workflow?"),
        ("architecture", "How should a nonprofit configure {topic}?"),
        ("integration", "What data and integrations are needed for {topic}?"),
        ("limitations", "What are the limitations and maintenance needs of {topic}?"),
        ("selection", "When should an NGO choose {topic} instead of another approach?"),
    ],
    "resource": [
        ("use", "How should a nonprofit use the {topic}?"),
        ("contents", "What fields or sections should the {topic} contain?"),
        ("ownership", "Who should complete and maintain the {topic}?"),
        ("adaptation", "How can the {topic} be adapted for different programme sizes?"),
        ("quality", "How can a team check that the {topic} is complete and useful?"),
    ],
    "comparison": [
        ("decision", "{title}: which option suits which type of nonprofit?"),
        ("cost", "How do the cost and implementation effort compare for {topic}?"),
        ("capability", "How do the options compare on field work, reporting and permissions for {topic}?"),
        ("tradeoff", "What trade-offs are easy to miss in {topic}?"),
        ("switching", "When should a nonprofit switch approaches after comparing {topic}?"),
    ],
    "implementation-insight": [
        ("lesson", "What practical lessons does EdZola have about {topic}?"),
        ("warning", "What usually goes wrong when teams deal with {topic}?"),
        ("decision", "Which decisions matter most in {topic}?"),
        ("evidence", "What evidence should an implementation team keep about {topic}?"),
        ("transfer", "Which lessons from {topic} apply across nonprofit sectors?"),
    ],
    "methodology-trust": [
        ("method", "How does EdZola approach {topic}?"),
        ("governance", "Who is accountable for {topic} at EdZola?"),
        ("evidence", "What evidence can a partner request about {topic}?"),
        ("limitations", "What limitations or exceptions apply to {topic}?"),
        ("assurance", "How can a nonprofit verify EdZola's claims about {topic}?"),
    ],
}


QUESTION_OVERRIDES = {
    ("Custom MIS versus off-the-shelf NGO software", "decision"):
        "When should a nonprofit choose a custom MIS instead of off-the-shelf software?",
    ("Custom MIS versus off-the-shelf NGO software", "cost"):
        "How do custom and off-the-shelf systems compare on cost and implementation effort?",
    ("Custom MIS versus off-the-shelf NGO software", "capability"):
        "How do custom and off-the-shelf systems compare on field work, reporting and permissions?",
    ("Custom MIS versus off-the-shelf NGO software", "tradeoff"):
        "Which ownership and exit trade-offs are easy to miss?",
    ("Custom MIS versus off-the-shelf NGO software", "switching"):
        "When should a nonprofit replace its current software approach?",
    ("Zoho Creator for nonprofits", "capability"):
        "Can Zoho Creator support a nonprofit's actual operating workflow?",
    ("Zoho Creator for nonprofits", "architecture"):
        "How should a nonprofit structure a Zoho Creator application?",
    ("Zoho Creator for nonprofits", "integration"):
        "Which data and integrations does a Zoho Creator application need?",
    ("Zoho Creator for nonprofits", "limitations"):
        "What are Zoho Creator's limitations and maintenance needs?",
    ("Zoho Creator for nonprofits", "selection"):
        "When should an NGO choose Zoho Creator over another approach?",
    ("Human escalation and override design", "ai-fit"):
        "When should an AI workflow hand a case to a person?",
    ("Human escalation and override design", "inputs"):
        "What information should be passed during an AI-to-human escalation?",
    ("Human escalation and override design", "human-oversight"):
        "Which actions can AI pause or prepare, and which require a person?",
    ("Human escalation and override design", "auditability"):
        "What should an escalation and override audit trail record?",
    ("Human escalation and override design", "limitations"):
        "What can go wrong when escalation and override rules are unclear?",
}


def topic_form(title):
    topic = title.rstrip("?.")
    for prefix in ("How to ", "What ", "When ", "Why "):
        if topic.startswith(prefix):
            topic = topic[len(prefix):]
            break
    first_word = topic.split(maxsplit=1)[0]
    if first_word.isupper() or first_word in {"EdZola", "ImpactOS", "Zoho", "KoboToolbox", "WhatsApp", "DozAI", "Zolabs", "ZolaShield", "Theory"}:
        return topic
    return topic[:1].lower() + topic[1:]


def questions_for(page, count):
    kind = page["content_type"]
    if kind.startswith("resource-"):
        patterns = QUESTION_PATTERNS["resource"]
    else:
        patterns = QUESTION_PATTERNS[kind]
    title = page["working_title"].rstrip("?.")
    topic = topic_form(title)
    result = []
    for family, pattern in patterns[:count]:
        question = QUESTION_OVERRIDES.get((title, family), pattern.format(title=title, topic=topic))
        question = re.sub(r"\s+", " ", question)
        result.append((family, question))
    return result


def build_question_bank(english_pages):
    ordered = sorted(
        english_pages,
        key=lambda p: (int(p["rollout_phase"]), 0 if p["priority"] == "high" else 1, p["page_id"]),
    )
    questions = []
    for index, page in enumerate(ordered):
        count = 5 if index < 100 else 4
        for family, question in questions_for(page, count):
            questions.append({
                "question_id": f"q-{len(questions)+1:04d}",
                "page_id": page["page_id"],
                "language": "en",
                "question": question,
                "question_family": family,
                "sector": page["sector"],
                "audience": page["primary_audience"],
                "journey_stage": page["primary_intent"],
                "answer_path": page["path"],
                "priority": page["priority"],
                "answer_status": "page-answered" if page["working_title"] in PHASE_ONE_TITLES else "planned",
                "evidence_needed": page["evidence_status"],
            })
    if len(questions) != 1500:
        raise ValueError(f"Expected 1,500 questions, found {len(questions)}")
    if len({q["question"] for q in questions}) != len(questions):
        repeats = [q for q, n in Counter(x["question"] for x in questions).items() if n > 1]
        raise ValueError(f"Duplicate question text: {repeats[:5]}")
    return questions


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(pages, questions):
    languages = Counter(p["language"] for p in pages)
    content_types = Counter(p["content_type"] for p in pages if p["language"] == "en")
    phases = Counter(p["rollout_phase"] for p in pages)
    sample_questions = [q for q in questions if q["answer_status"] == "page-answered"]
    text = f"""# EdZola content expansion registry

Generated by `scripts/build-content-expansion.py`. The registry is a backlog, not an instruction to publish every URL.

## Locked scope

- **350 English page opportunities**: 160 sector pages, 40 solution pages, 35 DozAI missions, 35 technology guides, 30 resources, 20 comparisons, 20 implementation insights and 10 trust pages.
- **140 localisation opportunities**: 40 Hindi, 30 Tamil, 20 Telugu, 15 Kannada, 15 Marathi, 10 Bengali and 10 French. Every localisation remains blocked until a fluent reviewer adapts the terminology and examples.
- **1,500 English natural-language questions** mapped to the English backlog. Questions are research and coverage prompts; they are not 1,500 proposed URLs.
- **30-page pilot built**: ten solution pages, ten sector guides, five DozAI mission pages, and five resources.

## Rollout gates

| Phase | Scope | Page opportunities |
| --- | --- | ---: |
| 1 | Prove the model: commercial, sector, mission and resource pages | {phases['1']} |
| 2 | Reach 100 cumulative English opportunities | {phases['2']} |
| 3 | Reach 250 cumulative English opportunities | {phases['3']} |
| 4 | Remaining English backlog plus localised backlog | {phases['4']} |

Publishing is conditional on intent differentiation, source sufficiency, human review, working internal links and indexability checks. Case-study claims require evidence and client permission. Product and legal pages require date-stamped verification.

## English page mix

| Content type | Count |
| --- | ---: |
""" + "\n".join(f"| {key} | {value} |" for key, value in sorted(content_types.items())) + """

## Language mix

| Language | Count |
| --- | ---: |
""" + "\n".join(f"| {key} | {value} |" for key, value in sorted(languages.items())) + f"""

## Sample-page questions

""" + "\n".join(f"- {row['question']}" for row in sample_questions) + """

## Fields that prevent mass-produced thin content

- `primary_intent` and `parent_path` make cannibalisation review possible.
- `source_pages` identifies the internal source material a writer must inspect.
- `evidence_status` prevents unsupported claims from silently becoming publishable copy.
- `publication_status` separates a planned URL from a reviewed page.
- `source_page_id` and `localization_note` keep localised pages tied to reviewed English sources without treating translation as word substitution.
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def main():
    english = build_english_pages()
    assign_rollout(english)
    localized = build_localized_pages(english)
    pages = english + localized
    questions = build_question_bank(english)
    write_csv(OUT / "content-registry.csv", pages)
    write_csv(OUT / "question-bank.csv", questions)
    write_summary(pages, questions)
    print(f"Wrote {len(pages)} page opportunities and {len(questions)} questions to {OUT}")


if __name__ == "__main__":
    main()
