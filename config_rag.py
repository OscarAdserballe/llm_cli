#!/usr/bin/env python3
from tika import parser 
import sys
import os
from config_llm import LLM
from prompts import PROMPTS
import time
import colored
import logging
import datetime
from config_logger import get_logger
from config_llm import LLM
import click

class RAG(LLM):
    def __init__(self,
                 folder_name,
                system_prompt=PROMPTS["rag"],
                model_name="gemini-1.5-flash"
            ):
        super().__init__(system_prompt=system_prompt, model_name=model_name)
        self.filepaths = self.get_filepaths(folder_name)
        self.context = self.retrieve_context(self.filepaths)
        self.logger = get_logger(__name__)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Log any exceptions that occurred within the context manager
        if exc_type:
            self.logger.error(f"Error during RAG execution: {exc_val}")
        return False  # Don't suppress exceptions

    def fallback_parse_file(self, file_path):
        """Fallback function to parse a file if the parser fails."""
        import pytesseract
        from pdf2image import convert_from_path
        try:
            images = convert_from_path(file_path)
            text = ""
            for image in images:
                text += pytesseract.image_to_string(image)
            filename, extension = os.path.splitext(file_path)
            with open(f"{filename}.txt", "w+") as f:
                f.write(text)
            return text
        except Exception as e:
            self.logger.error(f"Error in fallback parsing: {e}")
            return ""

    def parse_file(self, file_path, timeout_to_write=1):
        """Parses a file using Tika, with a fallback to OCR if Tika fails."""
        try:
            start_time = time.time()
            parsed_file = parser.from_file(file_path, requestOptions={'timeout': 180})
            time_to_parse = time.time() - start_time
            if time_to_parse > timeout_to_write:
                self.logger.info(f"Parsing {file_path} took {time_to_parse} seconds. Writing to .txt file.")
                filename, extension = os.path.splitext(file_path)
                with open(f"{filename}.txt", "w+") as f:
                    f.write(parsed_file['content'])
            return parsed_file['content']
        except Exception as e:
            self.logger.error(f"Failed parsing {file_path}. OCR'ing it\n\n\nError: {e}")
            return self.fallback_parse_file(file_path)

    def validate_version_of_file(self, file_path):
        """Checks if a .txt file exists for a given file_path."""
        file_name, extension = os.path.splitext(file_path)
        if os.path.exists(f"{file_name}.txt") and extension != ".txt":
            return False
        return True

    def retrieve_context(self, files):
        """Retrieves context from a list of files or a single file."""
        if isinstance(files, list):
            return "\n\n".join([f"Document {i+1}: {self.parse_file(file)}" for i, file in enumerate(files)])
        else:
            return self.parse_file(files)

    def get_filepaths(self, folder_name, startswith=None):
        """Gets file paths from a folder, optionally filtering by starting string."""
        if startswith:
            for filename in os.listdir(folder_name):
                if filename.startswith(startswith) and self.validate_version_of_file(os.path.join(folder_name, filename)):
                    return os.path.join(folder_name, filename)
        else:
            return [os.path.join(folder_name, filename)
                    for filename in os.listdir(folder_name)
                    if os.path.isfile(os.path.join(folder_name, filename))
                    and self.validate_version_of_file(os.path.join(folder_name, filename))]

    def query(self, query):
        """Queries the LLM with a prompt and optional context."""
        self.logger.info(f"Query: {query}\n\n\nContext: {self.context}\n\n\n\n\n\n")
        response = super().query(query=query, context=self.context)
        return response

