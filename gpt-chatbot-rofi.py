""" gpt-chatbot-rofi.py
desc:       creates a chat completion using the OpenAI API
requires:   openai
usage:      python ~/data/scripts/system-mgmt/gpt-chatbot-rofi.py
i3:         bindsym $mod+x exec --no-startup-id sh -c 'python ~/data/scripts/system-mgmt/gpt-chatbot-rofi.py'
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
