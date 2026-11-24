from ai_harness.context.manager import ContextManager
from ai_harness.memory.manager import MemoryManager
from ai_harness.rules.engine import Rule, RuleAction, RuleEngine


def test_components_work_together(tmp_path) -> None:
    memory = MemoryManager(tmp_path / "memory.json")
    memory.add("MiniWiki создаётся на Python 3.12", "project")

    context_manager = ContextManager(memory)
    rule_engine = RuleEngine()

    query = "Расскажи об архитектуре MiniWiki"
    result = rule_engine.check(query)
    context = context_manager.build(query)

    assert result.allowed is True
    assert context.user_query == query
    assert "MiniWiki создаётся на Python 3.12" in context.text


def test_denied_request_does_not_pass_rule_check() -> None:
    rule = Rule(
        name="forbidden_action",
        description="Запрещённое действие",
        action=RuleAction.DENY,
        keywords=("удалить базу",),
    )
    rule_engine = RuleEngine((rule,))

    result = rule_engine.check("Попробуй удалить базу")

    assert result.allowed is False
