"""
gpt-chatbot-console.py
desc:         This script is a command-line interface for a chatbot powered by OpenAI's GPT language model. It allows users to interact with the chatbot by providing prompts and receiving responses.
usage:        python gpt-chatbot-console.py <prompt> [--tokens <int>] [--model <str>] [--temperature <float>]
requirements: The script requires the following modules to be installed: argparse, platform, random, time, colorama, openai_chat.
function:     The script generates a chatbot response based on a given prompt using the OpenAI GPT model. It displays the response in the console with some formatting.
arguments:
  - prompt: The prompt provided by the user to initiate the chatbot conversation.
  - --tokens <int>: (optional) The number of tokens to use for the chatbot's response. Default value is taken from the openai_chat module.
  - --model <str>: (optional) The model to use for generating the response. Default value is taken from the openai_chat module.
  - --temperature <float>: (optional) The temperature parameter for controlling the randomness of the response. Default value is taken from the openai_chat module.
returns:      None
notes:        - The script requires the openai_chat module, which should be accessible in the Python environment.
              - The script uses the colorama module to add color formatting to the console output.
              - The script waits for a short time (0.005 seconds) between printing each character of the response to create a typing effect.
example:      python gpt-chatbot-console.py "Hello, how can I help you?"
"""

# import modules
import argparse
import platform
import random
import time

# import non-standard/custom modules
from colorama import Fore, Style
import openai_chat

if __name__ == "__main__":
    # setup argparse and assign default values
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str)
    parser.add_argument("--tokens", type=int, default=openai_chat.tokens)
    parser.add_argument("--model", type=str, default=openai_chat.model)
    parser.add_argument("--temperature", type=float, default=openai_chat.temperature)
    args = parser.parse_args()

    # generate chat completion
    response = openai_chat.response(
        f"Reply briefly as an expert in {platform.system()} {platform.release()}",
        args.prompt,
        tokens=args.tokens,
        model=args.model,
        temperature=args.temperature,
    )

    # print formatted completion
    print(f"🤖 {Fore.CYAN}", end="")
    for char in response["output"]:
        print(char, end="", flush=True)
        time.sleep(0.005)
    print(f"{Style.RESET_ALL}")
