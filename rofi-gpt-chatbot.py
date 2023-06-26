""" rofi-gpt-chatbot.py
desc:       creates a chat completion using the OpenAI API
requires:   openai
usage:      python ~/data/scripts/system-mgmt/rofi-gpt-chatbot.py
i3:         bindsym $mod+x exec --no-startup-id sh -c 'python ~/data/scripts/system-mgmt/rofi-gpt-chatbot.py'
"""

# import modules
import openai
import os
import subprocess

# import custom modules from PYTHONPATH
import openai_chat

# load custom theme
theme = "~/.config/rofi/themes/chatbot.rasi"


# main
try:
    # Open rofi bar and get user input
    rofi_cmd = [
        "rofi",
        "-dmenu",
        "-p",
        "🤖 ",
        "-theme",
        theme,
    ]
    user_input = subprocess.check_output(rofi_cmd, universal_newlines=True).strip()

    # send the user_input to the chatcompletion function
    chat_response = openai_chat.chat(
        "Reply briefly and concisely all in one line.", user_input
    )
    chat_output = chat_response["reply"]

    # Display the output in rofi
    rofi_cmd = [
        "rofi",
        "-e",
        "🤖 " + chat_output,
        "-theme",
        theme,
    ]
    subprocess.run(rofi_cmd)
except Exception as e:
    subprocess.run(
        f"notify-send 'rofi-gpt-chatbot' 'error: {e}' -t 3000 -r 1025",
        shell=True,
    )
