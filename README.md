# LLM-based CLI - Retrieval Augmented Generation from Your Command Line

This repository contains a Python CLI tool designed for basic LLM tasks along with retrieval augmented generation (RAG) tasks leveraging Google's Gemini AI models to answer questions. Currently default model called is always gemini-1.5-flash.

Current "models":
* Router: Before calling each query, router-llm is instantiated to classify which prompts (defined in /prompts folder is most relevant)
* LLM: Model to call simple prompt. Initialises most appropriate system prompt using router.
* RAG: Based on the current working directory it fetches all files using tika parser and inserts them into context of query.

## Features

* **Easy-to-use CLI:**  Interact with the model using simple command-line prompts.
* **Contextualized Responses:**  Provide documents for context and receive answers grounded in the provided information.
* **Document Parsing:**  Automatically parses various document formats (e.g., PDF, TXT) using Tika and OCR (if Tika fails). If it's a time-cnsuming process, defined as logner than 1 second, a .txt version is also written that's used for future prompts instead.
* **Multiple System Prompts:** Choose from pre-defined system prompts for different query types (e.g., coding, writing, study).
* **Router**: Based on query, routes to model initialised with most appropriate system prompt.
* **Logging:**  Track all queries, responses, and errors for debugging and analysis.

## Installation

1. **Install Required Packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variable:**
   - Obtain your Gemini API key from the Google AI Platform
   - Export the API key as an environment variable:
     ```bash
     export GEMINI_API_KEY=YOUR_API_KEY
     ```

## Usage

```bash
# Run the CLI
python .../cli_rag.py "<your query>"
```

## Usage CLI:

Instead of running the python files, you can set up an alias in your shell configuration file to access it from anywhere. This is especially useful for the rag functionality, as you can just have the terminal open in the folder you want to use the sources from, e.g. a code-base (though note no recursion yet through directories!) and call rag "<query>" from there to insert it into the query context.

```bash
# Running file as per usual
python .../cli_rag.py "<your query>"

rag "<your query>"
```

Configure it by setting alias as follows in your shell configuration file and saving afterwards:
```bash
alias llm="python .../cli_llm.py"
alias rag="python .../cli_rag.py" 
```

And then ensure scripts are executable using chmod +x
```bash
chmod +x .../cli_rag.py
chmod +x .../cli_llm.py
```

Ensure to save the reconfigured shell file.

**Options:**

* `--system-prompt`: Choose a specific system prompt for the query type.  The current available options from the /prompts folder are are:
    * `default`: General-purpose prompt for basic questions.
    * `rag`:  Prompt for retrieval augmented generation tasks.
    * `code`:  Prompt for code-related queries.
    * `study`:  Prompt for study/learning-related queries.
    * `math`:  Prompt for mathematical questions.
    * `write`: Prompt for writing-related queries.

**Example with Documents:**

1. Place the documents you want to use for context in the current directory.
2. Run the following command from the CLI:

   ```bash
   rag "What is the main theme of this document?" --system-prompt rag
   ```

**Output:**

The tool will display the response from the Gemini model, grounded in the provided context.  The response will also be logged to a file for future reference.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. 

## Acknowledgements

This project is built upon the Google Gemini API and utilizes Tika and PyTesseract for document parsing. 

