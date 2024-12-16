#!/usr/bin/env python3
from tika import parser 
import sys
import os
import time

from llm_utils.models.llm import LLM
from llm_utils.prompts.prompts import PROMPTS
from llm_utils.parameters import CONFIG\

from config_logger import get_logger

class RAG(LLM):
    def __init__(self,
                 folder_name,
                system_prompt=PROMPTS["default"],
                route=True,
                model_name=CONFIG['base_model'],
                use_chat_history=True,
                is_recursive=False,
                startswith=None
            ):
        super().__init__(
            system_prompt=system_prompt,
            model_name=model_name,
            route=route,
            use_chat_history=use_chat_history
        )
        self.is_recursive = is_recursive
        self.startswith = startswith
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

    def validate_file(self, file_path):
        """Checks if a .txt file exists for a given file_path and is not illegal type."""
        illegal_extensions = [
            ".pyc", ".img", ".jpg", ".jpeg", ".png", ".gif", ".log", ".csv",
            ".zip", ".tar", ".gz", ".tgz", ".csv", ".xls", ".xlsx",
        ]
        file_name, extension = os.path.splitext(file_path)
        if os.path.exists(f"{file_name}.txt") \
            and extension != ".txt" \
            and extension not in illegal_extensions:

            return False
        
        return True

    def retrieve_context(self, files):
        """Retrieves context from a list of files or a single file."""
        if isinstance(files, list):
            return "\n\n".join([f"Document {i+1}: {self.parse_file(file)}" for i, file in enumerate(files)])
        else:
            return self.parse_file(files)

    def get_filepaths(self, folder_name):
        """Gets file paths from a folder, optionally filtering by starting string."""
        file_paths = []
        for item in os.listdir(folder_name):
            item_path = os.path.join(folder_name, item)
            if os.path.isfile(item_path) and self.validate_file(item_path):
                if self.startswith and item.startswith(self.startswith):
                    file_paths.append(item_path)
                elif not self.startswith:
                    file_paths.append(item_path)
            elif os.path.isdir(item_path) and self.is_recursive:
                file_paths.extend(self.get_filepaths(item_path))
        return file_paths

    def query(self, query):
        """Queries the LLM with a prompt and optional context."""
        self.logger.info(f"Files used: {self.filepaths}, Query: {query}")
        response = super().query(query=query, context=self.context)
        return response

