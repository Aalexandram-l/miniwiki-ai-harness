from dataclasses import dataclass
from enum import StrEnum


class RuleAction(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class Rule:
    name: str
    description: str
    action: RuleAction
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class RuleResult:
    allowed: bool
    matched_rules: tuple[str, ...]
    reason: str


class RuleEngine:
    def __init__(self, rules: tuple[Rule, ...] = ()) -> None:
        self._rules = list(rules)

    def add_rule(self, rule: Rule) -> None:
        if any(existing.name == rule.name for existing in self._rules):
            raise ValueError(f"Правило '{rule.name}' уже существует")

        self._rules.append(rule)

    def check(self, text: str) -> RuleResult:
        if not text.strip():
            return RuleResult(
                allowed=False,
                matched_rules=(),
                reason="Пустой запрос не допускается",
            )

        normalized_text = text.casefold()
        matched = [
            rule
            for rule in self._rules
            if any(keyword.casefold() in normalized_text for keyword in rule.keywords)
        ]

        denied = [rule.name for rule in matched if rule.action == RuleAction.DENY]

        if denied:
            return RuleResult(
                allowed=False,
                matched_rules=tuple(denied),
                reason="Запрос нарушает одно или несколько правил",
            )

        allowed_rules = [
            rule.name for rule in matched if rule.action == RuleAction.ALLOW
        ]

        return RuleResult(
            allowed=True,
            matched_rules=tuple(allowed_rules),
            reason="Запрос разрешён",
        )
