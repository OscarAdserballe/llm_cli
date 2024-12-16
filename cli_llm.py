#!/usr/bin/env python
import click
import colored

from llm_utils.parameters import CONFIG
from llm_utils.models.llm import LLM
from llm_utils.prompts.prompts import PROMPTS
from llm_utils.utils.screenshot import take_screenshot

@click.command()
@click.argument("query", type=str)
@click.option("-p", '--pro', is_flag=True, help="Use the pro model")
@click.option("-s", '--snip', is_flag=True, help="Send screenshot of screen")
@click.option("--instruction", default="default", type=click.Choice(PROMPTS.keys()), help="System prompt to use")
def cli(query, instruction, pro, snip):
    kwargs = {
        "system_prompt": PROMPTS[instruction],
    }
    if pro:
        kwargs["model_name"] = CONFIG['pro_model'] 
    
    if snip:
        kwargs['system_prompt'] = PROMPTS['snip']

    llm = LLM(
        **kwargs
    )

    query_kwargs = {}
    query_kwargs["query"] = query
    if snip:
        query_kwargs["images"] = [take_screenshot()]


    response = llm.query(**query_kwargs)
    
    info_string = f"Using model {llm.model_name}..."
    colored.cprint(info_string, "green")
    colored.cprint(response, "navy_blue")

if __name__ == "__main__":
    cli() 
