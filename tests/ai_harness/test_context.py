import pytest

from ai_harness.context.manager import ContextManager
from ai_harness.memory.manager import MemoryManager


def test_build_context_with_memory(tmp_path) -> None:
    memory = MemoryManager(tmp_path / "memory.json")
    memory.add("Проект создаётся на Python", "project")
    manager = ContextManager(memory)

    context = manager.build("Расскажи о проекте")

    assert context.user_query == "Расскажи о проекте"
    assert len(context.memory_items) == 1
    assert "Проект создаётся на Python" in context.text


def test_build_context_without_memory(tmp_path) -> None:
    memory = MemoryManager(tmp_path / "memory.json")
    manager = ContextManager(memory)

    context = manager.build("Привет")

    assert context.user_query == "Привет"
    assert context.memory_items == ()
    assert "Привет" in context.text


def test_context_respects_character_limit(tmp_path) -> None:
    memory = MemoryManager(tmp_path / "memory.json")
    memory.add("A" * 100, "project")
    manager = ContextManager(memory, max_chars=40)

    context = manager.build("Привет")

    assert len(context.text) <= 40
    assert context.memory_items == ()


def test_empty_query_is_rejected(tmp_path) -> None:
    memory = MemoryManager(tmp_path / "memory.json")
    manager = ContextManager(memory)

    with pytest.raises(ValueError):
        manager.build("   ")


def test_invalid_character_limit_is_rejected(tmp_path) -> None:
    memory = MemoryManager(tmp_path / "memory.json")

    with pytest.raises(ValueError):
        ContextManager(memory, max_chars=0)
