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

# load custom theme
theme = "~/.config/rofi/themes/chatbot.rasi"

# load default model (from .bashrc)
model = os.environ.get("OPENAI_MODEL")


# function to generate chat completion
def generate_chat_completion(messages):
    response = openai.ChatCompletion.create(
        temperature=0,
        max_tokens=150,
        model=model,
        messages=messages,
    )
    reply = response.choices[0].message.content
    return {"reply": reply}


# function to generate response
def chat(query):
    system_prompt = "Reply briefly and concisely all in one line."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]
    output = generate_chat_completion(messages)
    return output


def main():
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
    chat_response = chat(user_input)
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


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        subprocess.run(
            "notify-send 'rofi-gpt-chatbot' 'an error occurred communicating with the server' -t 3000 -r 1025",
            shell=True,
        )
