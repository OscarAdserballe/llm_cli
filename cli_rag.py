#!/usr/bin/env python3
import click
from prompts import PROMPTS
import colored
from config_rag import RAG
import os


@click.command()
@click.argument("prompt", type=str)
@click.option("--system-prompt", default="default", type=click.Choice(PROMPTS.keys()), help="System prompt to use")
def cli(prompt, system_prompt):
    with RAG(system_prompt=system_prompt, folder_name=os.getcwd()) as rag:
        response = rag.query(prompt)
        colored.cprint(response, "navy_blue")

if __name__ == "__main__":
    cli()