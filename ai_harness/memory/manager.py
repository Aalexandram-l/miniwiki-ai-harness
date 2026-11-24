import json
from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class MemoryEntry:
    id: str
    content: str
    category: str


class MemoryManager:
    def __init__(self, storage_path: str | Path) -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._entries: list[MemoryEntry] = []
        self._load()

    def _load(self) -> None:
        if not self.storage_path.exists():
            return

        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        self._entries = [MemoryEntry(**item) for item in data]

    def _save(self) -> None:
        data = [asdict(entry) for entry in self._entries]
        temporary_path = self.storage_path.with_suffix(".tmp")
        temporary_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_path.replace(self.storage_path)

    def add(self, content: str, category: str = "general") -> MemoryEntry:
        if not content.strip():
            raise ValueError("Содержимое записи не может быть пустым")
        if not category.strip():
            raise ValueError("Категория не может быть пустой")

        entry = MemoryEntry(
            id=str(uuid4()),
            content=content.strip(),
            category=category.strip(),
        )
        self._entries.append(entry)
        self._save()
        return entry

    def get_all(self) -> list[MemoryEntry]:
        return list(self._entries)

    def get_by_category(self, category: str) -> list[MemoryEntry]:
        return [
            entry
            for entry in self._entries
            if entry.category.casefold() == category.casefold()
        ]

    def delete(self, entry_id: str) -> bool:
        for index, entry in enumerate(self._entries):
            if entry.id == entry_id:
                del self._entries[index]
                self._save()
                return True

        return False
