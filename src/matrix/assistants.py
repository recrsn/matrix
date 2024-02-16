from matrix.config import Assistant
from matrix.config import config
from matrix.prompts import run_prompt


def add_assistant(assistant_id: str, provider_id: str, model_id: str, prompt_id: str):
    with config() as cfg:
        cfg.add_assistant(Assistant(assistant_id, provider_id, model_id, prompt_id))


def run_assistant(assistant_id: str):
    with config() as cfg:
        assistant = cfg.get_assistant(assistant_id)
        run_prompt(assistant.prompt_id, assistant.provider_id, assistant.model_id)
