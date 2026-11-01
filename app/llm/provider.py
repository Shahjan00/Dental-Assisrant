"""LLM provider interface. Implementations: Gemini (LangChain) and rule-based mock."""
from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMProvider(ABC):
    @abstractmethod
    def extract_retrieval_intent(self, query: str) -> Dict[str, Any]:
        """Parse a retrieval query into {patient_name, report_type}."""
        ...

    @abstractmethod
    def structure_dictation(self, transcript: str) -> Dict[str, Any]:
        """Convert a clinical transcript into structured findings JSON."""
        ...

    @abstractmethod
    def answer_followup(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Answer a conversational follow-up given session context."""
        ...
