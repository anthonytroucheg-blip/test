from abc import ABC, abstractmethod
from typing import Optional
from ..config import settings


class BaseAgent(ABC):
    id: str
    name: str
    role: str
    description: str
    expertise: list[str]
    color: str     # Tailwind color name: indigo, emerald, amber, blue, orange, violet
    icon: str      # lucide-react icon name
    keywords: list[str]
    system_prompt: str

    def generate_response(
        self,
        message: str,
        history: list[dict],
        memory_context: str = "",
    ) -> str:
        if settings.openai_api_key:
            try:
                return self._openai_response(message, history, memory_context)
            except Exception:
                pass
        return self._mock_response(message)

    def _openai_response(
        self,
        message: str,
        history: list[dict],
        memory_context: str,
    ) -> str:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)

        system = self.system_prompt
        if memory_context:
            system += f"\n\n## Contexte entreprise\n{memory_context}"

        messages = [{"role": "system", "content": system}]
        for h in history[-10:]:
            messages.append({"role": h["role"], "content": h["content"]})
        messages.append({"role": "user", "content": message})

        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            max_tokens=1200,
            temperature=0.7,
        )
        return response.choices[0].message.content

    @abstractmethod
    def _mock_response(self, message: str) -> str:
        pass
