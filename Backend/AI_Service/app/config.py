import os

from dotenv import load_dotenv

load_dotenv()

CONTACTS_SERVICE_URL = os.getenv("CONTACTS_SERVICE_URL", "http://localhost:5002")

# The Vercel AI Gateway key. It is only read from the environment (.env).
# Never print it, log it or return it in a response.
AI_GATEWAY_API_KEY = os.getenv("AI_GATEWAY_API_KEY")
AI_GATEWAY_BASE_URL = os.getenv("AI_GATEWAY_BASE_URL", "https://ai-gateway.vercel.sh/v1")
LLM_MODEL = os.getenv("LLM_MODEL")