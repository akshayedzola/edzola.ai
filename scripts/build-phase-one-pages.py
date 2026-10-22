#!/usr/bin/env python3
"""Generate the approved 30-page EdZola search-content pilot.

The content registry remains the URL/intent source of truth. This generator adds
topic-specific operating detail, visible Q&A, JSON-LD and the shared Zoho CRM form.
"""

from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "content" / "expansion" / "content-registry.csv"
QUESTION_BANK = ROOT / "content" / "expansion" / "question-bank.csv"
TODAY = "2026-10-20"
DISPLAY_DATE = "20 October 2026"
SITE = "https://edzola.ai"
FORM_SCRIPT_VERSION = "20261022a"


def parts(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def brief(tagline, direct, central, records, steps, risks, measures, human, placeholder,
          help_default="Data Systems – MIS / ERP", form_question="What would you like this workflow to make easier?"):
    return {
        "tagline": tagline,
        "direct": direct,
        "central": central,
        "records": parts(records),
        "steps": parts(steps),
        "risks": parts(risks),
        "measures": parts(measures),
        "human": parts(human),
        "placeholder": placeholder,
        "help_default": help_default,
        "form_question": form_question,
    }


BRIEFS = {
    "Nonprofit MIS software": brief(
        "Connect the record, the work and the decision.",
        "Nonprofit MIS software is the operating record behind a programme. It joins intake, delivery, cases, consent, outcomes and follow-up around stable IDs, gives each role the right view and turns incomplete or risky records into work queues.",
        "person, household, institution or case",
        "identity and relationships|programme enrolment and status history|services, visits and assessments|cases, referrals and due actions|outcomes and verification status|consent, access and retention",
        "map the decisions and owners|define the central record and stable ID|prototype one complete journey|test permissions and field conditions|migrate useful data with a transformation log|review adoption and exceptions",
        "duplicated identities|reports that cannot be traced to source records|permissions added after sensitive data is loaded|a large first release nobody can test",
        "complete connected records|overdue actions resolved|duplicate and missing-data rates|time spent preparing review and donor reports",
        "eligibility and adverse action|safeguarding and crisis response|referral and case closure|interpretation of conflicting evidence",
        "our programme depends on several trackers, and we cannot see which participant, case or site needs attention next."
    ),
    "NGO monitoring and evaluation software": brief(
        "Make every indicator traceable to the work beneath it.",
        "Monitoring and evaluation software should connect each indicator to a definition, source record, reporting period, responsible role and review decision. Its purpose is not to produce more charts; it is to help teams notice missing evidence and respond sooner.",
        "indicator linked to source evidence",
        "results framework and indicator definition|participant or unit of analysis|baseline, milestone and endline observations|data-quality checks and exceptions|reporting obligation and due date|analysis notes, limitations and approvals",
        "agree decisions before indicators|document numerator, denominator and disaggregation|map each metric to a source workflow|build missingness and quality views|test a complete reporting cycle|review whether evidence changed a decision",
        "indicators without operational owners|changing definitions between reports|averages that hide attrition|AI-written narratives not checked against approved figures",
        "indicators produced without manual reconciliation|missingness visible before reporting|matched baseline-to-endline coverage|decisions recorded from review meetings",
        "accepting an outcome claim|changing an indicator definition|explaining bias or attrition|deciding programme adaptation",
        "our team spends days reconciling indicators, and managers see data-quality problems only when a report is due."
    ),
    "Offline field data collection for nonprofits": brief(
        "Design for the signal, device and language people actually have.",
        "Offline field data collection works when forms remain usable without a network, records have stable local IDs, sync conflicts are visible and field teams can correct mistakes safely. Offline capability is a workflow and support decision, not only a product checkbox.",
        "field interaction waiting to sync",
        "device and assigned user|local record ID and timestamp|form version and language|location or service point|attachments and consent evidence|sync status, conflict and correction history",
        "observe the real field visit|reduce the form to the next decision|define offline identity and duplicate rules|test long offline periods and shared devices|design sync and conflict review|monitor failed uploads and support requests",
        "two devices creating the same person|forms changing while records are offline|attachments failing silently|teams sharing credentials for convenience",
        "successful first-time sync|average time to complete a form|duplicate rate after sync|unresolved conflicts and failed attachments",
        "overriding a conflicting record|collecting sensitive evidence|deciding whether location is necessary|closing a case with incomplete data",
        "field teams work with patchy connectivity and shared phones, and delayed sync creates duplicates or lost follow-ups."
    ),
    "Nonprofit CRM implementation": brief(
        "Turn relationships and next actions into shared organisational memory.",
        "A nonprofit CRM should connect people and institutions to interactions, interests, proposals, donations or grants, commitments and next actions. Implementation succeeds when ownership and relationship practice improve, not when old spreadsheets are merely imported.",
        "person and organisation relationship",
        "contact and organisation|relationship owner and access|interaction and communication preference|opportunity, proposal or ask|donation, grant or commitment|next action, deadline and stewardship history",
        "map relationship journeys and handoffs|agree ownership and duplicate rules|configure the smallest useful pipeline|clean and stage migration|connect approved communication channels|run weekly pipeline and stewardship reviews",
        "treating every contact as a donor|mass importing without deduplication|unclear ownership after staff changes|automations that ignore consent or communication preference",
        "next actions with owners|duplicate organisation and contact rate|pipeline records updated on time|relationship history retained across ownership changes",
        "relationship strategy and ask timing|handling a sensitive donor concern|merging disputed duplicates|changing communication consent",
        "donor and partner history lives in inboxes, and follow-ups are missed when ownership changes.",
        help_default="CRM",
        form_question="Which relationship or fundraising workflow should the CRM make easier?"
    ),
    "AI voice surveys for NGOs": brief(
        "Reach more people without pretending a call is the same as human fieldwork.",
        "AI voice surveys can conduct structured multilingual calls, capture responses and prepare reviewable transcripts or coded outputs. They are most useful for high-volume, low-risk follow-up when consent, identity checks, nonresponse and human escalation are designed explicitly.",
        "consented interview attempt",
        "participant and safe contact window|language and consent state|question version and call attempt|audio or transcript access rule|response, uncertainty and evidence link|escalation, opt-out and reviewer decision",
        "define the research question and exclusions|test scripts with speakers of each language|pilot identity, consent and opt-out|review transcripts and coding errors|measure reach and nonresponse bias|scale with sampling and escalation controls",
        "misrecognition across accents|people answering on shared phones|leading translations|treating nonresponse as a negative outcome",
        "consent and completion rate|language-specific transcription quality|nonresponse by subgroup|cases escalated and resolved",
        "responding to distress or disclosure|interpreting ambiguous statements|deciding research validity|contacting someone where privacy is uncertain",
        "we need multilingual beneficiary follow-up at scale but must preserve consent, context and human review.",
        help_default="zolabs.ai – Qualitative Data Collection",
        form_question="What do you need to learn from people’s voices?"
    ),
    "DPDP compliance for NGOs": brief(
        "Turn legal obligations into everyday data practices.",
        "DPDP readiness for an NGO begins with knowing what personal data it holds, why it is used, who can access it, where it moves and when it should be deleted. A practical programme converts that map into notices, consent or other lawful processes, response workflows and accountable controls.",
        "personal-data processing activity",
        "data category and person affected|purpose and operating owner|collection channel and notice|systems, processors and transfers|access, retention and deletion|request, incident and grievance workflow",
        "map real data flows and shadow tools|prioritise high-risk and child data|confirm purposes, notices and consent practice|fix access and retention controls|exercise request and incident workflows|review evidence and ownership regularly",
        "copying generic policies without operational change|unknown spreadsheets and messaging groups|retaining data indefinitely|assuming a software setting equals compliance",
        "systems and datasets mapped|high-risk gaps assigned|access and deletion reviews completed|requests and incidents handled within the agreed process",
        "legal interpretation|accepting residual risk|responding to an incident|deciding exceptions and notices",
        "personal data sits across forms, drives and messaging groups, and we need a practical DPDP readiness plan.",
        help_default="zolashield – DPDP Compliance",
        form_question="Where does data protection feel unclear today?"
    ),
    "AI agents for nonprofits": brief(
        "Give AI a bounded job, evidence rules and a named reviewer.",
        "An AI agent for nonprofit work should execute a defined, repeatable job across approved information and tools, show the evidence behind its output and stop when a rule or risk requires a person. Start with one mission, not a vague digital employee.",
        "mission case with an outcome and audit trail",
        "mission objective and completion state|approved inputs and permissions|method, rules and examples|tool action and evidence|confidence, exception and escalation|reviewer decision and correction",
        "choose a high-volume bounded workflow|write completion and stop conditions|restrict tools and data|run in apprenticeship mode|evaluate errors by consequence|expand autonomy only after review",
        "a broad role with no completion test|hidden reasoning without source evidence|permissions larger than the job requires|automation continuing through a consequential exception",
        "cases completed correctly|exceptions handed over early|evidence attached to each output|review corrections declining without harm",
        "eligibility, rights, money or opportunity decisions|safeguarding and crisis judgement|approval of external communication|permission or policy changes",
        "we have a repetitive workflow that may suit AI, but need clear limits, evidence and human escalation.",
        help_default="Custom AI Solutions",
        form_question="Which bounded workflow would you like an AI agent to handle?"
    ),
    "Technology for CSR teams": brief(
        "Connect partner due diligence, grants, evidence and portfolio learning.",
        "Technology for CSR teams should create a dependable handoff from partner discovery and due diligence to grant obligations, programme evidence, utilisation and portfolio review. It should reduce duplicate requests to nonprofit partners while preserving the source and limits of every claim.",
        "partner-grant-programme relationship",
        "organisation and due-diligence profile|opportunity, proposal and decision|grant, budget and obligation|programme, indicator and evidence|disbursement, utilisation and variance|review, risk, learning and next action",
        "map the partner and grant lifecycle|standardise only essential evidence|separate partner self-report from verification|connect obligation and reporting calendars|build portfolio review views|improve requests using partner feedback",
        "asking partners for the same data repeatedly|mixing due-diligence risk with programme performance|dashboards without evidence links|automation that disadvantages smaller organisations",
        "duplicate requests removed|obligations completed on time|evidence traceability|portfolio decisions and follow-ups recorded",
        "funding and rejection decisions|interpreting contextual risk|responding to safeguarding concerns|approving outcome claims",
        "partner data, grant obligations and programme evidence are disconnected, creating repeated requests and late reviews."
    ),
    "Zoho Creator for nonprofits": brief(
        "Use low-code when the workflow needs configuration, ownership and change.",
        "Zoho Creator can support a nonprofit MIS or case workflow when the organisation needs tailored forms, linked records, role-based access, automation and reporting without maintaining a full custom codebase. Suitability depends on offline needs, licensing, integrations and internal ownership.",
        "configured application record",
        "form and linked data model|role, profile and record access|workflow rule and approval|report, page and dashboard|integration and scheduled job|change request, test and release history",
        "model the workflow outside the platform|prototype the central record|configure roles before importing data|test offline and integration constraints|document environments and releases|assign an internal product owner",
        "building screens before agreeing definitions|over-customising without release discipline|record permissions that are too broad|depending on one developer's memory",
        "workflow completion without workarounds|permission tests passed|automation failures resolved|documented changes and trained owners",
        "approval and policy decisions|access exceptions|merging disputed identities|accepting platform trade-offs",
        "we are considering Zoho Creator for an MIS and need to test workflow fit, offline use, permissions and ownership."
    ),
    "Custom MIS versus off-the-shelf NGO software": brief(
        "Compare operating fit, ownership and total change—not feature counts.",
        "Off-the-shelf software is usually stronger when the workflow is common and the organisation can adopt its model. A custom or low-code MIS is stronger when distinctive journeys, relationships, permissions or reporting logic are central to delivery. The decision should include implementation and long-term ownership.",
        "decision record with weighted requirements",
        "must-have workflow and exception|role and permission need|integration and migration constraint|configuration or customisation effort|licence, support and change cost|exit, export and ownership condition",
        "document the current and desired workflow|separate must-haves from preferences|test one real journey in each option|estimate three-year ownership|check export and exit terms|record the decision and assumptions",
        "buying on a polished demo|calling configuration free|ignoring adoption and migration|customising around a broken process",
        "critical workflow fit|time to first useful release|three-year cost and internal effort|ability to change and exit",
        "weighting requirements|accepting trade-offs|choosing procurement risk|approving the final platform",
        "we need an evidence-based custom-versus-product decision using our real workflow, not a generic feature checklist."
    ),
    "Foundational literacy and numeracy tracking software": brief(
        "Follow each learner from baseline level to demonstrated progress.",
        "FLN tracking software should connect a learner's baseline level, instructional group, attendance, periodic assessment and support action. It must preserve the assessment method and cohort changes so learning gain is not separated from participation or attrition.",
        "learner learning journey",
        "learner and guardian relationship|baseline skill and assessment version|group, facilitator and session attendance|periodic skill observation|level movement and support action|endline, attrition and verification",
        "agree skill progression and assessment rules|capture a trustworthy baseline|group learners without freezing labels|record attendance and short checks|review non-progress and absence together|report gain with attrition and missingness",
        "changing assessment versions without mapping|reporting only children with an endline|treating level as a fixed label|using automated scoring without facilitator review",
        "matched learner coverage|learning gain by starting level|attendance and assessment completion|support actions closed",
        "assigning remedial support|interpreting disability or language factors|overriding an assessment|communicating progress to families",
        "baseline and endline scores exist, but we cannot connect learning progress to attendance, group changes and support."
    ),
    "School attendance and dropout early-warning systems": brief(
        "Notice disengagement early enough for a safe response.",
        "An attendance early-warning system should combine recent absence, attendance trend, transition points and known context into a review queue. It should prompt a trained person to investigate; it should not label a child as a dropout or predict intent automatically.",
        "learner attendance and follow-up episode",
        "learner, school and class|session or daily attendance|reason and source of absence|transition or risk context|follow-up attempt and outcome|return, transfer, exit or unresolved status",
        "define absence and dropout carefully|use the least burdensome attendance source|set review thresholds with field teams|test false positives by subgroup|assign safe follow-up|close with evidence and reason",
        "paper registers entered twice|punitive use of risk scores|missing transfers counted as dropout|contact that exposes sensitive family information",
        "time from threshold to review|successful safe contact|documented return, transfer or exit|false-positive and unresolved rates",
        "whether and how to contact a family|safeguarding response|confirming transfer or dropout|changing support for a child",
        "attendance arrives late, and children who transfer or quietly disengage look identical in the report."
    ),
    "Placement verification and retention systems for skilling programmes": brief(
        "Separate offers, self-report, evidence and sustained work.",
        "Placement and retention systems should connect each candidate's training record to placement evidence, employer or self-employment verification and follow-up at defined intervals. Every outcome needs a state that distinguishes verified, self-reported, disputed, unreachable and requiring review.",
        "candidate employment outcome episode",
        "candidate and course completion|job or enterprise and start date|offer, payslip or employer evidence|follow-up attempt and response|30, 90 and 180-day status|dispute, nonresponse and reviewer decision",
        "define placement and retention states|capture consent and safe contact channels|verify initial placement evidence|schedule interval follow-ups|route conflicts and nonresponse|report denominators and verification status",
        "counting offers as placements|removing unreachable graduates from denominators|treating any employer response as proof|automated calls without language and privacy checks",
        "verified placement rate|retention by follow-up window|nonresponse and disputed cases|time reviewers spend on exceptions",
        "resolving disputed evidence|contacting an employer|interpreting informal or self-employment|support after job loss",
        "placement letters are recorded, but we cannot reliably verify who started work or stayed for 90 and 180 days."
    ),
    "Household graduation tracking systems": brief(
        "Track movement across capabilities without turning graduation into one opaque score.",
        "A household graduation system should connect a household baseline, services, shocks, milestones and repeated assessments across agreed dimensions. Graduation should remain a transparent programme judgement with visible criteria, evidence and exceptions.",
        "household graduation journey",
        "household and member relationships|baseline across agreed dimensions|service plan and receipt|income, asset and resilience observation|shock, referral and adaptation|graduation review, evidence and follow-up",
        "agree dimensions and evidence|create a stable household identity|record the service pathway|review progress and shocks together|conduct a documented graduation review|follow up for sustainability",
        "one composite score hiding trade-offs|income estimates treated as precise|household composition changes ignored|graduation used to end support automatically",
        "assessment coverage|milestones with current evidence|services matched to needs|sustained outcomes after graduation",
        "graduation and continuation decisions|interpreting household shocks|resolving conflicting income evidence|changing the support plan",
        "services and assessments sit in different trackers, making it hard to understand why a household did or did not graduate."
    ),
    "Community health worker case management systems": brief(
        "Give every worker a safe caseload and every referral an owner.",
        "A community health worker case system should connect household visits, screening, counselling, referrals and follow-up around a patient record while limiting access to the worker's assigned caseload. The system should surface overdue care without replacing clinical judgement.",
        "patient or household care episode",
        "person, household and safe contact|worker assignment and visit|screening result and protocol version|referral, facility and due date|service received and evidence|follow-up, closure and escalation",
        "map worker decisions and clinical boundaries|define minimum patient identity|build visit and referral workflow|test privacy on shared devices|connect facility confirmation where possible|review overdue and unresolved cases",
        "workers seeing unassigned patients|alerts without an escalation service|clinical interpretation embedded in code|unsafe contact after a sensitive screening",
        "assigned caseload reviewed|referrals completed|loss to follow-up|overdue actions resolved safely",
        "clinical diagnosis and treatment|urgent escalation|closing an unresolved referral|contact where privacy is uncertain",
        "visits and referrals are recorded, but workers cannot see a safe, current list of people who need follow-up."
    ),
    "Pregnancy and antenatal care tracking systems": brief(
        "Connect pregnancy, risk, referral and follow-up across home and facility.",
        "Pregnancy and ANC tracking software should keep one maternal record with gestational timeline, scheduled contacts, risk observations, referrals, facility services and outcomes. It should flag missed or urgent actions to trained staff without making clinical decisions.",
        "pregnancy care journey",
        "mother, pregnancy and estimated timeline|frontline visit and ANC contact|risk observation and protocol source|referral, facility and urgency|service confirmation and next due action|birth, postnatal and closure status",
        "agree timeline and service definitions|link home and facility identity|schedule contacts and referrals|test urgent escalation|reconcile facility confirmation|review maternal and newborn follow-up",
        "duplicate pregnancies across workers|risk alerts without response capacity|estimating clinical status from incomplete data|unsafe disclosure on shared phones",
        "ANC contacts completed on time|urgent referrals acknowledged|facility confirmation|postnatal follow-up completed",
        "clinical risk assessment|emergency response|changing the care plan|closing a pregnancy record after loss or transfer",
        "pregnancy visits, referrals and facility outcomes are tracked by different teams and do not reconcile."
    ),
    "Child protection case management systems": brief(
        "Keep the child’s safety, wishes and case history at the centre.",
        "Child protection case management software should connect intake, assessment, safety planning, referrals, reviews and closure with strict role-based access and a complete decision trail. It supports practitioners; it must not automate best-interest or safeguarding decisions.",
        "child protection case",
        "child identity and safe relationships|concern, intake and source|assessment and safety plan|action, referral and responsible person|review, change and evidence|closure, transition and restricted archive",
        "define access and escalation before configuration|model the case and review cycle|separate allegations from findings|test partner handoffs|monitor overdue safety actions|audit access and closure decisions",
        "broad access to narrative notes|automatic risk scoring used as judgement|referrals without confirmed ownership|records continuing beyond a justified retention period",
        "urgent actions acknowledged|reviews completed on time|referrals confirmed|access and export events reviewed",
        "best-interest determination|risk and safeguarding response|placement or removal decisions|case closure and disclosure",
        "case actions, referrals and review deadlines cross organisations, and sensitive history is hard to protect."
    ),
    "Women's collective and group management systems": brief(
        "Follow participation, leadership, finance and collective action together.",
        "A women's collective management system should connect members, groups, meetings, savings or enterprise activity, leadership roles, referrals and outcomes without reducing empowerment to attendance. It should make agency and control visible through appropriate qualitative and quantitative evidence.",
        "member and collective journey",
        "member, household and safe contact|group, role and membership history|meeting, attendance and decision|savings, loan or enterprise record|referral and service outcome|agency, leadership and collective action evidence",
        "define the group's operating model|establish member and group identity|record decisions not only attendance|connect financial and support workflows|review inclusion and leadership patterns|measure agency with context",
        "publicly exposing membership or finance|treating attendance as empowerment|household-level outcomes attributed to one service|technology controlled only by external staff",
        "active groups and member continuity|decisions with member participation|financial records reconciled|leadership and agency evidence reviewed",
        "handling conflict or disclosure|interpreting agency and safety|loan or benefit decisions|changing group leadership",
        "membership, meetings, savings and referrals are separate, so the collective cannot see its own complete history."
    ),
    "Disability inclusion case management systems": brief(
        "Track barriers, choices and accommodations—not a deficit catalogue.",
        "A disability inclusion case system should connect a person's goals, functional needs, environmental barriers, requested accommodations, services and outcomes. It should use respectful, rights-based language and keep people involved in decisions about their record.",
        "person-centred inclusion plan",
        "person, communication preference and consent|goal and participation context|functional need and environmental barrier|accommodation or assistive support|referral, service and follow-up|participation outcome and person feedback",
        "co-design language and access needs|record goals before service categories|map barriers and accommodations|assign and follow referrals|review whether participation changed|give people a correction route",
        "diagnosis used as identity|collecting impairment detail without purpose|accommodation marked complete before use|inaccessible forms and communication",
        "requested accommodations delivered|service use confirmed|participation goals progressed|records corrected by the person",
        "clinical diagnosis|eligibility and benefit decisions|accepting an accommodation as adequate|sharing sensitive functional information",
        "assessments, accommodations and service referrals live in different systems and do not reflect the person’s own goals."
    ),
    "Community needs and household profiling systems": brief(
        "Build a shared picture without turning a community into a permanent survey.",
        "Community profiling software should connect households, institutions, assets, priorities and referrals while collecting only information that supports an agreed decision or service. Profiles need dates, sources, consent and community review because conditions and priorities change.",
        "household within a community profile",
        "household, members and location|need, strength and source|community asset and institution|priority, meeting and participant voice|referral, scheme or action|review date, change and closure",
        "agree which decisions need data|co-design categories and consent|establish household and place identity|connect priorities to actions|review representation and missing voices|retire stale or unnecessary fields",
        "extractive surveys with no return value|sensitive labels visible to neighbours|old profiles treated as current|loudest voices represented as consensus",
        "profile coverage and freshness|participation across groups|priorities linked to owned actions|referrals and schemes resolved",
        "community priority setting|handling disputed information|sensitive household referrals|publishing or sharing local data",
        "we collect household data repeatedly, but communities cannot see how it connects to priorities, services or action."
    ),
    "Scholarship application eligibility screening": brief(
        "Prepare a reviewable eligibility packet; do not automate opportunity decisions.",
        "AI can assist scholarship screening by checking completeness, extracting stated facts and applying explicit rules to prepare a reviewer packet. A person should resolve ambiguous evidence, exceptions, appeals and the final eligibility or selection decision.",
        "application review case",
        "applicant and consent|scheme and rule version|application answer and source|document, extraction and confidence|rule result and explanation|exception, reviewer and appeal decision",
        "translate policy into explicit rules|test rules on diverse historical examples|separate missing from ineligible|run extraction under review|prepare evidence-linked packets|audit outcomes and appeals",
        "proxy discrimination hidden in rules|poor scans treated as missing proof|conflicting documents resolved automatically|eligibility conflated with merit selection",
        "complete packets prepared|extraction errors by document type|exceptions routed correctly|review time without changed outcomes",
        "eligibility and selection|interpreting hardship or context|document fraud judgement|appeals and exceptions",
        "applications and documents arrive in volume, and reviewers need a consistent evidence packet without outsourcing decisions to AI.",
        help_default="Custom AI Solutions",
        form_question="Which part of scholarship review should the mission prepare?"
    ),
    "Employment placement verification": brief(
        "Verify the outcome, preserve the evidence and escalate disagreement.",
        "An AI placement-verification mission can contact graduates and employers, collect permitted evidence and classify cases into clear review states. It should distinguish self-report, employer confirmation, document evidence, conflict and nonresponse rather than outputting a single opaque verified flag.",
        "placement verification case",
        "graduate and safe contact|placement claim and date|employer or enterprise identity|call, message or document evidence|verification state and reason|conflict, reviewer and final outcome",
        "define acceptable evidence|capture permission for contact|verify identity before disclosure|collect evidence across channels|route conflict and low confidence|approve outcome and preserve trail",
        "contacting an employer without permission|informal work treated as unverifiable|nonresponse marked as false|AI resolving wage or identity conflicts",
        "cases reaching a clear state|evidence attached|nonresponse by subgroup|reviewer overturn and escalation rate",
        "final verification state|disputed evidence|employer contact exceptions|support after adverse findings",
        "we need to verify placement claims at scale while keeping every source, conflict and reviewer decision visible.",
        help_default="Custom AI Solutions",
        form_question="What placement evidence and verification state do you need?"
    ),
    "90-day and 180-day retention follow-up": brief(
        "Keep following the cohort after the placement report is filed.",
        "A retention follow-up mission schedules consented contact at defined intervals, gathers current employment evidence and prepares exceptions for human review. Denominators must retain unreachable and unresolved graduates so retention is not overstated.",
        "graduate follow-up episode",
        "graduate and consent state|placement baseline|follow-up window and attempt|current role, employer and wage evidence|change, exit or support need|nonresponse, conflict and reviewer decision",
        "define follow-up windows and states|verify safe contact channels|schedule multilingual outreach|collect comparable evidence|route support needs and conflicts|report retention with nonresponse",
        "different questions at each interval|unreachable graduates removed|job change counted as failure|sensitive reasons shared with employers",
        "contact and completion rate|verified retention by window|job change and exit reasons|unresolved and support cases",
        "responding to distress or exploitation|resolving employment conflict|offering programme support|approving the reported status",
        "we can report placement at course exit but cannot follow every graduate consistently at 90 and 180 days.",
        help_default="Custom AI Solutions",
        form_question="Which cohort and follow-up windows should the mission cover?"
    ),
    "MEL data quality assistant": brief(
        "Find the exception, show the source and let the data owner decide.",
        "A MEL data-quality assistant can apply documented checks, compare related records and prepare a queue of missing, inconsistent or unusual cases with source links. It should never silently change source data or invent values to make a dataset complete.",
        "data-quality exception",
        "dataset and approved version|record and source link|rule, threshold and rationale|exception and possible explanation|assigned owner and correction|review outcome and change history",
        "document definitions and quality rules|profile current error patterns|run checks without changing source|prioritise consequential exceptions|route to accountable owners|learn from reviewed false positives",
        "anomaly treated as an error|missing values imputed into source|rules changing without versioning|teams overwhelmed by low-value alerts",
        "exceptions confirmed|time to resolution|false-positive rate|repeated error pattern reduced",
        "correcting source records|accepting a valid outlier|changing an indicator rule|deciding dataset fitness for reporting",
        "quality checks are manual and late, but automated corrections would create a new trust problem.",
        help_default="Custom AI Solutions",
        form_question="Which dataset and quality checks should the assistant prepare?"
    ),
    "Human escalation and override design": brief(
        "Design the handoff before the automation earns autonomy.",
        "Human escalation design specifies which conditions stop automation, who receives the case, what evidence they see, how quickly they must act and how their correction changes future work. An override must be visible, attributable and reversible where appropriate.",
        "escalated mission case",
        "case and mission state|trigger, risk and confidence|source evidence and action history|assigned reviewer and deadline|decision, reason and override|downstream effect and learning record",
        "list consequential decisions and failure modes|define stop and escalation rules|design the reviewer packet|test capacity and response time|record overrides and downstream effects|review patterns and adjust autonomy",
        "an escalation queue nobody owns|confidence used as the only risk signal|reviewers seeing conclusions without evidence|overrides that disappear from the audit trail",
        "high-risk cases stopped|review time and overdue escalation|override and overturn rate|recurring failure modes reduced",
        "consequential decision|accepting residual uncertainty|changing mission rules|expanding or reducing autonomy",
        "we need explicit stop conditions, reviewer ownership and an auditable override path before automating a workflow.",
        help_default="Custom AI Solutions",
        form_question="Where must AI stop and hand the work to a person?"
    ),
    "Nonprofit MIS requirements template": brief(
        "Describe the work, records and decisions before listing features.",
        "A useful nonprofit MIS requirements template captures the programme journey, central record, roles, decisions, forms, indicators, permissions, integrations, migration and adoption measures. It helps teams compare proposals against operating reality instead of generic feature lists.",
        "requirements decision pack",
        "programme model and scope|roles, decisions and permissions|records, fields and relationships|workflows, exceptions and approvals|reports, indicators and evidence|migration, integration, adoption and ownership",
        "complete the programme journey first|work through one representative case|mark must-have versus later|attach examples and definitions|review with field, MEL and leadership|issue a controlled version for proposals",
        "copying another NGO's requirements|hundreds of fields without purpose|non-functional needs omitted|success defined only as launch",
        "requirements with named owners|critical exceptions represented|proposals compared consistently|scope changes recorded",
        "scope and trade-off decisions|accepting security risk|choosing the implementation partner|signing off the final requirement",
        "we need a requirements document that vendors can respond to without forcing us to design the solution first."
    ),
    "Skilling placement and retention tracker": brief(
        "Keep placement, evidence and follow-up states in one working tracker.",
        "A skilling placement and retention tracker should separate placement claim, verification evidence, current employment state, follow-up attempts and reviewer decisions. It is a practical starting point for smaller cohorts and a clear migration source when a full MIS becomes necessary.",
        "candidate placement and follow-up row",
        "candidate and course identifiers|placement claim and start date|evidence and verification state|30, 90 and 180-day follow-up|job change, exit and reason|next action, owner and review note",
        "agree definitions and dropdown states|protect identifiers and contact fields|enter the placement baseline|schedule follow-up views|review conflict and nonresponse|freeze reporting snapshots",
        "free-text states that cannot be counted|overwriting historical outcomes|unreachable graduates deleted|evidence links shared too broadly",
        "rows with complete identifiers|verified placement coverage|follow-ups due and completed|nonresponse retained in reporting",
        "final verification|resolving evidence conflict|contacting employers|responding to support needs",
        "we need a disciplined tracker now that can preserve evidence and later migrate into a placement MIS."
    ),
    "Nonprofit MIS cost estimator": brief(
        "Estimate the work behind the build, not a price per screen.",
        "A nonprofit MIS cost estimator should account for workflow complexity, user roles, data migration, integrations, offline use, security, training and ongoing ownership. It should return a range with assumptions and risk drivers rather than a false fixed quote.",
        "scoped estimate with assumptions",
        "programme and workflow count|roles, users and permission complexity|forms, reports and languages|migration volume and quality|integrations, offline and attachments|training, support and ownership period",
        "describe one complete workflow|count roles and exceptions|profile migration and integrations|separate launch from ongoing cost|state assumptions and exclusions|review range with implementation teams",
        "estimating before workflow discovery|licences confused with implementation|data cleaning omitted|support and internal ownership treated as free",
        "assumptions explicitly answered|high-risk drivers identified|range sensitivity visible|actual cost compared after implementation",
        "budget approval|risk appetite|scope trade-offs|vendor and platform choice",
        "we need a realistic budget range and want to understand which requirements are actually driving cost."
    ),
    "Theory of Change to data model guide": brief(
        "Translate causal intent into records a programme can actually maintain.",
        "Moving from a Theory of Change to a data model means identifying the actors, activities, outputs, outcomes, assumptions and decisions that need records—then removing everything the programme cannot collect or use responsibly. The result is not a database version of every box in the diagram.",
        "outcome claim linked to programme evidence",
        "actor and unit of analysis|activity and service delivery|output and immediate result|outcome observation and timing|assumption, risk and context|indicator, source and decision owner",
        "mark the decisions the theory should inform|identify units and relationships|map outcomes to observable evidence|define timing and attribution limits|design the minimum source workflow|test whether teams can maintain it",
        "one table for every diagram box|proxy indicators treated as outcomes|context and assumptions omitted|collecting fields nobody reviews",
        "outcomes linked to source records|indicators with owners and definitions|assumptions reviewed|unused collection removed",
        "accepting an outcome claim|interpreting contribution|changing the programme theory|deciding what not to collect",
        "our Theory of Change is strong, but the MIS and indicators do not map cleanly to the decisions it describes."
    ),
    "Nonprofit MIS implementation roadmap": brief(
        "Move from diagnosis to adoption through reviewable releases.",
        "A nonprofit MIS roadmap should sequence discovery, data modelling, prototyping, migration, testing, launch and adoption around small complete workflows. Each release needs a decision gate, named owner, evidence of use and a clear boundary for what comes later.",
        "implementation release and decision gate",
        "current-state workflow and pain|blueprint and central record|prototype and acceptance case|migration and quality decision|training, release and support|adoption measure and improvement backlog",
        "diagnose and prioritise one journey|architect records and roles|prototype with real users|migrate and test representative cases|launch with support and ownership|review use, quality and next release",
        "a big-bang scope|testing only happy paths|training delivered too early|project closure before adoption stabilises",
        "acceptance cases passed|migration reconciled|critical roles using the workflow|exceptions and support demand declining",
        "scope and release sign-off|risk acceptance|data cut-over|prioritising the next module",
        "we need a phased roadmap that gets one workflow working before the organisation depends on a full system."
    ),
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sentence_list(items: list[str]) -> str:
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def answer_for(question: dict[str, str], page: dict[str, str], info: dict) -> str:
    family = question["question_family"]
    topic = page["working_title"]
    if family in {"fit", "direct-answer", "ai-fit", "capability", "decision", "use"}:
        return info["direct"]
    if family in {"requirements", "data-model", "inputs", "contents", "architecture", "integration"}:
        return f"Start with {info['central']}. The minimum useful record set covers {sentence_list(info['records'])}. Remove any field that does not support a service, safeguard, decision or reporting obligation."
    if family == "implementation":
        return f"Use a phased sequence: {sentence_list(info['steps'])}. Each stage needs a named owner and a review gate before the next stage begins."
    if family == "workflow":
        return f"Give every stage a named operational owner and require a separate human review for {sentence_list(info['human'])}. Use {sentence_list(info['measures'])} to decide whether the workflow is ready to expand."
    if family == "ownership":
        return f"The team that owns {info['central']} should maintain the resource, with input from frontline, programme, MEL or data, technology and leadership roles as relevant. Keep one named owner responsible for version control, review decisions and updates."
    if family == "cost":
        return "The main cost and timeline drivers are workflow and permission complexity, data migration quality, integrations, offline or language needs, testing availability, training and long-term ownership. Estimate after modelling one real journey and its exceptions."
    if family in {"scale", "adaptation"}:
        return f"Keep the definition of {info['central']} stable at every scale. A small programme can begin with one workflow and a few roles; a multi-state programme also needs delegated ownership, stronger permissions, shared definitions, integration rules and location-level quality review."
    if family == "readiness":
        return f"Readiness depends less on organisation size than on whether the team can name {info['central']}, the people who own each step, the decisions the system should support and the evidence needed to test a first release."
    if family == "selection":
        return "Choose this approach only after testing one real workflow, its exceptions, permissions, integrations and maintenance needs. Compare the operating fit and ownership model—not only features shown in a demonstration."
    if family == "switching":
        return "Consider switching when critical workflows depend on repeated workarounds, permissions cannot be enforced, reporting requires manual reconstruction or the current platform cannot be maintained responsibly. Test the replacement against a complete real journey before migrating."
    if family in {"risk", "limitations", "tradeoff", "warning"}:
        return f"The main risks are {sentence_list(info['risks'])}. Test these with representative cases and keep the consequential judgement with a named person."
    if family in {"human-oversight", "governance"}:
        return f"People should retain responsibility for {sentence_list(info['human'])}. Software or AI may prepare evidence and queues, but it should not silently make those decisions."
    if family in {"auditability", "evidence", "quality", "assurance"}:
        return f"Keep the source, definition, time, owner, status and review decision together. Monitor {sentence_list(info['measures'])}, and preserve limitations instead of cleaning them out of the report."
    if family in {"vendor-selection"}:
        return f"Ask a prospective partner to model one real journey, one exception, one permission boundary and one report. Compare how they handle {sentence_list(info['risks'])}, not only the number of features in a demonstration."
    if family in {"minimum-viable", "indicators", "exceptions"}:
        return f"Begin with {info['central']} and only the records needed for the next action. Review {sentence_list(info['measures'])}; route exceptions to a person rather than hiding them in totals."
    return info["direct"]


def type_label(content_type: str) -> str:
    labels = {
        "sector-guide": "Sector implementation guide",
        "solution-landing": "Solution guide",
        "dozai-mission": "DozAI mission design",
        "technology-guide": "Technology guide",
        "resource-template": "Working template",
        "resource-tool": "Decision tool",
        "resource-framework": "Implementation framework",
        "comparison": "Buying guide",
    }
    return labels.get(content_type, "EdZola guide")


def parent_label(page: dict[str, str]) -> tuple[str, str]:
    ctype = page["content_type"]
    if ctype == "sector-guide":
        return page["sector"], page["parent_path"]
    if ctype == "dozai-mission":
        return "DozAI missions", "/dozai/"
    if ctype.startswith("resource-"):
        return "Resources", "/resources/"
    if ctype == "technology-guide":
        return "Technology guides", "/learn/technology/"
    if ctype == "comparison":
        return "Comparisons", "/learn/compare/"
    return "Solutions", "/solutions/"


def page_json_ld(page: dict[str, str], info: dict, questions: list[dict[str, str]]) -> str:
    url = SITE + page["path"]
    parent_name, parent_path = parent_label(page)
    faq = []
    for question in questions:
        faq.append({
            "@type": "Question",
            "name": question["question"],
            "acceptedAnswer": {"@type": "Answer", "text": answer_for(question, page, info)},
        })
    graph = [
        {
            "@type": "Organization",
            "@id": f"{SITE}/#organisation",
            "name": "EdZola",
            "legalName": "EdZola Technologies Private Limited",
            "url": f"{SITE}/",
            "email": "reachus@edzola.com",
            "address": {"@type": "PostalAddress", "addressLocality": "Coimbatore", "addressRegion": "Tamil Nadu", "addressCountry": "IN"},
        },
        {
            "@type": "Article",
            "@id": url + "#article",
            "headline": page["working_title"],
            "description": info["direct"],
            "datePublished": TODAY,
            "dateModified": TODAY,
            "inLanguage": "en-GB",
            "mainEntityOfPage": {"@id": url + "#webpage"},
            "author": {"@id": f"{SITE}/#organisation"},
            "publisher": {"@id": f"{SITE}/#organisation"},
            "image": f"{SITE}/assets/og-edzola.png",
        },
        {
            "@type": "WebPage",
            "@id": url + "#webpage",
            "url": url,
            "name": page["working_title"] + " | EdZola",
            "description": info["direct"],
            "inLanguage": "en-GB",
            "breadcrumb": {"@id": url + "#breadcrumb"},
            "about": {"@type": "Thing", "name": page["working_title"]},
            "publisher": {"@id": f"{SITE}/#organisation"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": url + "#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": parent_name, "item": SITE + parent_path},
                {"@type": "ListItem", "position": 3, "name": page["working_title"], "item": url},
            ],
        },
        {"@type": "FAQPage", "mainEntity": faq},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))


def render_page(page: dict[str, str], info: dict, questions: list[dict[str, str]], related: list[dict[str, str]]) -> str:
    esc = html.escape
    title = page["working_title"]
    first_word = title.split(maxsplit=1)[0]
    topic = title if first_word.isupper() or first_word in {"Zoho", "KoboToolbox", "WhatsApp", "DozAI", "Zolabs", "ZolaShield"} else title[:1].lower() + title[1:]
    url = SITE + page["path"]
    parent_name, parent_path = parent_label(page)
    meta = info["direct"][:156].rsplit(" ", 1)[0].rstrip(".,") + "."
    qa_html = "".join(
        f'<details data-question-id="{esc(q["question_id"])}"' + (' open' if i == 0 else '') + '>'
        f'<summary>{esc(q["question"])}</summary><p>{esc(answer_for(q, page, info))}</p></details>'
        for i, q in enumerate(questions)
    )
    risk_html = "".join(
        f'<article class="card"><span class="num">RISK {i:02d}</span><h3>{esc(item[0].upper() + item[1:] if item else item)}</h3><p>Make this visible in testing, ownership and review rather than leaving it as an implementation surprise.</p></article>'
        for i, item in enumerate(info["risks"], 1)
    )
    model_html = "".join(
        f'<div><b>{i:02d}</b><span>{esc(item[0].upper() + item[1:])}</span></div>'
        for i, item in enumerate(info["records"], 1)
    )
    steps_html = "".join(
        f'<div class="flow-step"><div><h3>{esc(item[0].upper() + item[1:])}</h3><p>Agree the owner, evidence and exit condition before moving forward.</p></div><span class="owner {"human" if i in {1, len(info["steps"])} else ""}">{"Human gate" if i in {1, len(info["steps"])} else "System-supported"}</span></div>'
        for i, item in enumerate(info["steps"], 1)
    )
    measures_html = "".join(
        f'<article class="metric"><span>0{i}</span><strong>{esc(item[0].upper() + item[1:])}</strong></article>'
        for i, item in enumerate(info["measures"], 1)
    )
    human_html = "".join(f"<li>{esc(item[0].upper() + item[1:])}</li>" for item in info["human"])
    system_html = "".join(f"<li>{esc(item[0].upper() + item[1:])}</li>" for item in info["steps"][1:-1])
    related_html = "".join(
        f'<a href="{esc(item["path"])}"><small>{esc(type_label(item["content_type"]))}</small><strong>{esc(item["working_title"])}</strong><span>Read the guide →</span></a>'
        for item in related[:3]
    )
    json_ld = page_json_ld(page, info, questions)
    form_title = "Tell us about the workflow you want to improve."
    form_body = "Share what happens today, where it breaks and what a useful decision or outcome would look like. We’ll help identify a practical first step."
    return f'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)} | EdZola</title>
<meta name="description" content="{esc(meta)}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="EdZola">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_GB">
<meta property="og:image" content="{SITE}/assets/og-edzola.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta)}">
<meta name="twitter:image" content="{SITE}/assets/og-edzola.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/crm-webform.css?v=20261015h">
<link rel="stylesheet" href="/assets/knowledge-page.css?v=20261019a">
<script type="application/ld+json">{json_ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap"><a class="logo" href="/" aria-label="EdZola home">edzola<i>.</i></a><nav aria-label="Primary navigation"><a href="/solutions/">Solutions</a><a href="/sectors/">Sectors</a><a href="/learn/">Learn</a><a href="/resources/">Resources</a></nav><a class="pill primary" href="#contact-form">Discuss this workflow</a></div></header>
<main id="main">
<div class="wrap crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="{esc(parent_path)}">{esc(parent_name)}</a><span aria-hidden="true">/</span><span aria-current="page">{esc(title)}</span></div>
<section class="wrap hero knowledge-hero" aria-labelledby="page-title"><div><span class="status">{esc(type_label(page["content_type"]))} · Evidence-led</span><h1 id="page-title">{esc(title)}.<br><em>{esc(info["tagline"])}</em></h1><p class="lead">{esc(info["direct"])}</p><div class="hero-actions"><a class="pill dark" href="#framework">See the working model</a><a class="pill ghost" href="#questions">Read the Q&amp;A</a></div><div class="byline"><span>For {esc(page["primary_audience"])}</span><span>Updated {DISPLAY_DATE}</span></div></div>
<div class="mis-map"><div class="map-head"><strong>{esc(info["central"].title())}</strong><span>Reference model</span></div><div class="person-card"><span class="avatar" aria-hidden="true">EZ</span><div><strong>One connected record</strong><small>SOURCE · STATUS · OWNER · EVIDENCE</small></div><span class="one">traceable</span></div><div class="record-flow">{''.join(f'<div class="record"><span class="date">0{i}</span><div><b>{esc(item[0].upper()+item[1:])}</b><p>Linked to the same operating record.</p></div><span class="tag">Defined</span></div>' for i,item in enumerate(info["records"][:3],1))}</div><div class="decision"><span class="spark">✦</span><div><b>Decision boundary</b><p>A system prepares the record and evidence. A named person owns consequential judgement.</p></div></div><p class="map-caption">Illustrative operating model, not a client record or product screenshot.</p></div></section>
<section class="answer-band"><div class="wrap"><div class="answer-label">The direct answer</div><p>{esc(info["direct"])}</p></div></section>
<div class="wrap page-grid"><aside class="toc"><b>On this page</b><a href="#risks">What breaks</a><a href="#framework">Minimum model</a><a href="#sequence">Implementation sequence</a><a href="#measures">What to measure</a><a href="#boundary">Human boundary</a><a href="#questions">Questions answered</a><a href="#contact-form">Talk to EdZola</a></aside><article class="article">
<section id="risks"><p class="eyebrow">01 · What breaks</p><h2>Design for the failure modes, not only the happy path.</h2><p class="section-lead">The value of {esc(topic)} depends on what happens when records are incomplete, evidence conflicts or the next action carries consequence.</p><div class="problem-grid">{risk_html}</div></section>
<section id="framework"><p class="eyebrow">02 · Minimum viable model</p><h2>Start with {esc(info["central"])} and the decisions around it.</h2><p class="section-lead">The smallest useful model for this page connects the following records. Each field should have a purpose, owner and retention rule.</p><div class="data-model"><div class="model-core"><small>Central record</small><strong>{esc(info["central"].title())}</strong></div><div class="model-spokes">{model_html}</div></div></section>
<section id="sequence"><p class="eyebrow">03 · Implementation sequence</p><h2>Move through reviewable gates.</h2><p class="section-lead">A complete small workflow is safer and more useful than a large collection of unfinished modules.</p><div class="workflow">{steps_html}</div></section>
<section id="measures"><p class="eyebrow">04 · Evidence</p><h2>Measure whether the work became clearer.</h2><p class="section-lead">Usage alone is not success. Review the quality, timeliness and decisions the system is meant to improve.</p><div class="metric-grid">{measures_html}</div></section>
<section id="boundary"><p class="eyebrow">05 · Responsible automation</p><h2>Let systems prepare. Keep consequence with people.</h2><div class="boundary"><div class="checks"><h3>Systems can support</h3><ul>{system_html}</ul></div><div class="checks human"><h3>People should decide</h3><ul>{human_html}</ul></div></div></section>
<section id="questions"><p class="eyebrow">06 · Common questions</p><h2>Practical questions teams ask.</h2><p class="section-lead">Use these answers to clarify scope, compare approaches and identify the decisions your team needs to make before implementation.</p><div class="faq">{qa_html}</div></section>
<section class="related"><p class="eyebrow">Continue exploring</p><h2>Related implementation guidance.</h2><div class="related-grid">{related_html}</div></section>
</article></div>
<section class="crm-embed-section knowledge-crm" aria-labelledby="crm-embed-heading"><div class="crm-embed-inner"><div class="final crm-form-left"><div class="contact" data-crm-webform data-crm-form-title="Tell us about this workflow." data-crm-form-note="Five short questions. Plain language is perfect; you do not need to have the solution worked out." data-crm-question-label="{esc(info["form_question"])}" data-crm-placeholder="{esc(info["placeholder"])}" data-crm-help-default="{esc(info["help_default"])}" data-crm-submit-label="Share this workflow"></div><div data-crm-intro><h2 id="crm-embed-heading">{esc(form_title)}</h2><p>{esc(form_body)}</p></div></div></div></section>
</main>
<footer><div class="wrap"><span>© 2026 EdZola Technologies Private Limited · Coimbatore, India</span><span><a href="/solutions/">Solutions</a> · <a href="/learn/">Learn</a> · <a href="/resources/">Resources</a> · <a href="/about/">About</a></span></div></footer>
<script defer src="/assets/crm-webform.js?v={FORM_SCRIPT_VERSION}"></script>
</body></html>'''


def render_hub(title: str, path: str, description: str, pages: list[dict[str, str]], eyebrow: str) -> str:
    esc = html.escape
    cards = "".join(
        f'<a class="library-card" href="{esc(page["path"])}"><small>{esc(type_label(page["content_type"]))}</small><h2>{esc(page["working_title"])}</h2><p>{esc(BRIEFS[page["working_title"]]["direct"])}</p><b>Read the guide →</b></a>'
        for page in pages
    )
    url = SITE + path
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": title,
        "description": description,
        "url": url,
        "isPartOf": {"@type": "WebSite", "name": "EdZola", "url": SITE + "/"},
        "hasPart": [{"@type": "WebPage", "name": p["working_title"], "url": SITE + p["path"]} for p in pages],
    }, ensure_ascii=False, separators=(",", ":"))
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{esc(title)} | EdZola</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="EdZola"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:locale" content="en_GB"><meta property="og:image" content="{SITE}/assets/og-edzola.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{SITE}/assets/og-edzola.png"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"><link rel="stylesheet" href="/assets/crm-webform.css?v=20261015h"><link rel="stylesheet" href="/assets/knowledge-page.css?v=20261019a"><script type="application/ld+json">{schema}</script></head><body><a class="skip" href="#main">Skip to content</a><header class="top"><div class="wrap"><a class="logo" href="/">edzola<i>.</i></a><nav aria-label="Primary navigation"><a href="/solutions/">Solutions</a><a href="/sectors/">Sectors</a><a href="/learn/">Learn</a><a href="/resources/">Resources</a></nav><a class="pill primary" href="#contact-form">Talk to us</a></div></header><main id="main"><section class="library-hero wrap"><p class="eyebrow">{esc(eyebrow)}</p><h1>{esc(title)}</h1><p>{esc(description)}</p></section><section class="wrap library-grid" aria-label="{esc(title)}">{cards}</section><section class="crm-embed-section knowledge-crm" aria-labelledby="crm-embed-heading"><div class="crm-embed-inner"><div class="final crm-form-left"><div class="contact" data-crm-webform data-crm-form-title="Tell us what you are trying to improve." data-crm-question-label="Which workflow or decision should we understand?" data-crm-placeholder="one workflow depends on several trackers, and we need a practical first step." data-crm-help-default="Data Systems – MIS / ERP"></div><div data-crm-intro><h2 id="crm-embed-heading">Start with one real workflow.</h2><p>Bring one tracker, form or decision. We’ll help identify which guide applies and what a useful first step could be.</p></div></div></div></section></main><footer><div class="wrap"><span>© 2026 EdZola Technologies Private Limited</span><span><a href="/">Home</a> · <a href="/about/">About</a></span></div></footer><script defer src="/assets/crm-webform.js?v={FORM_SCRIPT_VERSION}"></script></body></html>'''


def related_pages(page: dict[str, str], phase_one: list[dict[str, str]]) -> list[dict[str, str]]:
    candidates = [p for p in phase_one if p["page_id"] != page["page_id"]]
    return sorted(candidates, key=lambda p: (
        0 if p["sector"] and p["sector"] == page["sector"] else 1,
        0 if p["cluster"] == page["cluster"] else 1,
        0 if p["content_type"] == page["content_type"] else 1,
        p["page_id"],
    ))


def build_sitemap(paths: list[str]) -> None:
    urls = "\n".join(f"  <url><loc>{SITE}{path}</loc><lastmod>{TODAY}</lastmod></url>" for path in paths)
    (ROOT / "sitemap-content.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8",
    )


def main() -> None:
    registry = read_rows(REGISTRY)
    question_rows = read_rows(QUESTION_BANK)
    phase_one = [p for p in registry if p["language"] == "en" and p["rollout_phase"] == "1"]
    if len(phase_one) != 30:
        raise ValueError(f"Expected 30 phase-one pages, found {len(phase_one)}")
    missing = {p["working_title"] for p in phase_one} - set(BRIEFS)
    if missing:
        raise ValueError(f"Missing page briefs: {sorted(missing)}")
    questions = {}
    for row in question_rows:
        questions.setdefault(row["page_id"], []).append(row)
    for page in phase_one:
        if page["working_title"] == "Nonprofit MIS software":
            continue  # The approved long-form sample is maintained by hand.
        target = ROOT / page["path"].lstrip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_page(page, BRIEFS[page["working_title"]], questions[page["page_id"]], related_pages(page, phase_one)), encoding="utf-8")

    solution_pages = [p for p in phase_one if p["content_type"] == "solution-landing"]
    resource_pages = [p for p in phase_one if p["content_type"].startswith("resource-")]
    tech_pages = [p for p in phase_one if p["content_type"] == "technology-guide"]
    comparison_pages = [p for p in phase_one if p["content_type"] == "comparison"]
    learn_pages = tech_pages + comparison_pages
    hubs = [
        ("Solutions for nonprofit operations", "/solutions/", "Practical systems, privacy, voice AI and responsible automation for nonprofit and social-impact teams.", solution_pages, "Commercial solution guides"),
        ("EdZola implementation library", "/learn/", "Evidence-led guides for choosing, designing and implementing nonprofit technology.", learn_pages, "Learn"),
        ("Technology guides", "/learn/technology/", "Platform and architecture guides grounded in nonprofit operating workflows.", tech_pages, "Learn · Technology"),
        ("Nonprofit technology comparisons", "/learn/compare/", "Buying guides that compare workflow fit, ownership, cost and trade-offs.", comparison_pages, "Learn · Compare"),
        ("Templates, tools and implementation resources", "/resources/", "Working resources that turn programme intent into clearer requirements, decisions and systems.", resource_pages, "Resource library"),
    ]
    for title, path, description, pages, eyebrow in hubs:
        target = ROOT / path.lstrip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render_hub(title, path, description, pages, eyebrow), encoding="utf-8")
    sitemap_paths = [path for _, path, _, _, _ in hubs] + [p["path"] for p in phase_one]
    build_sitemap(sitemap_paths)
    print(f"Built {len(phase_one)} phase-one pages, {len(hubs)} hubs and sitemap-content.xml")


if __name__ == "__main__":
    main()
