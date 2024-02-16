import sys

import click

from matrix import prompts
from matrix import providers
from matrix.config import config


@click.group()
def cli():
    """
    Matrix CLI

    A prompt management tool
    """
    pass


@cli.group('providers')
def providers_group():
    """
    Provider management
    """
    pass


@providers_group.command('register')
@click.argument('alias')
@click.option('--name', help='Name of the provider')
@click.option('--url', help='URL of the provider')
@click.option('--token', help='Auth token for the provider')
def register(alias, name, url, token):
    """
    Register a new provider
    """
    if name is None:
        name = click.prompt('Name (leave empty to use alias)')
    if url is None:
        url = click.prompt('URL')
    if token is None:
        token = click.prompt('Token (leave empty if not required)')

    providers.register(alias, url, token, name)
    click.echo(f'Registered provider {name} with alias {alias}')


@providers_group.command('list')
def list_providers():
    """
    List all registered providers
    """
    for _p in providers.find_all():
        click.echo(f'Provider: {_p.alias}')
        click.echo(f'\tName: {_p.name}')
        click.echo(f'\tURL: {_p.url}')
        click.echo(f'\tAuth Required: {_p.auth_required}')


@cli.group('assistants')
def assistants_group():
    """
    Assistant management
    """
    pass


@cli.group('prompts')
def prompts_group():
    """
    Prompt management
    """
    pass


@prompts_group.command('add')
@click.argument('prompt_id')
@click.argument('text', type=click.File('r'), default=sys.stdin)
def add_prompt(prompt_id, text):
    """
    Add a new prompt
    """
    prompts.add_prompt(prompt_id, text.read())
    click.echo(f'Added prompt {prompt_id}')


@prompts_group.command('list')
def list_prompts():
    """
    List all prompts
    """
    with config() as cfg:
        for prompt_id in cfg.get_prompts():
            click.echo(prompt_id)


@prompts_group.command('run')
@click.argument('prompt_id')
@click.option('--provider', help='Provider to use', required=True)
@click.option('--model', help='Model to use', required=True)
@click.option("--stream", is_flag=True, help="Stream the output. Will force --raw")
@click.option("--raw", is_flag=True, help="Show raw, unformatted output.")
def run_prompt(prompt_id, provider, model, stream, raw):
    """
    Run a prompt
    """
    prompts.run_prompt(prompt_id, provider, model, stream, raw)
