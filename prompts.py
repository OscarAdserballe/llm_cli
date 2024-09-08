import os

root_dir = "/Users/oscarjuliusadserballe/cli_scripts/prompts"


filepaths = {
    "code" : "coding_prompt.txt",
    "study" : "study_prompt.txt",
    "math" : "math_prompt.txt",
    "write" : "writing_prompt.txt",
}

PROMPTS = {
    "default" : """
Answer questions concisely. Format as raw text, and be cognizant that output will be displayed in a shell, so no HTML, newlines etc.
""",

    "rag" : """
You'll be provided a list of sources, and you'll be asked to write a response to a prompt based on the sources.

Please answer as extensively as possible. Always format as RAW TEXT, and be cognizant that output will be displayed in a shell, so no HTML, Markdown formatting, newlines etc.

ALWAYS ANSWER THE QUESTION FULLY. Cite sources whenever it's possible.
"""
}

for key, value in filepaths.items():
    with open(os.path.join(root_dir, value), "r") as f:
        PROMPTS[key] = f.read()
