from dataclasses import dataclass

from ai_harness.memory.manager import MemoryManager


@dataclass(frozen=True)
class Context:
    user_query: str
    memory_items: tuple[str, ...]
    text: str


class ContextManager:
    def __init__(
        self,
        memory_manager: MemoryManager,
        max_chars: int = 4000,
    ) -> None:
        if max_chars <= 0:
            raise ValueError("Лимит контекста должен быть больше нуля")

        self.memory_manager = memory_manager
        self.max_chars = max_chars

    def build(self, user_query: str) -> Context:
        query = user_query.strip()
        if not query:
            raise ValueError("Запрос пользователя не может быть пустым")

        parts = [f"Запрос пользователя:\n{query}"]
        selected_memories: list[str] = []
        current_length = len(parts[0])

        for entry in self.memory_manager.get_all():
            memory_text = f"[{entry.category}] {entry.content}"
            separator = "\n\n"
            added_length = len(separator) + len(memory_text)

            if current_length + added_length > self.max_chars:
                continue

            selected_memories.append(memory_text)
            parts.append(memory_text)
            current_length += added_length

        return Context(
            user_query=query,
            memory_items=tuple(selected_memories),
            text="\n\n".join(parts),
        )
