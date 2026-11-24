import pytest

from ai_harness.rules.engine import Rule, RuleAction, RuleEngine


def test_empty_request_is_denied() -> None:
    engine = RuleEngine()

    result = engine.check("   ")

    assert result.allowed is False
    assert result.reason == "Пустой запрос не допускается"


def test_request_without_matching_rules_is_allowed() -> None:
    engine = RuleEngine()

    result = engine.check("Объясни архитектуру проекта")

    assert result.allowed is True


def test_denied_keyword_blocks_request() -> None:
    rule = Rule(
        name="forbidden_action",
        description="Запрещённое действие",
        action=RuleAction.DENY,
        keywords=("удалить базу",),
    )
    engine = RuleEngine((rule,))

    result = engine.check("Попробуй удалить базу данных")

    assert result.allowed is False
    assert "forbidden_action" in result.matched_rules


def test_duplicate_rule_is_rejected() -> None:
    rule = Rule(
        name="test_rule",
        description="Тестовое правило",
        action=RuleAction.ALLOW,
        keywords=("тест",),
    )
    engine = RuleEngine((rule,))

    with pytest.raises(ValueError):
        engine.add_rule(rule)
