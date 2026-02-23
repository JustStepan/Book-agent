from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from prompts import PROMPTS
from pathlib import Path

BASE_DIR = Path(__file__).parent
MODELS = {
    'O': 'openai/gpt-oss-20b',
    'M': 'mistralai/devstral-small-2-2512',
    'DS': 'deepseek/deepseek-r1-0528-qwen3-8b',
    'L': 'liquid/lfm2.5-1.2b',
    'Q': 'qwen/qwen3-8b',
    'Z': 'zai-org/glm-4.6v-flash',
}


class Settings(BaseSettings):
    app_name: str = "Book-agent"
    version: str = '0.0.1'

    database_url: str = f"sqlite:///{BASE_DIR}/local_db.sqlite"
    model: str = MODELS['O']
    prompts: dict = PROMPTS


settings = Settings()