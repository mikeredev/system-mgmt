""" manage-brightness.py
desc:       adjust screen brightness with xrandr (i3blocks signal 11)
i3:         bindsym $mod+o exec sh -c 'python ~/data/scripts/system-mgmt/manage-brightness.py --monitor $monitor --adjust down && exec pkill -RTMIN+11 i3blocks'
            bindsym $mod+p exec sh -c 'python ~/data/scripts/system-mgmt/manage-brightness.py --monitor $monitor --adjust up && exec pkill -RTMIN+11 i3blocks'
"""

import argparse
import subprocess
import sys

# define constants
MAX_BRIGHTNESS = 1.0
MIN_BRIGHTNESS = 0.5
BRIGHTNESS_INCREMENT = 0.1


def get_brightness():
    # get brightness level
    cmd = ["xrandr", "--verbose"]
    cmd2 = ["grep", str(args.monitor), "-A", "6"]
    cmd3 = ["grep", "-oP", "(?<=Brightness: )[^ ]+"]
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(cmd3, stdin=p2.stdout, stdout=subprocess.PIPE)
    output = p3.communicate()[0].decode("utf-8").strip()
    return float(output)


def set_brightness(level):
    # check level is within allowed bounds
    if level > MAX_BRIGHTNESS:
        print(f"Cannot set brightness level above {MAX_BRIGHTNESS}")
        return
    elif level < MIN_BRIGHTNESS:
        print(f"Cannot set brightness level below {MIN_BRIGHTNESS}")
        return

    # set brightness level
    cmd = ["xrandr", "--output", str(args.monitor), "--brightness", str(level)]
    subprocess.Popen(cmd)

    print(f"New level: {level}")


def adjust_brightness(direction):
    # get current brightness level
    brightness = get_brightness()

    # adjust brightness level
    if direction == "up":
        new_brightness = brightness + BRIGHTNESS_INCREMENT
        if new_brightness > MAX_BRIGHTNESS:
            print("Cannot increase brightness further.")
            sys.exit(2)
    elif direction == "down":
        new_brightness = brightness - BRIGHTNESS_INCREMENT
        if new_brightness < MIN_BRIGHTNESS:
            print("Cannot decrease brightness further.")
            sys.exit(2)
    else:
        sys.exit(1)

    # adjust brightness with new value
    cmd = ["xrandr", "--output", str(args.monitor), "--brightness", str(new_brightness)]
    subprocess.Popen(cmd)

    print(f"New level: {new_brightness}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adjust monitor brightness.")
    parser.add_argument("--monitor", help="Name of the monitor to adjust brightness.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--adjust", choices=["up", "down"], help="Direction to adjust brightness"
    )
    group.add_argument(
        "--set", type=float, help="Set brightness to a specific level (0.5-1.0)"
    )
    args = parser.parse_args()

    try:
        if args.adjust:
            adjust_brightness(args.adjust)
        elif args.set:
            set_brightness(args.set)
    except ImportError as e:
        print(f"Check failed: {e}")
