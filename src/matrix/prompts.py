import atexit
import readline

from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

from matrix import providers
from matrix.config import config
from matrix.config import CONFIG_DIR


def add_prompt(prompt_id: str, text: str):
    with config() as cfg:
        cfg.add_prompt(prompt_id, text)


def get_prompt(prompt_id: str) -> str:
    with config() as cfg:
        return cfg.get_prompt(prompt_id)


def run_prompt(prompt_id: str, provider_id, model_id, stream=False, raw=False):
    client = providers.get_client(provider_id)
    prompt = get_prompt(prompt_id)

    hist_dir = CONFIG_DIR / "history"
    hist_dir.mkdir(exist_ok=True)

    hist_file = hist_dir / f"{prompt_id}.txt"

    try:
        readline.read_history_file(hist_file)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, hist_file)

    messages = [
        {"role": "system", "content": prompt}
    ]

    console = Console()

    with client:
        try:
            while True:
                line = console.input(Text("You: ", style="bold"))
                messages.append({"role": "user", "content": line.strip()})
                with console.status("Thinking..."):
                    chat_completion = client.chat.completions.create(
                        model=model_id,
                        messages=messages,
                        temperature=0.1,
                        stream=stream,
                    )

                if stream:
                    output = []
                    console.print(Text("🤖 Assistant: ", style="bold"), end="")
                    for message in chat_completion:
                        text = message.choices[0].delta.content
                        if text is not None:
                            output.append(text)
                            console.print(text, end="", highlight=False)

                    console.print()
                    response = "".join(output)
                else:
                    response = chat_completion.choices[0].text.strip()
                    output = Text(response) if raw else Markdown(response)
                    console.print(Text("Assistant: ", style="bold"), output)

                messages.append({"role": "assistant", "content": response})
        except (KeyboardInterrupt, EOFError):
            # User cancelled, so we just exit
            pass
