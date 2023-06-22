import os
import json
import filecmp
import shutil
import datetime

color_reset = "\033[0m"
color_ok = "\033[32m"
color_nok = "\033[31m"
color_log = "\033[2m"

HOME_DIR = os.path.expanduser("~")
CONFIG_FILE = f"{HOME_DIR}/.config/system-mgmt/backup-dotfiles.json"
BACKUP_DIR = f"{HOME_DIR}/data/backup/dotfiles"


def run_function(message, func, *args, **kwargs):
    output = f"=> {message}... "
    print(output, end="")
    try:
        result = func(*args, **kwargs)
        result = f"{color_ok}OK{color_reset} {color_log}{str(result)}{color_reset}"
    except Exception as e:
        result = f"{color_nok}FAIL{color_reset}\n==> {color_log}{str(e)}{color_reset}"
        # return result
    print(result)


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
    print(f"{color_log}{func_output_log}{color_reset}")

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


if __name__ == "__main__":
    run_function("load config", load_configuration)
    run_function("initialise backup", check_backup_structure)
    run_function("execute backup", make_backup)
