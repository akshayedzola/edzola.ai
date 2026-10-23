---
title: "This is how we think about AI. For whatever it's worth."
url: "https://www.edzola.com/post/this-is-how-we-think-about-ai-for-whatever-it-s-worth"
description: "AI doesn't create new habits — it amplifies what already exists. A practical 3-stage framework for nonprofits ready to make their institutional knowledge work harder."
author: "Akshay V"
published: "2026-04-22T03:27:54.542Z"
modified: "2026-04-22T05:17:34.269Z"
featured: false
minutes_to_read: 6
cover_image_local: "media/946993_e9368343ae724a15a6c2f81778be3721_mv2.webp"
og_image_local: "media/946993_e9368343ae724a15a6c2f81778be3721_mv2.webp"
seo_title: "This is how we think about AI. For whatever it's worth."
sitemap_lastmod: "2026-04-22"
---

![How Nonprofits Should Actually Think About AI in 2026 - EdZola](../media/946993_e9368343ae724a15a6c2f81778be3721_mv2.webp)

I've been having the same conversation with a lot of nonprofit leaders lately. Someone hears about what we've been doing with AI at EdZola, asks if I can share more, and I end up walking them through it. Not as a pitch, but as a genuine **"here's what we tried, what worked, what didn't."**

What I've noticed is that the questions are almost always the same. And the anxiety is almost always the same too.

So let me try to write down what I've actually learnt, from a year of building this on our own organization first, before recommending any of it to anyone else.

## The thing most people get wrong about AI

Most organizations I meet are either trying to use AI for everything at once, or they're waiting until it's "ready enough." Both extremes miss the point.

AI doesn't create new habits. It amplifies habits that already exist.

If your team already writes strong proposals, AI will help them write better ones faster. If your organization doesn't have institutional memory, AI won't create it for you. It'll just give you a better-looking gap. The tool follows the behaviour. Not the other way around.

That's been the most important thing I've learnt. And it's changed how we approach everything.

## Three stages. One direction.

After a year of experimenting, failing, and slowly figuring things out at EdZola (running things on our own organization first before recommending anything to a partner), here's the framework I've come to think in.

###

### Stage 1: Institutional Intelligence

AI knows your org. Your voice. Your thinking. Your history. Tribal knowledge becomes reusable.

This is where we started. We didn't go build agents or automation. We sat down and asked: what does EdZola actually know after five years? What's in our proposals, our brand, our delivery playbooks, our way of framing things? And then we put all of it, systematically, into something AI can actually use.

We built what we call ***skills***. A skill is just a markdown file, but it contains the compressed intelligence of everything we've built. Our brand voice. How we write proposals. The MAP framework we use for every MIS delivery. How a discovery call with a nonprofit should actually go.

The result?
When someone on the team writes a client email or drafts a proposal or creates a LinkedIn post, they're not starting from zero. The institutional memory is already there, already active. They don't even have to consciously invoke it. It just applies.

> **We're not prompting every time. We're compounding intelligence.**

### Stage 2: Decision and Execution Engine

AI works in your systems. Connected to your calendar, your CRM, your inbox. It reads live data and acts on it.

This is where it gets genuinely powerful. Every morning at 9, I run a prompt (or increasingly, it runs itself). It pulls my calendar, classifies each call, does the relevant research and prep, reads my inbox to flag what needs a reply, drafts first responses, and posts a structured summary to my Zoho Cliq.

Before this, I was spending 30 to 45 minutes every morning just getting oriented. Now I log in and I already have a head start on the day.

The way I think about it: I've trained Claude on how I think, not just what I do.

### Stage 3: Scalable Systems

AI builds infrastructure: pipelines, frameworks, open knowledge, things that work beyond any one person.

This is the stage that matters most to me, because it's what makes EdZola more than a consultancy.

