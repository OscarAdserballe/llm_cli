#!/usr/bin/env python3
import click
import colored
import os

from llm_utils.prompts.prompts import PROMPTS
from llm_utils.parameters import CONFIG
from llm_utils.models.rag import RAG

@click.command()
@click.option("-p", '--pro', is_flag=True, help="Use the pro model")
@click.option("-r", '--recursive', is_flag=True, help="Goes through all files in the directory, including directories")
@click.option("-s", '--search', default=None, help="Search for a specific file")
@click.argument("query", type=str)
@click.option("--instruction", default=None, type=click.Choice(PROMPTS.keys()), help="System prompt to use")
def cli(
        query,
        instruction,
        pro,
        recursive,
        search
    ):
    kwargs = {
        "folder_name": os.getcwd()
    }

    if instruction:
        kwargs["route"] = False
        kwargs["system_prompt"] = PROMPTS[instruction]

    if pro:
        kwargs["model_name"] = CONFIG['pro_model']

    if recursive:
        kwargs["is_recursive"] = True
    
    if search:
        kwargs["startswith"] = search
    

    with RAG(
        **kwargs
    ) as rag:
        response = rag.query(query)
        colored.cprint(response, "navy_blue")

if __name__ == "__main__":
    cli()
