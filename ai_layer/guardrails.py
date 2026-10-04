import re

INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior)\s+instructions", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+(a|an)\s+", re.IGNORECASE),
    re.compile(r"system\s*prompt", re.IGNORECASE),
    re.compile(r"disregard\s+(the\s+)?above", re.IGNORECASE),
]

FORBIDDEN_SQL_KEYWORDS = {
    "insert",
    "update",
    "delete",
    "drop",
    "truncate",
    "alter",
    "grant",
    "revoke",
}


def sanitize_retrieved_context(chunks: list[str]) -> list[str]:
    """Sanitizes context retrieved from RAG before prompt injection"""
    sanitized = []
    for chunk in chunks:
        clean = chunk
        for pattern in INJECTION_PATTERNS:
            if pattern.search(clean):
                clean = pattern.sub("[REDACTED_SUSPICIOUS_DIRECTIVE]", clean)
        sanitized.append(clean)
    return sanitized


def validate_readonly_sql(query: str) -> bool:
    """Verifies that an agent-generated SQL query is strictly read-only"""
    normalized = query.strip().lower()
    tokens = set(re.findall(r"\b\w+\b", normalized))
    violations = tokens.intersection(FORBIDDEN_SQL_KEYWORDS)
    if violations:
        raise PermissionError(
            f"Unauthorized mutation keyword detected: {violations}. Only SELECT permitted."
        )
    return True
