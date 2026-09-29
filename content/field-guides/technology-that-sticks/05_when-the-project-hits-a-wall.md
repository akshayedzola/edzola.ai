---
title: "When the project hits a wall"
subtitle: "Five delivery instincts and a blocker protocol for nonprofit technology"
series: "Field Essays, part 5 of 7"
slug: when-the-project-hits-a-wall
author: Akshay, Founder & CEO, EdZola
reading_time: 8 min
meta_description: "Nonprofit tech projects fail even when the code works. Five delivery instincts and a five-step blocker protocol that keep trust intact when reality changes."
excerpt: "We once inherited a dashboard where every number was correct. Nobody used it. The system worked. The knowledge didn't survive."
suggested_visuals: "Animation: five-instincts.mp4, Carousel: Blocker protocol, Quote card 10"
---

# When the project hits a wall

We once inherited a dashboard where every number was correct. Nobody used it. The documentation had been skipped to save time, and when a new director joined and wanted to understand the metrics, nobody left could explain them. The system worked. The knowledge didn't survive.

Another time we met an organisation whose enrolment process was a three-email exchange between three departments, a phone call to a regional office and a spreadsheet where one person tracked approvals. Someone had automated the formal process in the procedure manual, which was five years out of date. The new system was elegant and completely useless.

In both cases the code was fine. The delivery failed.

## Why nonprofit delivery is harder

Nonprofit projects work under conditions that make technical excellence necessary and nowhere near enough.

**Requirements move mid-project.** A funder shifts priorities. A programme finds the population it serves has changed. A merger forces two organisations to integrate systems nobody fully understood. That's the organisation paying attention to real people. Projects have to be built to bend.

**Ownership is fragmented.** A donor database belongs partly to fundraising, partly to programmes, partly to finance, partly to the executive director and partly to whichever funder asked for it. Each speaks a different language about the same records.

**Data quality becomes a delivery problem.** A participant's phone number is in one system, the address in another, enrolment in a spreadsheet last updated eight months ago. A perfect system can't fix bad data. It exposes it, usually on day one.

**There's no budget for rework.** Commercial projects often plan a second pass. Nonprofit projects have to work the first time or get abandoned.

**Failure costs more than revenue.** When a case management system fails, participants go unsupported and staff spend nights recovering data.

## Five instincts

Requirements will change, stakeholders will disagree and data will be worse than expected. So delivery excellence here means just enough clarity to build safely, transparency when things change and a written record of what matters. We work from five instincts.

**1. Clarity before code.** The strongest predictor of rework is starting to build before the decision rule or data logic is clear. We pause, long enough to write down what the user is trying to do, what data they need at each step, what happens when it's missing and who validates it. A two-hour conversation before a sprint costs a fraction of rework halfway through.

**2. Specificity before commitment.** "The report is slow" or "the data looks wrong" starts a guessing game. We ask: what time did you run it, with which filters, what did you see, what did you expect? Can you share a screenshot? Can we reproduce it together now? This almost always finds the real problem faster, and it leaves no room to argue about what "broken" means. The same applies inside the team. We don't promise a feature "this week" until it's in the sprint plan with its dependencies and an estimate from the person doing the work.

**3. Documentation before memory.** Decisions and the reasons for them, action items and owners, screenshots with the problem circled, reproduction steps, the fix and the date the partner confirmed it. Written down as it happens, somewhere findable, so knowledge survives people moving on.

**4. Parallel momentum.** Projects depend on things outside the team's control. When an integration can't be tested because API access hasn't arrived, we build the scaffolding, write the logic and prepare the test cases so everything runs the moment access lands. Waiting drains a team. Parallel work keeps it engaged.

**5. Recovery before blame.** Surface the blocker the moment it's real, involve the partner, agree a concrete next step. "We add an index to the main query and test performance on Thursday." "We hold this feature for the next phase and launch on the planned date without it." Then change the next project so the same blocker doesn't surprise us twice.

## Week one sets the trajectory

Most of a project's future is decided in its first week. Ours always includes:

- A kickoff with stakeholders and decision-makers that confirms the problem, walks through acceptance criteria, names risks and sets the governance cadence. Documented, with owners.
- A sprint planning call against an estimated backlog. If the estimates aren't ready, planning waits.
- One shared tracker where every piece of work is visible, estimated and assigned. When a partner asks "where are we?", they can look.
- A cadence already on everyone's calendar: standups, demos, refinement and an escalation path.

When week three brings a hard problem, the partner remembers that week one was solid and solves it with you. When week one is vague, they assume every update will be bad news.

## The blocker protocol

Silence about blockers kills projects. The sprint plan becomes fiction, the partner assumes the team is slow, and workarounds harden into hidden technical debt. Our protocol has five steps.

1. **Name it the day it appears.** Not at the next status meeting.
2. **State the impact in specifics.** "Without the full dataset loaded by Friday, we can't build the intake validation planned for this sprint. We have the schema and sample records."
3. **Name the person who can unblock.** A specific decision-maker and a date.
4. **Bring the partner into the solve.** Lay out the options. They often know the data exists elsewhere or that a constraint can be waived.
5. **Write down what happened.** Next time a partner uses the same system, the plan accounts for it.

## Specificity is the antidote to blame

"The client is slow to respond" is a judgement, and once it's said it's hard to take back. "We sent the data schema on Monday and need confirmation by Wednesday to load the test database" is a fact with a deadline.

"The API is broken" could mean anything. "We can make 500 calls a day to the payment processor, the current workflow needs 800, so we either raise the limit or restructure the reconciliation logic" is a constraint with options.

One status update we sent during a busy stretch read: 14 showstopper issues. None open, one in progress, seven waiting for user acceptance testing, six on hold for more information. It told the whole story without blaming anyone, and it made the partner's next step obvious.

When blockers are named early, described precisely and solved together, they become the moments trust gets built.

---

*Previous: **Problem first, tool last.** Next: **Warmth is how standards travel.***
