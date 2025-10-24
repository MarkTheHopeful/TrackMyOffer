"""
PII anonymization utilities.

Provides a single function `anonymize_text` that masks/removes personally identifiable information (PII)
from arbitrary text. The function is conservative and idempotent: applying it multiple times yields the
same result and it aims to avoid over-redacting normal prose where possible.
"""
from __future__ import annotations

import re
from typing import Callable


# Precompiled regex patterns for performance and clarity
_EMAIL_RE = re.compile(r"""
    (?P<email>
        [A-Z0-9._%+-]+      # local part
        @
        [A-Z0-9.-]+         # domain
        \.                  # dot
        [A-Z]{2,}           # TLD
    )
""", re.IGNORECASE | re.VERBOSE)

# International-ish phone numbers, allowing spaces, dashes, parentheses
_PHONE_RE = re.compile(r"""
    (?P<phone>
        (?:\+\d{1,3}[\s-]?)?           # country code
        (?:\(?\d{2,4}\)?[\s-]?)       # area code
        \d{3,4}[\s-]?\d{3,4}           # local number
    )
""", re.VERBOSE)

# URLs and social profiles
_URL_RE = re.compile(r"""
    (?P<url>
        (?:https?://)?
        (?:www\.)?
        [A-Z0-9.-]+\.[A-Z]{2,}          # domain
        (?:/[\w./%#?&=+-]*)?            # path
    )
""", re.IGNORECASE | re.VERBOSE)

# Street addresses (very heuristic)
_ADDRESS_RE = re.compile(r"""
    (?P<address>
        \b\d{1,5}                      # street number
        [\s,.-]+
        (?:[A-Z][a-z]+\s?){1,4}        # street name words
        (?:St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Ln|Lane|Dr|Drive|Ct|Court|Pl|Place)\b
        (?:[^\n]*)?                    # rest of line until newline (city/state/zip often follow)
    )
""", re.IGNORECASE | re.VERBOSE)

# Email/phone labels variations (helps when models produce labeled fields)
_LABEL_VALUE_RES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)\b(Full\s*Name|Name)\s*:\s*.+"), "Name: [REDACTED]")
    ,(re.compile(r"(?i)\bEmail\s*:\s*.+"), "Email: [REDACTED]")
    ,(re.compile(r"(?i)\bPhone\s*:\s*.+"), "Phone: [REDACTED]")
    ,(re.compile(r"(?i)\bLocation\s*:\s*.+"), "Location: [REDACTED]")
    ,(re.compile(r"(?i)\bAddress\s*:\s*.+"), "Address: [REDACTED]")
    ,(re.compile(r"(?i)\bLinkedIn\s*:\s*.+"), "LinkedIn: [REDACTED]")
    ,(re.compile(r"(?i)\bGitHub\s*:\s*.+"), "GitHub: [REDACTED]")
    ,(re.compile(r"(?i)\bWebsite\s*:\s*.+"), "Website: [REDACTED]")
]

def _mask(match: re.Match[str], placeholder: str) -> str:
    return placeholder


def _build_name_patterns(names: list[str]) -> list[re.Pattern[str]]:
    patterns: list[re.Pattern[str]] = []
    for raw in names:
        name = raw.strip()
        if not name:
            continue
        # Exact full name (collapse multiple spaces)
        collapsed = re.sub(r"\s+", " ", name)
        escaped = re.escape(collapsed)
        patterns.append(re.compile(rf"\b{escaped}\b", re.IGNORECASE))
        # If two or more parts, also support first-initial + last-name (e.g., J. Doe)
        parts = collapsed.split(" ")
        if len(parts) >= 2 and all(p for p in parts[:2]):
            first, last = parts[0], parts[-1]
            first_initial = re.escape(first[0])
            last_escaped = re.escape(last)
            patterns.append(re.compile(rf"\b{first_initial}\.\s+{last_escaped}\b", re.IGNORECASE))
    return patterns


def anonymize_text(text: str, *, placeholder_email: str = "[REDACTED_EMAIL]", placeholder_phone: str = "[REDACTED_PHONE]", placeholder_url: str = "[REDACTED_URL]", placeholder_address: str = "[REDACTED_ADDRESS]", placeholder_name: str = "[REDACTED_NAME]", names_to_mask: list[str] | None = None) -> str:
    """
    Remove or mask common PII in a given text.

    What is masked:
    - Emails, phone numbers, URLs, and common street address formats
    - Typical labeled fields like "Email: ...", "Phone: ...", "Full Name: ..."
    - Candidate's own name occurrences, when provided via `names_to_mask` (exact full name and first-initial variants)

    The function is idempotent and aims to avoid excessive redaction of normal text.
    """
    if not text:
        return text

    # Mask obvious tokens
    text = _EMAIL_RE.sub(lambda m: _mask(m, placeholder_email), text)
    text = _PHONE_RE.sub(lambda m: _mask(m, placeholder_phone), text)
    text = _URL_RE.sub(lambda m: _mask(m, placeholder_url), text)
    text = _ADDRESS_RE.sub(lambda m: _mask(m, placeholder_address), text)

    # Replace labeled lines
    for pattern, replacement in _LABEL_VALUE_RES:
        text = pattern.sub(replacement, text)

    # Explicit name masking (no header/signature heuristics)
    if names_to_mask:
        for pat in _build_name_patterns(names_to_mask):
            text = pat.sub(placeholder_name, text)

    return text
