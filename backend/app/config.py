import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "deepseek-chat")
