# PROJECT File

> Project state — what's built, where we are, what's planned

---

Format: YAML

```yaml
# PROJECT - Project State

name: project-name
type: web-app | cli-tool | library | static-site | api
status: development | beta | production | frozen

phase: 25
id: current-phase-id

stack:
  language: Python 3.11+ | Node 18+ | etc
  framework: Jinja2 | React | Express | etc
  tools: [list of key tools]

structure:
  src: path/to/source
  output: path/to/output
  config: path/to/config

method:
  workflow: "PROJECT → FIXES → TODO → code → test → DONE"
  branching: "Feature branches, never commit to main"
  testing: "How testing is done"
  deploy: "How deploy works"

expect:
  language: "Standards reference, e.g. ~/.rules/Python/RULES"
  quality: "What quality means in this project"

patterns:
  pattern-name: "Short description of pattern"

done:
  - phase: 1-16
    id: core
    title: "Core functionality"

planned:
  - phase: 25
    id: content-expansion
    title: "Content expansion"
```

## Rules

RULE: `phase:` and `id:` must match an entry in `done:` or `planned:`
RULE: Update `done:` when phase completes
RULE: Keep `planned:` current with future work
RULE: `status:` reflects overall project state

## PROJECT Is Single Source of Truth

All project circumstances go here:

| Category | Examples |
|----------|----------|
| Identity | Name, type, purpose, URLs |
| Infrastructure | SSH hosts, servers, paths, IPs |
| Domains | Production URL, dev URL, subdomains |
| Repositories | Git remote, hosting (GitHub/Codeberg) |
| Secrets | Location of API keys, env files (NOT the secrets themselves) |
| Credentials | Username references, auth methods (NOT passwords) |
| Services | External APIs, databases, CDNs |
| Deployment | rsync paths, deploy commands, environments |
| Protection | IP whitelists, basic auth setup, access rules |

**Why:** One file with all truths. No hunting through configs, docs, or memory.
**Security:** Document WHERE secrets are, never WHAT they contain.
