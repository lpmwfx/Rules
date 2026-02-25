---
tags: [rag, fixes, ai-memory, persistent]
concepts: [ai-memory, knowledge-base]
feeds: [project-files/rag-file.md, project-files/fixes-file.md]
layer: 1
---
# Persistent AI Memory

> RAG + FIXES = AI's persistent memory across sessions

---

PROBLEM: AI starts every session with zero project knowledge
PROBLEM: AI repeats the same mistakes across sessions
PROBLEM: AI doesn't learn from what worked before

SOLUTION: Project files that AI both READS and WRITES to
- AI reads → gets context, avoids known mistakes
- AI writes → captures discoveries, solutions for future sessions
- Files grow over time → AI gets progressively smarter on the project

THIS IS THE WHOLE POINT:
- RAG captures what AI learns (facts, patterns, links)
- FIXES captures what AI solves (problems, causes, solutions)
- Both are persistent memory that survives session boundaries
- AI that uses these files produces consistently excellent results
- AI that ignores them repeats mistakes and loses context

AUTOMATION: The more AI writes to RAG/FIXES, the smarter future AI sessions become.
This is not documentation for humans — it's knowledge transfer between AI sessions.

## RAG = Project Knowledge

- Quick facts, links, patterns, discoveries
- AI WRITES when learning something useful
- AI READS to recall project-specific knowledge
- Format: Short, precise, lookup-friendly

## FIXES = Problem Solutions

- Problem → Cause → Solution format
- AI WRITES when solving a problem
- AI READS before coding (avoid repeating mistakes)
- Format: What broke, why, how to fix

Both files grow over time = AI gets smarter on the project.
