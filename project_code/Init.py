#!/usr/bin/env python3

import os
import subprocess
import sys
import argparse
import google.generativeai as genai
from dotenv import load_dotenv
import logging

load_dotenv()

# Configuración inicial de Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
DEFAULT_MODEL = 'gemini-1.5-pro'
logging.basicConfig(filename='/tmp/commit-msg-hook.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

model = genai.GenerativeModel(DEFAULT_MODEL) 

def get_commit_message_from_args(args):
    """Obtiene el mensaje de commit proporcionado en los argumentos."""
    if "-m" in args:
        index = args.index("-m") + 1
        if index < len(args):
            return args[index]
    return None

def modify_commit_message(commit_message):
    """Envía el mensaje de commit a la API de Gemini para su modificación."""
    logging.info("Enviando mensaje de commit a Gemini para su modificación...")
    original_message = commit_message
    try:
        prompt = f"""Improve the following commit message while preserving its original intent. If the message is in Spanish, translate it to English. Follow the Conventional Commits rules:
                - Use feat: for new features and fix: for bug fixes.
                - Use BREAKING CHANGE: in the footer or a ! after the type/scope for breaking changes.
                - Additional types like build:, chore:, ci:, docs:, style:, refactor:, perf:, and test: are allowed.
                - Optionally, include a scope within parentheses after the type to provide additional context (e.g., feat(parser):).
                - The commit message should be clear, concise, and follow these conventions strictly.
                - Correct any spelling or grammar mistakes, and add verbs or any necessary elements to enhance clarity and professionalism.
                - **Do not add any kind of quotes, backticks (\`), or characters around the message, respond only with the string of the message itself.**

                Respond only with the improved commit message and nothing else: {commit_message}"""
        response = model.generate_content(prompt)
        modified_message = response.text.strip() if response and response.text else commit_message
        logging.info(f"Mensaje modificado: {modified_message}")
        return modified_message
    except Exception as e:
        logging.error(f"Error al usar el modelo Gemini: {e}")
        return original_message


def init():
    # Comprobar si se ha pasado el archivo de commit como argumento
    if len(sys.argv) < 2:
        logging.error("No se ha proporcionado un archivo de mensaje de commit.")
        sys.exit(1)

    commit_file = sys.argv[1]

    # Leer el mensaje del archivo
    try:
        with open(commit_file, 'r') as f:
            commit_message = f.read().strip()
    except FileNotFoundError:
        logging.error(f"No se pudo encontrar el archivo: {commit_file}")
        sys.exit(1)

    # Modificar el mensaje usando la API de Gemini
    modified_message = modify_commit_message(commit_message)

    # Sobrescribir el archivo de commit con el mensaje modificado
    with open(commit_file, 'w') as f:
        f.write(modified_message)

def handle_interrupt(signal, frame):
    """Handles Ctrl+C interrupt."""
    print("\nCtrl+C pressed! Exiting...")
    clear_screen()
    sys.exit(0)  

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
