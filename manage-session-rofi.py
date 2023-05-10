#!/usr/bin/env python3

import subprocess

options = ["Lock", "Logoff", "Suspend", "Reboot", "Shutdown"]
chosen = subprocess.check_output(
    ["rofi", "-dmenu", "-i", "-p", "Manage Session"],
    input="\n".join(options),
    text=True,
).strip()

if chosen == "Lock":
    # lock the screen using i3lock
    subprocess.run(["i3lock"])
elif chosen == "Logoff":
    # log off the current session using i3-msg
    subprocess.run(["i3-msg", "exit"])
elif chosen == "Suspend":
    # lock the screen using i3lock
    subprocess.run(["i3lock"])
    # suspend the computer using systemctl
    subprocess.run(["systemctl", "suspend"])
elif chosen == "Reboot":
    # prompt the user for confirmation using rofi
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
        # reboot the computer using systemctl
        subprocess.run(["systemctl", "reboot"])
elif chosen == "Shutdown":
    # prompt the user for confirmation using rofi
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
        # shut down the computer using systemctl
        subprocess.run(["systemctl", "poweroff"])
else:
    # do nothing if an invalid option is selected
    pass
