"""Register config — categories, concept mappings, layer assignment, stop words."""

from __future__ import annotations

CATEGORIES = [
    "global",
    "project-files",
    "automation",
    "devops",
    "ipc",
    "mcp",
    "personas",
    "gateway",
    "adapter",
    "core",
    "pal",
    "uiux",
    "slint",
    "python",
    "js",
    "css",
    "cpp",
    "rust",
    "kotlin",
    "csharp",
    "catalog",
]

CONCEPT_MAP = {
    "startup": ["workflow", "initialization"],
    "memory": ["memory-management", "lifecycle"],
    "persistent-memory": ["knowledge-base", "ai-memory"],
    "types": ["type-safety", "type-checking"],
    "modules": ["encapsulation", "architecture"],
    "testing": ["tdd", "quality"],
    "validation": ["runtime-checking", "boundaries"],
    "nesting": ["code-style", "readability", "flat-code"],
    "errors": ["error-handling", "result-types"],
    "threading": ["concurrency", "async"],
    "naming": ["conventions", "readability"],
    "ownership": ["memory-management", "borrowing"],
    "compose": ["ui", "declarative"],
    "viewmodel": ["state-management", "mvvm"],
    "coroutines": ["concurrency", "async"],
    "ktor": ["http", "networking"],
    "amper": ["build-system", "configuration"],
    "stability": ["build-system", "ci"],
    "encapsulation": ["architecture", "privacy"],
    "result-pattern": ["error-handling", "result-types"],
    "cascade": ["css-architecture", "separation"],
    "themes": ["theming", "dark-mode"],
    "responsive": ["mobile-first", "breakpoints"],
    "typography": ["fonts", "spacing"],
    "separation": ["architecture", "concerns"],
    "custom-properties": ["design-tokens", "variables"],
    "posix": ["linux", "system-programming"],
    "build": ["cmake", "configuration"],
    "jsdoc": ["type-annotations", "documentation"],
    "eslint": ["linting", "code-quality"],
    "typescript-cli": ["type-checking", "jsconfig"],
    "philosophy": ["design-principles", "approach"],
    "consistency": ["cross-language", "patterns"],
    "versions": ["language-versions", "compatibility"],
    "secrets": ["security", "environment"],
    "diagrams": ["mermaid", "visualization"],
    "index-system": ["navigation", "codebase-index"],
    "project-file": ["project-state", "yaml"],
    "todo-file": ["tasks", "tracking"],
    "fixes-file": ["problem-solving", "ai-memory"],
    "rag-file": ["knowledge-base", "ai-memory"],
    "goal-chain": ["milestones", "traceability"],
    "workflow": ["process", "methodology"],
    "contract": ["protocol", "json-rpc"],
    "keyboard": ["shortcuts", "accessibility"],
    "context-menus": ["ui-patterns", "interaction"],
    "drag-drop": ["interaction", "file-management"],
    "pointer-touch": ["interaction", "accessibility"],
    "issue-reporter": ["bug-reporting", "crash-handling"],
    "checklist": ["verification", "shipping"],
    "safety": ["runtime-validation", "boundaries"],
    "distribution": ["packaging", "pipx"],
    "gtk": ["gtk4", "gui"],
    "verification": ["clippy", "testing"],
    "naming-suffix": ["naming", "code-suffix"],
    "ack-pattern": ["result-types", "return-format"],
    "dependencies": ["libraries", "tooling"],
    "structure": ["file-organization", "architecture"],
    "quick-ref": ["reference", "summary"],
    "app-model": ["architecture", "state-management"],
    "component-model": ["slint-component-model", "property-direction", "slint-naming"],
    "rust-bridge": ["rust-slint-bridge", "adapter-event-routing", "type-mapping"],
    "globals": ["slint-globals", "design-tokens", "event-routing-global"],
    "threading": ["thread-safety", "event-loop", "async-ui-update"],
    "io": ["io-boundary", "gateway-pattern", "pal-delegation"],
    "lifecycle": ["gateway-lifecycle", "startup-sequence", "shutdown-sequence"],
    "viewmodel": ["viewmodel", "domain-mapping", "adapter-state"],
    "event-flow": ["event-flow", "adapter-event-routing", "core-dispatch"],
    "design": ["pure-business-logic", "domain-rules", "platform-abstraction"],
    "traits": ["pal-traits", "platform-interface", "file-api"],
}

# ---------------------------------------------------------------------------
# Learning path layers (1 = read first, 6 = reference/index)
# ---------------------------------------------------------------------------

CORE_FILES = {"types", "structure", "modules", "errors", "ack-pattern",
              "result-pattern", "naming", "encapsulation", "ownership"}

ADVANCED_FILES = {"testing", "dependencies", "nesting", "build", "posix",
                  "threading", "coroutines", "ktor", "amper", "stability",
                  "compose", "viewmodel", "data-classes", "gtk",
                  "verification", "eslint", "jsdoc", "typescript-cli",
                  "validation", "philosophy", "safety", "distribution",
                  "cascade", "custom-properties", "themes", "separation",
                  "responsive", "typography", "naming-suffix"}

INFRA_CATEGORIES = {"automation", "devops", "ipc", "uiux"}
ARCH_CATEGORIES = {"gateway", "adapter", "core", "pal"}

STOP_WORDS = frozenset([
    "the", "a", "an", "is", "are", "not", "and", "or", "for", "in",
    "on", "with", "to", "of", "by", "from", "at", "but", "vs", "it",
    "no", "do", "how", "why", "what", "when", "who", "than", "that",
    "its", "you", "be", "all",
])


def assign_layer(category: str, stem: str, file_type: str) -> int:
    """Assign a learning path layer (1-6) based on category and file."""
    if file_type in ("readme", "quick-ref"):
        return 6
    if category == "global":
        return 1
    if category == "project-files":
        return 2
    if category in INFRA_CATEGORIES:
        return 5
    if stem in CORE_FILES:
        return 3
    if stem in ADVANCED_FILES:
        return 4
    return 4
