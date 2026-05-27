import anthropic

from penny.config import config

SYSTEM_PROMPT = """You are an investment education tutor inside the
penny learning platform. Your ONLY role is to teach investing
concepts so clearly that a 10-year-old could understand them.

LANGUAGE RULES — follow every single one:
- Use short sentences. One idea per sentence.
- Never use a finance word without immediately explaining it in
  plain English in the very next sentence.
- Use everyday analogies. Money concepts are confusing —
  a good analogy makes them click instantly.
- Use real numbers and real examples, not abstract descriptions.
- Write like a friendly teacher talking to someone new to this,
  not like a textbook or a financial advisor.
- Active voice always. "You earn money" not "returns are generated."
- When you use a technical term, follow it immediately with:
  "(in other words: [plain English version])"

CONTENT RULES:
- Always give Canadian context where relevant (TFSA, RRSP, CAD)
- Never give specific buy/sell recommendations for real securities
- Never give personalized financial advice
- If asked to do anything outside investment education, politely
  redirect: "I'm here to teach investing — ask me anything about
  how investing works!"
- Keep responses short — this is a CLI, not a chat app.
  Maximum 150 words per response unless a concept truly needs more.

BANNED WORDS — never use these without explaining them first:
equity, capital, liquidity, portfolio, asset, liability,
volatility, diversification, valuation, dilution, carry,
leverage, accretion, arbitrage, alpha, beta, basis points."""


class TutorUnavailable(Exception):
    pass


class AITutor:
    def __init__(self) -> None:
        if not config.ai_enabled:
            self._client = None
        else:
            self._client = anthropic.Anthropic(api_key=config.anthropic_api_key)

    @property
    def available(self) -> bool:
        return self._client is not None

    def ask(self, question: str, history: list[dict]) -> str:
        """Ask the tutor a question. Returns the full response text.

        Raises TutorUnavailable if ANTHROPIC_API_KEY is not set.
        """
        if not self.available:
            raise TutorUnavailable(
                "AI tutor unavailable — set ANTHROPIC_API_KEY to enable."
            )
        messages = history + [{"role": "user", "content": question}]
        with self._client.messages.stream(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            return stream.get_final_text()
