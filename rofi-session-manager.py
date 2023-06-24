""" rofi-session-manager.py
desc:       rofi session manager for i3wm
usage:      rofi-session-manager.py [-h] [--session {lock,logoff,suspend,reboot,shutdown}] [--rofi]
i3 rofi:    bindsym $mod+Shift+l exec --no-startup-id sh -c 'python rofi-session-manager.py --rofi'
i3 lock:    bindsym $mod+l exec --no-startup-id sh -c 'python rofi-session-manager.py --session lock'
"""

# import modules
import subprocess

# variables
custom_theme = True
theme = "~/.config/rofi/themes/dmenu.rasi"
lock_background = "~/Pictures/wallpapers/arch_pixel_dark.png"
lock_cmd = f"i3lock -efi {lock_background}"
logoff_cmd = "i3-msg exit"
suspend_cmd = "systemctl suspend"
reboot_cmd = "systemctl reboot"
shutdown_cmd = "systemctl poweroff"


# function to display options in rofi
def rofi():
    options = ["lock", "logoff", "suspend", "reboot", "shutdown"]
    if custom_theme:
        session_cmd = f"rofi -dmenu -i -p session -theme {theme}"
    else:
        session_cmd = f"rofi -dmenu -i -p session"
    selected_action = subprocess.check_output(
        session_cmd, input="\n".join(options), text=True, shell=True
    ).strip()

    actions = {
        "lock": lock,
        "logoff": logoff,
        "suspend": suspend,
        "reboot": reboot,
        "shutdown": shutdown,
    }

    if selected_action in actions:
        actions[selected_action]()


# function to confirm user action
def confirm_action(action):
    confirmation_prompt = f"🔒 Are you sure you want to {action}?"
    if custom_theme:
        confirmation_cmd = f"rofi -dmenu -i -p '{confirmation_prompt} [y/n]' -lines 2 -eh 2 -theme {theme}"
    else:
        confirmation_cmd = (
            f"rofi -dmenu -i -p '{confirmation_prompt} [y/n]' -lines 2 -eh 2"
        )
    get_confirmation = subprocess.check_output(
        confirmation_cmd, input="y\nn", text=True, shell=True
    ).strip()
    if get_confirmation.lower() == "y":
        confirmation = True
        return confirmation


# function to lock screen
def lock():
    subprocess.run(lock_cmd, shell=True)


# function to log off session
def logoff():
    confirmation = confirm_action("logoff")
    if confirmation:
        subprocess.run(logoff_cmd, shell=True)


# function to suspend system
def suspend():
    confirmation = confirm_action("suspend")
    if confirmation:
        subprocess.run(lock_cmd, shell=True)
        subprocess.run(suspend_cmd, shell=True)


# function to reboot system
def reboot():
    confirmation = confirm_action("reboot")
    if confirmation:
        subprocess.run(reboot_cmd, shell=True)


# function to shutdown system
def shutdown():
    confirmation = confirm_action("shutdown")
    if confirmation:
        subprocess.run(shutdown_cmd, shell=True)


# main
if __name__ == "__main__":
    # setup argparse and process user input
    import argparse

    parser = argparse.ArgumentParser(description="session manager for i3/rofi")
    parser.add_argument(
        "--session",
        "-s",
        choices=["lock", "logoff", "suspend", "reboot", "shutdown"],
        help="select an action",
    )
    parser.add_argument(
        "--rofi",
        "-r",
        action="store_true",
        help="open in rofi",
    )

    args = parser.parse_args()

    # open rofi session manager
    if args.rofi:
        rofi()

    # or process action if passed as command line argument
    elif args.session:
        actions = {
            "lock": lock,
            "logoff": logoff,
            "suspend": suspend,
            "reboot": reboot,
            "shutdown": shutdown,
        }
        selected_action = args.session
        actions[selected_action]()
