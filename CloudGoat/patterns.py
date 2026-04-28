import re
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
@dataclass
class SecretPattern:
    name: str
    pattern: re.Pattern
    severity: str
    description: str

SECRET_PATTERNS: List[SecretPattern] = [
    # AWS Credentials
    SecretPattern(
        name="aws_access_key_id",
        pattern=re.compile(r'AKIA[0-9A-Z]{16}'),
        severity="critical",
        description="AWS Access Key ID",
    ),
    SecretPattern(
        name="aws_secret_access_key",
        # Dodano grupę (1) dla samego klucza
        pattern=re.compile(r'(?i)(?:aws_secret|secret_access_key)\s*[=:]\s*[\'"]?([A-Za-z0-9/+=]{40})[\'"]?'),
        severity="critical",
        description="AWS Secret Access Key",
    ),
    SecretPattern(
        name="cloudgoat_password",
        pattern=re.compile(r'CloudGoat[A-Za-z0-9_]*(?:Password|Secret|Key)', re.IGNORECASE),
        severity="critical",
        description="CloudGoat specific credential",
    )
]

def _redact(match_str: str):
    if not match_str or len(match_str) < 8:
        return "***"
    return f"{match_str[:4]}****{match_str[-2:]}"

def scan_text(text: str) -> List[Dict[str,Any]]:
    findings = []
    if not text:
        return findings
    
    for secretPattern in SECRET_PATTERNS:
        for match in secretPattern.pattern.finditer(text):
            value = match.group(1) if match.lastindex else match.group(0)
            findings.append({
                "pattern_name": secretPattern.name,
                "severity": secretPattern.severity,
                "description": secretPattern.description,
                "preview": _redact(value),
                "offset": match.start()
            })
    return findings

def scan_dict(data: Dict[str,Any]) -> List[Dict[str,Any]]:
    findings = []
    for key, value in data.items():
        text = f"{key} {value}"
        matches = scan_text(text)
        for match in matches:
            match["location"] = f"Key: {key}"
            findings.append(match)
    return findings
    

