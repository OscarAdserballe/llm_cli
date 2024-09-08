#!/usr/bin/env python3
import sys
import os
from config_llm import LLM
from prompts import PROMPTS
import click

@click.command()
@click.argument("prompt", type=str)
@click.option("--system-prompt", default="default", type=click.Choice(PROMPTS.keys()), help="System prompt to use")
def cli(prompt, system_prompt):
    llm = LLM(system_prompt=PROMPTS[system_prompt])

    response = llm.query(prompt)

    click.echo(response)

if __name__ == "__main__":
    cli() 
