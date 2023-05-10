import os
import filecmp
import shutil
import datetime

HOME_DIR = os.path.expanduser("~")
BACKUP_DIR = f"{HOME_DIR}/data/backup/dotfiles"

files = [
    # alacritty
    (
        f"{HOME_DIR}/.config/alacritty/alacritty.yml",
        f"{BACKUP_DIR}/alacritty/alacritty.yml",
    ),
    # bashrc
    (f"{HOME_DIR}/.bashrc", f"{BACKUP_DIR}/.bashrc"),
    # code
    (
        f"{HOME_DIR}/.config/Code - OSS/User/settings.json",
        f"{BACKUP_DIR}/Code - OSS/User/settings.json",
    ),
    # gtk settings
    (
        f"{HOME_DIR}/.config/gtk-3.0/settings.ini",
        f"{BACKUP_DIR}/gtk-3.0/settings.ini",
    ),
    # i3
    (f"{HOME_DIR}/.config/i3/config", f"{BACKUP_DIR}/i3/config"),
    # i3blocks
    (
        f"{HOME_DIR}/.config/i3blocks/i3blocks.conf",
        f"{BACKUP_DIR}/i3blocks/i3blocks.conf",
    ),
    (
        f"{HOME_DIR}/.config/i3blocks/i3blocks.py.conf",
        f"{BACKUP_DIR}/i3blocks/i3blocks.py.conf",
    ),
    # i3status
    (
        f"{HOME_DIR}/.config/i3status/i3status.conf",
        f"{BACKUP_DIR}/i3status/i3status.conf",
    ),
    # picom
    (f"{HOME_DIR}/.config/picom/picom.conf", f"{BACKUP_DIR}/picom/picom.conf"),
    # rofi
    (
        f"{HOME_DIR}/.config/rofi/themes/custom_drun.rasi",
        f"{BACKUP_DIR}/rofi/themes/custom_drun.rasi",
    ),
    # vim
    (f"{HOME_DIR}/.vimrc", f"{BACKUP_DIR}/.vimrc"),
]


def check_backup_structure():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    for _, dest_path in files:
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)


def check_backup_status(file, dest):
    backups = {}
    for source_path, dest_path in files:
        if not os.path.exists(dest_path):
            backups[source_path] = dest_path
            continue
        if filecmp.cmp(source_path, dest_path):
            continue
        backups[source_path] = dest_path
    return backups


def make_backup(source, dest):
    backups = check_backup_status(source, dest)
    if not backups:
        print("No changes to backup.")
        return
    print("The following files have changed since the last backup:")
    for source_path, dest_path in backups.items():
        print(f"{source_path} -> {dest_path}")
    print("Do you want to backup these files? (y/n)")
    user_input = input().strip().lower()
    if user_input != "y":
        return
    for source_path, dest_path in backups.items():
        shutil.copy2(source_path, dest_path)
    print("Backup completed.")

    # Create log file
    log_path = os.path.join(dest, "backup.log")
    with open(log_path, "a") as f:
        f.write(f"Backup completed on {datetime.datetime.now()}\n")
        for source_path, dest_path in backups.items():
            f.write(f"{source_path} -> {dest_path}\n")


check_backup_structure()
make_backup(files, BACKUP_DIR)
