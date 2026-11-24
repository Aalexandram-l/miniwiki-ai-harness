import pytest

from ai_harness.memory.manager import MemoryManager


def test_add_and_get_memory(tmp_path) -> None:
    manager = MemoryManager(tmp_path / "memory.json")

    entry = manager.add("Описание проекта", "project")

    assert entry.content == "Описание проекта"
    assert entry.category == "project"
    assert manager.get_all() == [entry]


def test_memory_is_persisted(tmp_path) -> None:
    storage = tmp_path / "memory.json"
    manager = MemoryManager(storage)
    manager.add("Важная информация", "general")

    reloaded_manager = MemoryManager(storage)

    assert len(reloaded_manager.get_all()) == 1
    assert reloaded_manager.get_all()[0].content == "Важная информация"


def test_filter_by_category(tmp_path) -> None:
    manager = MemoryManager(tmp_path / "memory.json")
    manager.add("Первая запись", "project")
    manager.add("Вторая запись", "personal")

    result = manager.get_by_category("PROJECT")

    assert len(result) == 1
    assert result[0].content == "Первая запись"


def test_delete_memory(tmp_path) -> None:
    manager = MemoryManager(tmp_path / "memory.json")
    entry = manager.add("Удаляемая запись")

    assert manager.delete(entry.id) is True
    assert manager.get_all() == []
    assert manager.delete(entry.id) is False


def test_empty_content_is_rejected(tmp_path) -> None:
    manager = MemoryManager(tmp_path / "memory.json")

    with pytest.raises(ValueError):
        manager.add("   ")
