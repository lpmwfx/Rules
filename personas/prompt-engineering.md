---
tags: [persona, prompt-engineering, system-prompt, xml-tags, claude, anthropic]
concepts: [prompt-engineering, system-prompt-design, role-prompting, xml-structure]
feeds: [personas/aidevops.md]
keywords: [system-prompt, xml, role, claude, anthropic, persona-format, agent-prompt]
layer: 1
---
# Persona & Agent Prompt Engineering

> Rules for writing persona files and agent prompts that work reliably with Claude.
> Source: Anthropic prompt engineering best practices (claude.ai/docs).

---

VITAL: A persona file is a Claude system prompt — it must follow Anthropic's prompting guidelines
VITAL: Structure content with XML tags — Claude parses tagged sections unambiguously
VITAL: State the role in one clear sentence at the top of the system prompt
RULE: Provide context/motivation for constraints — not just "never X" but "never X because Y"
RULE: Use numbered steps for ordered sequences — Claude follows them precisely
RULE: Tell Claude what to do, not only what not to do — positive framing first
RULE: Put long context (documents, state) before instructions — improves response quality up to 30%
RULE: Wrap examples in `<example>` tags (multiple in `<examples>`) — separates them from instructions

---

## System Prompt Structure (Anthropic recommended order)

```xml
<role>
One sentence defining who Claude is in this context.
</role>

<context>
Background the AI needs — project state, current phase, relevant files.
Long data goes here, before instructions.
</context>

<instructions>
Numbered steps for ordered sequences.
Clear, specific directives.
</instructions>

<constraints>
Hard limits. Each constraint includes WHY — Claude generalizes from explanation.
</constraints>

<examples>
  <example>...</example>
  <example>...</example>
</examples>
```

RULE: Role section = one sentence — focus, not a paragraph
RULE: Constraints section explains WHY each limit exists — Claude understands and generalizes
RULE: Examples section uses `<example>` tags — 3–5 examples for best results
BANNED: Writing a persona as a flat wall of text with no XML structure

---

## Role Definition

RULE: "You are [Name], [one-line description of what this AI does]."
RULE: The role sentence establishes tone, expertise, and behavioral baseline immediately
RULE: Name the persona — a named persona is more consistent than an unnamed role

```xml
<role>
You are AIDevOps, a developer-first AI that alternates between collaborative planning
with the human (OPS mode) and strict autonomous execution (DEV mode).
</role>
```

---

## Constraint Formulation

Anthropic: "Never X" is less effective than "Never X because Y — Claude generalizes from explanation."

```xml
<!-- Less effective -->
<constraints>
Never commit untested code.
</constraints>

<!-- More effective -->
<constraints>
Never commit code that has not passed its tests — git history is the audit trail of
what works. A commit that hasn't been tested cannot be trusted or rolled back safely.
</constraints>
```

RULE: Each hard constraint states its reason — one sentence is enough
RULE: Use "never" and "always" sparingly — reserve for genuinely non-negotiable constraints

---

## Agentic Persona Rules (from Anthropic agentic systems guidance)

These apply to all agentic personas — personas that take actions autonomously.

VITAL: Confirm before irreversible actions — destructive ops, force-push, dropping data, external posts
VITAL: Investigate before answering — never speculate about files not read, code not opened
RULE: Use git for state tracking — git log is the record of what has been done
RULE: Tests before commits — write tests first, commit only when they pass
RULE: Incremental progress — advance steadily on a few things at a time, not everything at once
RULE: Save state before context window fills — write progress to files, commit, then continue fresh
RULE: Make independent tool calls in parallel — sequential only when one depends on another
BANNED: Overengineering — no abstractions, helpers, or features beyond what was asked
BANNED: Hard-coding to pass tests — implement the real logic, not the minimal case
BANNED: Speculating about code before reading it — read first, answer second

```xml
<investigate_before_answering>
Never speculate about files or code you have not read. If the user references a specific
file, read it before answering. Give grounded, hallucination-free responses only.
</investigate_before_answering>

<confirm_before_destructive_actions>
Take local, reversible actions (file edits, tests) freely.
Confirm with the human before: deleting files/branches, force-pushing, resetting hard,
posting to external services, or any action that cannot be undone.
</confirm_before_destructive_actions>
```

---

## How Persona Files in This Repo Work

Each `personas/*.md` file is both:
1. **A rule reference** — YAML frontmatter for MCP discoverability, RULE/VITAL markers for enforcement
2. **A system prompt template** — the body, when stripped of frontmatter, is ready to paste as system prompt

The XML-structured sections in the body ARE the system prompt. Load via:
```
get_rule("personas/aidevops.md")
```
Strip the YAML frontmatter block, paste the remainder as system prompt.

RULE: Every persona file must have a `requires:` list in frontmatter — these are the rule files
      that must also be loaded alongside the persona for complete behavioral coverage
RULE: The persona body uses XML tags for all major sections
RULE: RULE/VITAL/BANNED markers in the body are enforceable — they also appear in register.jsonl


---

<!-- LARS:START -->
<a href="https://lpmathiasen.com">
  <img src="https://carousel.lpmathiasen.com/carousel.svg?slot=3" alt="Lars P. Mathiasen"/>
</a>
<!-- LARS:END -->
