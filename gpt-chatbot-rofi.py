""" 
gpt-chatbot-rofi.py
desc:         This script allows the user to interact with a chatbot using the Rofi interface. It prompts the user with a message input field in Rofi, sends the user input to the chatbot for processing, and displays the chatbot's response in Rofi.
usage:        Run this script to start the chatbot interface in Rofi.
requirements: The script requires the following modules to be installed: os, subprocess, openai_chat.
function:     The main function of this script is to provide a chatbot interface using Rofi.
arguments:    None.
returns:      None.
notes:        The script assumes that the Rofi theme file is located at ~/.config/rofi/themes/chatbot.rasi.
example:      python gpt-chatbot-rofi.py
"""

# import modules
import os
import subprocess

# import non-standard/custom modules
import openai_chat

# define constants
custom_theme = "~/.config/rofi/themes/chatbot.rasi"

# main
if __name__ == "__main__":
    try:
        # Open rofi bar and get user input
        rofi_cmd = ["rofi", "-dmenu", "-p", "🤖 ", "-theme", custom_theme]
        user_input = subprocess.check_output(rofi_cmd, universal_newlines=True).strip()

        # send the user_input to the chatcompletion function
        response = openai_chat.response(
            "Reply helpfully in one concise line.", user_input
        )

        # Display the output in rofi
        rofi_cmd = ["rofi", "-e", "🤖 " + response["output"], "-theme", custom_theme]
        subprocess.run(rofi_cmd)

    except Exception as e:
        subprocess.run(
            f"notify-send 'rofi-gpt-chatbot' 'error: {e}'",
            shell=True,
        )