One example: I had six years of grant emails sitting in a folder I was too guilty to open. I'd subscribed to all the right mailing lists, carefully filed everything, and basically never looked at it again. So I wrote a Python script (with AI helping me write the script, which is a nice recursion) that went through every .eml file, extracted the funder name, grant type, eligible organizations, geography, deadline, and summary, and built it into a Postgres database with a visual dashboard.

It took half a day. The database now has six years of grant intelligence in it, filtered by org type, geography, tech focus, grant size, deadline. Open sourced. Anyone can use it.

That's one example. The bigger example is ImpactOS: productising six years of EdZola's delivery thinking into a framework and platform that any nonprofit can use, rather than keeping it locked inside our team's heads.

## What I've actually stopped doing

Here's the part I don't usually say out loud, but I think it's important.

Since we went deep on Claude (we're on the team plan, we've been on it for a while), I've stopped hiring for certain roles.

Every time I think about posting a Founder's Office Associate role, I pause and ask: *do I actually need a human for this, or can I build an agent that does it better?* More often than not, the honest answer is the second one. For coordination, for prep work, for synthesising information, for first-draft everything: agents are doing what I used to pay a full-time person to do.

I'm not saying that's universally a good thing. It's something I'm still thinking through. But it's real, and I think founders who are honest with themselves are seeing it too.

## What this means for nonprofits (and the people who work in them)

Every time I walk through this, someone stops me and says some version of: *"This is basically a new employee who has the institutional knowledge of everyone who's ever worked here."*

Yes. And here's the thing. It never forgets. It doesn't have bad days. It doesn't get overwhelmed. And unlike a real knowledge transfer, you don't need to rely on the good grace of someone's notice period.

But it only knows what you've actually taught it. The quality of the output is directly proportional to the quality of the input. You still need a person who thinks carefully about what the organisation knows, how it communicates, what it values. The tool doesn't replace that judgment. It amplifies it.

For nonprofits specifically, there are a few use cases I think are immediately worth starting with, because they require no new software and almost no tech team:

- **Program teams** should be turning field data into board insights. Not reports that sit in folders. Actual 3 to 5 line summaries that drive decisions. "Here's what's emerging. Here's the risk."
- **Fundraising teams** should not be spending three days on a grant proposal. That time can be compressed, not by cutting corners, but by using AI as a first-draft collaborator who already knows your programme story.
- **Leaders** should not be walking into funder meetings relying entirely on what they can hold in their heads. Twenty minutes of prep (the funder's priorities, your strongest angle, the two questions you should ask) is automatable.
- **HR and people functions:** This one is underrated. Giving good feedback consistently, across a team, at different levels, is genuinely hard. AI doesn't make it easier to decide what to say. But it does help you say it better.

## The one principle I keep coming back to

*AI amplifies behaviour that already exists.*

If the habit isn't there offline, the tool won't create it. If the knowledge isn't somewhere, the skill won't surface it.

This is actually good news. It means you don't have to become a tech company to use AI well. You just have to be honest about what your organisation already knows, already does, already cares about, and then figure out how to make that intelligence accessible and reusable.

That's it. That's the whole thing.

## Why this matters beyond EdZola

I've been doing this work for six years. And one thing I know about the social sector is that knowledge is its most under-leveraged asset.

Organizations spend years developing deep program intuition: what works in a particular geography, what a community actually responds to, where implementation breaks down. That knowledge lives in people's heads, in old emails, in proposals that were never filed anywhere useful. When people leave, it walks out the door with them.

The opportunity AI presents, for this sector specifically, is not about automation or efficiency in the generic sense. It's about making accumulated wisdom reusable. It's about a team of three being able to punch at the level of a team of ten, not because they're working harder, but because the organization's intelligence is finally working for them.

That is worth building towards. Not because it's exciting technology. But because the sector deserves better infrastructure.

We tried all of this on ourselves first. We broke things. We figured out what actually matters. And then we shared it.

> **Because that's what this sector does best: learn something, then give it away.**

|  |
| --- |
| Your organization already knows more than it uses.  Let AI unlock it.  [Book a free discovery call](https://www.edzola.com/contact) |
