"""
manage-screenshot.py
desc:         Script to take screenshots of the full screen or a selected area and copy them to the clipboard.
usage:        python manage-screenshot.py [--type {full, area}]
requirements: The script requires the following modules to be imported: os, random, time, subprocess, argparse.
function:     The script takes a screenshot of the full screen or a selected area, saves it as a PNG file with a unique filename, and then copies it to the clipboard.
arguments:    The script accepts an optional argument '--type' to specify the type of screenshot: 'full' for a screenshot of the full screen (default), or 'area' for a screenshot of a selected area.
returns:      The script does not have a return value.
notes:        The screenshots are saved in the 'Pictures/screenshots' directory in the user's home directory. The scrot command-line tool is used to capture the screenshots, and the xclip command-line tool is used to copy the screenshots to the clipboard.
example:      To take a screenshot of the full screen and copy it to the clipboard, run the script with no arguments: 'python manage-screenshot.py'. To take a screenshot of a selected area and copy it to the clipboard, run the script with the '--type area' argument: 'python manage-screenshot.py --type area'.
"""

# import modules
import os
import random
import time
import subprocess
import argparse


# function to take screenshot (fullscreen / area)
def take_screenshot(screenshot_type="full"):
    date = time.strftime("%Y-%m-%d")
    rand_num = str(random.randint(10000, 99999))
    filename = f"{date}-{rand_num}_{'f' if screenshot_type=='full' else 's'}.png"
    file_path = os.path.join(os.environ["HOME"], "Pictures", "screenshots", filename)
    if screenshot_type == "full":
        subprocess.run(["scrot", file_path], check=True)
    else:
        subprocess.run(["scrot", "-s", file_path], check=True)
    copy_to_clipboard(file_path)


# function to copy image to clipboard
def copy_to_clipboard(image_path):
    subprocess.run(
        ["xclip", "-selection", "clipboard", "-t", "image/png", image_path], check=True
    )


# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Take a screenshot of the full screen or a selected area and copy it to the clipboard"
    )
    parser.add_argument(
        "--type",
        choices=["full", "area"],
        default="full",
        help="Type of screenshot to take (default: full)",
    )
    args = parser.parse_args()
    take_screenshot(args.type)
