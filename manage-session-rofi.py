#!/usr/bin/env python3

import subprocess

options = ["lock", "logoff", "suspend", "reboot", "shutdown"]
chosen = subprocess.check_output(
    ["rofi", "-dmenu", "-i", "-p", "session"],
    input="\n".join(options),
    text=True,
).strip()

if chosen == "lock":
    subprocess.run(["i3lock"])
elif chosen == "logoff":
    confirm = subprocess.check_output(
        [
            "rofi",
            "-dmenu",
            "-i",
            "-p",
            "Are you sure you want to logoff? [y/n]",
            "-lines",
            "2",
            "-eh",
            "2",
        ],
        input="y\nn",
        text=True,
    ).strip()
    if confirm.lower() == "y":
        subprocess.run(["i3-msg", "exit"])
elif chosen == "suspend":
    subprocess.run(["i3lock"])
    subprocess.run(["systemctl", "suspend"])
elif chosen == "reboot":
    confirm = subprocess.check_output(
        [
            "rofi",
            "-dmenu",
            "-i",
            "-p",
            "Are you sure you want to reboot? [y/n]",
            "-lines",
            "2",
            "-eh",
            "2",
        ],
        input="y\nn",
        text=True,
    ).strip()
    if confirm.lower() == "y":
        subprocess.run(["systemctl", "reboot"])
elif chosen == "shutdown":
    confirm = subprocess.check_output(
        [
            "rofi",
            "-dmenu",
            "-i",
            "-p",
            "Are you sure you want to shutdown? [y/n]",
            "-lines",
            "2",
            "-eh",
            "2",
        ],
        input="y\nn",
        text=True,
    ).strip()
    if confirm.lower() == "y":
        subprocess.run(["systemctl", "poweroff"])
else:
    pass
