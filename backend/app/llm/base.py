from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator


class BaseLLM(ABC):

    @abstractmethod
    async def generate(
        self,
        messages: list[dict],
    ) -> str:
        ...

    @abstractmethod
    async def stream(
        self,
        messages: list[dict],
    ) -> AsyncGenerator[str, None]:
        ...