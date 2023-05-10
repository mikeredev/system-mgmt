import os
import random
import time
import subprocess
import argparse


def copy_to_clipboard(image_path):
    subprocess.run(
        ["xclip", "-selection", "clipboard", "-t", "image/png", image_path], check=True
    )


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
