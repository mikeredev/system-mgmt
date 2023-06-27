""" backup-dotfiles.py
desc:       check selected files for changes and copy them to another folder
requires:   colorama, custom module (modules repo)
usage:      python backup-dotfiles.py
"""

# import modules
from colorama import Style
import datetime
import filecmp
import json
import os
import shutil
import sys

# import non-standard/custom modules
import run_function

# constants
HOME_DIR = os.path.expanduser("~")
CONFIG_FILE = f"{HOME_DIR}/.config/system-mgmt/backup-dotfiles.json"
BACKUP_DIR = f"{HOME_DIR}/data/backup/dotfiles"


# function to load CONFIG_FILE
def load_configuration():
    global files_for_backup
    func_output = ""
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    files_for_backup = [
        (
            os.path.join(HOME_DIR, file_config["source"]),
            os.path.join(BACKUP_DIR, file_config["destination"]),
        )
        for file_config in config["backup-dotfiles"]
    ]
    return func_output


# function to check backup folder directory structure
def check_backup_structure():
    func_output = ""
    # make parent dir if not existing
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        func_output += "\n==> created main directory: " + BACKUP_DIR

    # create any required sub-folders
    for _, dest_path in files_for_backup:
        dest_dir = os.path.dirname(dest_path)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            func_output += "\n==> created directory: " + dest_dir
    return func_output


# function to compare files listed in CONFIG_FILE
def check_backup_status():
    backups = {}
    for source_path, dest_path in files_for_backup:
        if not os.path.exists(dest_path):
            backups[source_path] = dest_path
            continue
        if filecmp.cmp(source_path, dest_path):
            continue
        backups[source_path] = dest_path
    return backups


# function to copy any changed files to BACKUP_DIR
def make_backup():
    func_output = ""
    backups = check_backup_status()
    if not backups:
        func_output += "\n==> no changes to back up"
        return func_output

    # if new files found
    func_output_log = "new files found"
    for source_path, dest_path in backups.items():
        func_output_log += f"\n==> {source_path} -> {dest_path}"
    print(f"{Style.DIM}{func_output_log}{Style.RESET_ALL}")

    # get user confirmation to continue
    print(f"=> do you want to backup these files? (y/n) ", end="")
    user_input = input().strip().lower()
    if user_input != "y":
        func_output += "==> backup cancelled"
        return func_output

    # make backup
    for source_path, dest_path in backups.items():
        shutil.copy2(source_path, dest_path)
    func_output += "==> backup complete"

    # write to log file
    log_path = os.path.join(BACKUP_DIR, "backup.log")
    with open(log_path, "a") as f:
        f.write(f"Backup completed on {datetime.datetime.now()}\n")
        for source_path, dest_path in backups.items():
            f.write(f"{source_path} -> {dest_path}\n")
    return func_output


# main
if __name__ == "__main__":
    run_function.run(load_configuration, "load config")
    run_function.run(check_backup_structure, "initialise backup")
    run_function.run(make_backup, "execute backup")
