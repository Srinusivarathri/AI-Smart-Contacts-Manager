import logging

from openai import OpenAI

from app import config

logger = logging.getLogger(__name__)


class LLMConfigError(Exception):
    """The key or the model is not configured."""


class LLMError(Exception):
    """The LLM call failed. The message is always generic (it never has the key)."""


def _get_client() -> OpenAI:
    if not config.AI_GATEWAY_API_KEY or not config.LLM_MODEL:
        raise LLMConfigError("AI service is not configured")
    return OpenAI(
        api_key=config.AI_GATEWAY_API_KEY,
        base_url=config.AI_GATEWAY_BASE_URL,
        timeout=30.0,
        max_retries=1,
    )


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    """Send one prompt to the LLM (through the gateway) and return the text reply."""
    client = _get_client()
    try:
        response = client.chat.completions.create(
            model=config.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
    except Exception as exc:
        # Provider errors can contain a masked copy of the key, so we never pass the
        # original message on. We only log the error TYPE (for example NotFoundError for
        # a wrong model name) so debugging is still possible. "from None" hides the chain.
        logger.warning("LLM call failed: %s", type(exc).__name__)
        raise LLMError("LLM request failed") from None

    if not content:
        raise LLMError("LLM returned an empty response")
    return content