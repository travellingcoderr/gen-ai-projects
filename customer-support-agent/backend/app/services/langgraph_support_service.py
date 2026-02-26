from __future__ import annotations

from typing import TypedDict

from app.core.config import settings


class SupportState(TypedDict):
    query: str
    category: str
    analysis: str
    response: str


class LangGraphSupportService:
    def __init__(self) -> None:
        # Hybrid strategy:
        # 1) Prefer LLM-driven node behavior when a provider key is available.
        # 2) Fall back to deterministic logic when keys/packages are missing.
        # This keeps local/dev startup reliable while still enabling richer behavior in configured environments.
        self._llm_backend = self._resolve_llm_backend()
        self._openai_client = None
        self._gemini_model = None
        self._initialize_llm_clients()
        self._graph = self._build_graph()

    def _resolve_llm_backend(self) -> str:
        provider = (settings.LLM_PROVIDER or "openai").strip().lower()
        has_openai = bool(settings.OPENAI_API_KEY)
        has_gemini = bool(settings.GEMINI_API_KEY)

        if provider == "openai" and has_openai:
            return "openai"
        if provider == "gemini" and has_gemini:
            return "gemini"
        if has_openai:
            return "openai"
        if has_gemini:
            return "gemini"
        return "none"

    def _initialize_llm_clients(self) -> None:
        if self._llm_backend == "openai":
            try:
                from openai import OpenAI
            except ImportError:
                self._llm_backend = "none"
                return
            self._openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            return

        if self._llm_backend == "gemini":
            try:
                import google.generativeai as genai
            except ImportError:
                self._llm_backend = "none"
                return
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._gemini_model = genai.GenerativeModel(model_name=self._default_model_for("gemini"))

    def _default_model_for(self, backend: str) -> str:
        if settings.LLM_MODEL:
            return settings.LLM_MODEL
        if backend == "gemini":
            return "gemini-2.0-flash-exp"
        return "gpt-4o-mini"

    def _complete(self, prompt: str) -> str | None:
        try:
            if self._llm_backend == "openai" and self._openai_client is not None:
                response = self._openai_client.responses.create(
                    model=self._default_model_for("openai"),
                    input=prompt,
                )
                text = (response.output_text or "").strip()
                return text or None

            if self._llm_backend == "gemini" and self._gemini_model is not None:
                response = self._gemini_model.generate_content(prompt)
                text = (response.text or "").strip()
                return text or None
        except Exception:
            return None

        return None

    def _build_graph(self):
        try:
            from langgraph.graph import END, START, StateGraph
        except ImportError:
            return None

        graph = StateGraph(SupportState)
        graph.add_node("categorize", self._categorize_node)
        graph.add_node("analyze", self._analyze_node)
        graph.add_node("respond", self._respond_node)

        graph.add_edge(START, "categorize")
        graph.add_edge("categorize", "analyze")
        graph.add_edge("analyze", "respond")
        graph.add_edge("respond", END)

        return graph.compile()

    def run(self, query: str) -> dict[str, str]:
        state: SupportState = {
            "query": query,
            "category": "general",
            "analysis": "",
            "response": "",
        }

        if self._graph is not None:
            output = self._graph.invoke(state)
            return {
                "query": output["query"],
                "category": output["category"],
                "analysis": output["analysis"],
                "response": output["response"],
            }

        categorized = self._categorize_node(state)
        analyzed = self._analyze_node(categorized)
        responded = self._respond_node(analyzed)
        return {
            "query": responded["query"],
            "category": responded["category"],
            "analysis": responded["analysis"],
            "response": responded["response"],
        }

    def _categorize_node(self, state: SupportState) -> SupportState:
        category = self._categorize_with_llm(state["query"])
        if category is None:
            category = self._categorize_with_rules(state["query"])

        return {
            **state,
            "category": category,
        }

    def _analyze_node(self, state: SupportState) -> SupportState:
        analysis = self._analyze_with_llm(state["query"], state["category"])
        if analysis is None:
            analysis = self._analyze_with_rules(state["query"])

        return {
            **state,
            "analysis": analysis,
        }

    def _respond_node(self, state: SupportState) -> SupportState:
        response = self._respond_with_llm(state["query"], state["category"], state["analysis"])
        if response is None:
            response = self._respond_with_rules(state["category"], state["analysis"])

        return {
            **state,
            "response": response,
        }

    def _categorize_with_llm(self, query: str) -> str | None:
        prompt = (
            "Categorize the customer query into exactly one label: "
            "billing, technical, account, orders, general. "
            "Return only the label.\n"
            f"Query: {query}"
        )
        label = self._complete(prompt)
        if not label:
            return None

        normalized = label.strip().lower()
        allowed = ["billing", "technical", "account", "orders", "general"]
        for item in allowed:
            if item in normalized:
                return item
        return None

    def _analyze_with_llm(self, query: str, category: str) -> str | None:
        prompt = (
            "Write a one-sentence support analysis for this customer query. "
            "Focus on urgency and actionability.\n"
            f"Category: {category}\n"
            f"Query: {query}"
        )
        return self._complete(prompt)

    def _respond_with_llm(self, query: str, category: str, analysis: str) -> str | None:
        prompt = (
            "Write a concise, empathetic customer-support response with clear next steps.\n"
            f"Category: {category}\n"
            f"Analysis: {analysis}\n"
            f"Query: {query}"
        )
        return self._complete(prompt)

    def _categorize_with_rules(self, query: str) -> str:
        text = query.lower()
        if any(keyword in text for keyword in ["refund", "charge", "billing", "invoice"]):
            return "billing"
        if any(keyword in text for keyword in ["error", "bug", "not working", "crash"]):
            return "technical"
        if any(keyword in text for keyword in ["login", "password", "account", "profile"]):
            return "account"
        if any(keyword in text for keyword in ["delivery", "shipping", "order", "tracking"]):
            return "orders"
        return "general"

    def _analyze_with_rules(self, query: str) -> str:
        text = query.lower()
        urgent = any(keyword in text for keyword in ["urgent", "asap", "immediately", "angry"])

        if urgent:
            return "High-priority request. Respond with urgency and offer immediate escalation."
        if len(text) < 30:
            return "Low-context request. Ask clarifying questions before final resolution."
        return "Standard support request. Provide clear next steps and expected turnaround."

    def _respond_with_rules(self, category: str, analysis: str) -> str:
        return (
            f"Category: {category}. "
            f"Assessment: {analysis} "
            "Thanks for contacting support. I can help with this and will guide you through the next step."
        )
