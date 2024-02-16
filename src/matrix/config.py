import re
from configparser import ConfigParser
from contextlib import contextmanager
from dataclasses import dataclass
from os import makedirs
from pathlib import Path
from typing import ContextManager

import platformdirs
from httpx import URL

CONFIG_DIR = Path(platformdirs.user_config_dir("matrix"))
MATRIX_PROMPTS_INI = CONFIG_DIR / "prompts.ini"
MATRIX_PROVIDERS_INI = CONFIG_DIR / "providers.ini"


@dataclass(frozen=True)
class Provider:
    alias: str
    name: str
    url: str
    auth_required: bool

    def __post_init__(self):
        if not re.match(r"^[a-z0-9-]+$", self.alias):
            raise ValueError("Alias must only contain lowercase letters, numbers, and hyphens")

        if not URL(self.url).is_absolute_url:
            raise ValueError("URL must be an absolute URL")


@dataclass(frozen=True)
class Assistant:
    id: str
    provider_id: str
    model_id: str
    prompt_id: str

    def __post_init__(self):
        if not re.match(r"^[a-z0-9-]+$", self.id):
            raise ValueError("ID must only contain lowercase letters, numbers, and hyphens")

        if not re.match(r"^[a-z0-9-]+$", self.provider_id):
            raise ValueError("Provider ID must only contain lowercase letters, numbers, and hyphens")

        if not re.match(r"^[a-z0-9-]+$", self.model_id):
            raise ValueError("Model ID must only contain lowercase letters, numbers, and hyphens")

        if not re.match(r"^[a-z0-9-]+$", self.prompt_id):
            raise ValueError("Prompt ID must only contain lowercase letters, numbers, and hyphens")


class Config:
    def __init__(self):
        self.providers = ConfigParser()
        self.prompts = ConfigParser()
        self.assistants = ConfigParser()
        self._dirty = False

    def set_provider(self, provider: Provider):
        self.providers[provider.alias] = {
            "name": provider.name,
            "url": provider.url,
            "auth_required": provider.auth_required,
        }
        self._dirty = True

    def get_provider(self, alias: str):
        data = self.providers[alias]
        return Provider(
            alias,
            data["name"],
            data["url"],
            data.getboolean("auth_required")
        )

    def get_providers(self):
        return [
            Provider(
                alias,
                data["name"],
                data["url"],
                data.getboolean("auth_required")
            )
            for alias, data in self.providers.items() if alias != "DEFAULT"
        ]

    def remove_provider(self, alias: str):
        self.providers.remove_section(alias)
        self._dirty = True

    def add_prompt(self, prompt_id: str, text: str):
        self.prompts[prompt_id] = {"text": text}
        self._dirty = True

    def get_prompt(self, prompt_id: str) -> str:
        return self.prompts[prompt_id]["text"]

    def get_prompts(self):
        return [section for section in self.prompts.sections() if section != "DEFAULT"]

    def add_assistant(self, assistant: Assistant):
        self.assistants[assistant.id] = {
            "provider_id": assistant.provider_id,
            "model_id": assistant.model_id,
            "prompt_id": assistant.prompt_id,
        }
        self._dirty = True

    def get_assistant(self, assistant_id: str) -> Assistant:
        data = self.assistants[assistant_id]
        return Assistant(
            assistant_id,
            data["provider_id"],
            data["model_id"],
            data["prompt_id"],
        )

    def get_assistants(self):
        return [
            Assistant(
                assistant_id,
                data["provider_id"],
                data["model_id"],
                data["prompt_id"],
            )
            for assistant_id, data in self.assistants.items() if assistant_id != "DEFAULT"
        ]

    def load(self):
        self.providers.read(MATRIX_PROVIDERS_INI)
        self.prompts.read(MATRIX_PROMPTS_INI)
        self._dirty = False

    def save(self):
        with open(MATRIX_PROVIDERS_INI, "w") as file:
            self.providers.write(file)
        with open(MATRIX_PROMPTS_INI, "w") as file:
            self.prompts.write(file)

        self._dirty = False


def _get_config():
    if not hasattr(_get_config, "_config"):
        makedirs(CONFIG_DIR, exist_ok=True)
        _config = Config()
        _config.load()
        setattr(_get_config, "_config", _config)

    return getattr(_get_config, "_config")


@contextmanager
def config() -> ContextManager[Config]:
    _config = _get_config()
    try:
        yield _config
    finally:
        if _config._dirty:
            _config.save()
