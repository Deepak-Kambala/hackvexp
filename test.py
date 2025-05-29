#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

# Ensure UTF-8 encoding for input/output (especially on Windows)
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def generate_edge_cases(file_path, model_name="llama3:1b"):
    """
    Generate edge test cases for the given code file using Ollama
    """
    try:
        # Read the file content with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()
        
        # Create the prompt for edge test cases
        prompt = f"""Analyze the following code and generate comprehensive edge test cases.
For each test case, include:
1. Description of what edge case it tests
2. Input values that would trigger this edge case
3. Expected output/behavior
4. Why this case is important to test

Focus on boundary conditions, invalid inputs, and unusual scenarios.
Here's the code:

{code_content}
"""
        print(f"Generating edge test cases for {file_path}...")

        # Run ollama model and send the prompt to stdin
        process = subprocess.Popen(
            ["ollama", "run", model_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Encode prompt and communicate with subprocess
        stdout, stderr = process.communicate(input=prompt.encode('utf-8'))

        # Decode output using utf-8 to avoid UnicodeDecodeError
        stdout = stdout.decode('utf-8', errors='replace')
        stderr = stderr.decode('utf-8', errors='replace')

        if process.returncode != 0:
            print(f"Error generating edge cases:\n{stderr}")
            return None

        return stdout

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def save_edge_cases(file_path, edge_cases):
    """
    Save the edge test cases to a text file
    """
    base_name = os.path.splitext(file_path)[0]
    output_file = f"{base_name}_edge_cases.txt"

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(edge_cases)

    print(f"Edge test cases saved to {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Edge Case Generator using Ollama")
    parser.add_argument("file", help="The code file to generate edge cases for")
    parser.add_argument("--model", default="llama3:1b", help="Ollama model to use")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)

    edge_cases = generate_edge_cases(args.file, args.model)
    if edge_cases:
        save_edge_cases(args.file, edge_cases)

if __name__ == "__main__":
    main()