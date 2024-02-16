import keyring
from openai import OpenAI

from matrix.config import config
from matrix.config import Provider


def register(alias: str, url: str, token: str | None = None, name: str | None = None):
    name = name or alias

    with config() as cfg:
        cfg.set_provider(Provider(alias, name, url, bool(token)))

    if token:
        keyring.set_password("system", alias, token)


def find_all():
    with config() as cfg:
        return cfg.get_providers()


def get_client(provider_id) -> OpenAI:
    with config() as cfg:
        provider = cfg.get_provider(provider_id)

        url = api_key = keyring.get_password("system", provider.alias) if provider.auth_required else "dummy"
        return OpenAI(api_key=api_key, base_url=provider.url)
