import os
import pickle
import tempfile
import threading
import yaml
import urllib.request
import ssl
from os import path
from os import system
from sys import exit
from time import sleep
from shutil import rmtree
from pathlib import Path
from tkinter import Tk
from tkinter import filedialog
import class_animation
import class_threadloading
import mode_edit


def os_check():
    if os.name not in ('nt', 'dos'):
        print("\nThis Program is made for Windows ONLY")
        input("Press Enter to close")
        exit()


def whitelist_length():
    # Count number of files in whitelist
    with open(f"{assets}\\whitelist.yaml", "r") as r:
        data_whitelist = yaml.safe_load(r)
    r.close()
    custom_whitelist = data_whitelist['config']["custom_whitelist"]
    default_whitelist = data_whitelist['config']['default_whitelist']
    all_data = custom_whitelist + default_whitelist
    count = 0
    for _ in all_data:
        count += 1
    return count


def check_update():
    if os.path.exists(f"{owned_roaming}\\updater.exe"):
        os.remove(f"{owned_roaming}\\updater.exe")
    ssl._create_default_https_context = ssl._create_unverified_context
    global server_version, server_version_float
    internal_version = internal_version_float.replace(".", "")  # local exe version (x.x.x) turned into (xxx)
    url = "https://private.storage-backup.us-nyc1.upcloudobjects.com/programming/applications/DeModGTA/update/version" \
          ".txt"
    retry = 0
    while True:
        try:
            version_request = urllib.request.urlopen(url)
            for line in version_request:
                server_version_float = line.decode("utf-8")
                server_version = server_version_float.replace(".", "")
            if internal_version == server_version:
                queue.enque(True)
                break
            else:
                queue.enque(False)
                break
        except Exception:
            retry += 1
            if retry != 10:
                sleep(1)
                continue
            else:
                break


def update_program():
    download_program = "https://private.storage-backup.us-nyc1.upcloudobjects.com/programming/applications/DeModGTA" \
                       "/update/assets/DeModGTAV.exe"
    download_updater = "https://private.storage-backup.us-nyc1.upcloudobjects.com/programming/applications/DeModGTA" \
                       "/update/assets/updater.exe"
    system('cls')
    try:
        urllib.request.urlretrieve(download_program, exe_main)
        print("[File1]: Done")
        urllib.request.urlretrieve(download_updater, exe_updater)
        print("[File2]: Done")
    except Exception:
        print("Network Error")
        input("Press Enter to close")
        exit()


def askdirectory(dir_path):
    _, icon_path = tempfile.mkstemp()
    with open(icon_path, 'wb') as icon_file:
        icon_file.write(ICON)
    root = Tk()
    root.withdraw()
    root.iconbitmap(default=icon_path)  # Use transparent icon for no logo
    dirname = filedialog.askdirectory(parent=root,
                                      initialdir=dir_path,  # default directory when window is opened
                                      title='Select GTAV Folder')
    return dirname


def load(var):
    if path.exists(f"{owned_roaming}\\{var}"):
        save_file = open(f"{owned_roaming}\\{var}", "rb")
        saved_dir = pickle.load(save_file)
        save_file.close()
        print("Save: Loaded")
        return saved_dir
    else:
        new_save = open(f"{owned_roaming}\\{var}", "wb")
        pickle.dump(get_root(), new_save)  # If no save file one is created and the root (C:\, etc) gets entered
        new_save.close()
        print("Created Save File")
        return get_root()


def get_root() -> str:  # Returns the first 3 items (0-2, e.g C:\) of the cwd path
    root = str(Path(__file__))
    return root[:3]


def intro():
    print(f"### GTAV-DeMod ###\nVERSION: {internal_version_float}\n")


def menu1():
    global length
    while True:
        print(f"Files/Folders In Whitelist: [{length - 2}]")  # Give number of items in whitelist -2 example items
        print("\n2 - Edit Whitelist\n1 - Continue\n0 - Exit")
        user = input("\n> ")
        if user == "2":
            system('cls')
            mode_edit.run()
            intro()
            print(f'{STATUS}\n')
            length = whitelist_length()
            continue
        elif user == "1":
            break
        elif user == "0":
            exit()
        else:
            system('cls')
            intro()
            print(f'{STATUS}\n')
            length = whitelist_length()
            continue


server_version = "Unknown"
server_version_float = "Unknown"
internal_version_float = "1.6.20"
STATUS = '[Network Problem Detected]'

os_check()
system('cls')
intro()

appdata = os.getenv('APPDATA')
owned_roaming = appdata + "\\Retards-With-Computers"
assets = owned_roaming + "\\assets"
exe_updater = owned_roaming + "\\updater.exe"
exe_main = owned_roaming + "\\DeModGTAV.exe"


if not os.path.exists(owned_roaming):
    os.mkdir(owned_roaming)
if not os.path.exists(assets):
    os.mkdir(assets)
else:
    pass

# Create whitelist and dump defaults if not exists
if os.path.exists(f'{assets}\\whitelist.yaml'):
    pass
else:
    open(f'{assets}\\whitelist.yaml', 'w')
    mode_edit.dump_whitelist()

# Check for update and display loading animation. Using class_threadloading.py
queue = class_threadloading.Queue()
updatecheck_process = threading.Thread(name='process', target=check_update)
updatecheck_process.start()
while updatecheck_process.is_alive():
    class_animation.animated_loading()
while True:
    flag = queue.isEmpty()
    if flag:
        system('cls')  # This block gets executed when there is a break (everytime) in the else while true loop
        intro()
        break
    else:
        update_check = queue.dequeue()  # True = No Update False = Update
        if not update_check:  # If check_update returns false (local version != server version)
            while True:
                user_update = input(
                    f"""
[Update Available]
{internal_version_float} -> {server_version_float}
Ignoring updates may cause incorrect deletions
Update Now (y, n)?\n> """).casefold()
                if user_update == "y" or user_update == "":
                    current_wd = os.getcwd()
                    stored_cwd = open(f"{assets}\\origin.dat", "wb")  # Save main.exe directory
                    pickle.dump(current_wd, stored_cwd)
                    stored_cwd.close()
                    system('cls')  # Start of update process
                    update_process = threading.Thread(name='process', target=update_program)
                    update_process.start()
                    while update_process.is_alive():
                        class_animation.animated_download()
                    system('cls')
                    print("Starting Updater...")
                    sleep(1)
                    os.startfile(f'{owned_roaming}\\updater.exe')
                    exit()  # End of update process
                elif user_update == "n":
                    STATUS = "Update: IGNORED"
                    break
                else:
                    continue
        else:
            system('cls')
            intro()
            STATUS = "[Up to Date]"
            break


print(f"{STATUS}\n")

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00' * 1282 + b'\xff' * 64  # Transparent base64 pic


# If updater.exe backed up custom items move it to new whitelist
if os.path.exists(f'{owned_roaming}\\item_backup.yaml'):
    with open(f'{owned_roaming}\\item_backup.yaml', "r") as file_descriptor:
        backup_data = yaml.safe_load(file_descriptor)
    file_descriptor.close()
    custom_data = backup_data['temp']
    moved_data = []
    for item in custom_data:
        moved_data.append(item)
    with open(f'{assets}\\whitelist.yaml', "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    file_descriptor.close()
    for filename in moved_data:
        data["config"]["custom_whitelist"].append(filename)
    with open(f'{assets}\\whitelist.yaml', 'w') as f:
        yaml.dump(data, f)
    f.close()
    os.remove(f'{owned_roaming}\\item_backup.yaml')
else:
    pass


sleep(.2)
length = whitelist_length()

saved_game_dir = load("save.dat")  # Call load function to load in file named save.dat


menu1()


# Make whitelist
with open(f"{assets}\\whitelist.yaml", "r") as file_descriptor:
    data = yaml.safe_load(file_descriptor)
file_descriptor.close()
user_whitelist = data['config']["custom_whitelist"]
game_whitelist = data['config']['default_whitelist']
whitelist = user_whitelist + game_whitelist


# Ask and Store game directory location
while True:
    print("\nSelect The GTAV Folder")
    try:
        raw_game_dir = askdirectory(saved_game_dir)
        if raw_game_dir == "":  # If nothing entered in window (If window is closed)
            system('cls')
            intro()
            print(f'{STATUS}\n')
            length = whitelist_length()
            menu1()
        else:
            game_dir = raw_game_dir.replace("/", "\\")
            check_game_dir = os.path.join(game_dir, "update\\update.rpf")
            print(f"GameDir: [{game_dir}]")
            if path.exists(check_game_dir):
                print("DIR: OK")
                if game_dir != saved_game_dir:  # If entered directory doesn't match save files directory
                    f = open(owned_roaming + "\\save.dat", "wb")
                    pickle.dump(game_dir, f)  # Save Game Directory
                    f.close()
                    print("DIR: Saved")
                    break
                else:
                    break
            else:
                print("DIR: BAD\n")
                continue
    except OSError:
        print("**EXIT**")
        exit()

# Confirm and then delete non-whitelist files
while True:
    all_files = os.listdir(game_dir)
    dir_amount = len(all_files)
    for file in all_files:  # Number of files to be deleted/not in whitelist
        if file in whitelist:
            dir_amount -= 1
    del_files = dir_amount
    if del_files == 0:
        print("\nGTAV: Folder Already Default")
        input("\n\nPress Enter to close")
        exit()
    print(f"\nATTENTION: [{del_files}] Item(s) will be removed")
    user_check = input("Do you want to continue (y, n)?\n> ").casefold()
    if user_check == "y" or user_check == "":
        print("**Prepping**\n")
        os.chdir(game_dir)
        sleep(1)  # Making script feel less robotic
        for file in all_files:  # non-whitelist files will be deleted
            if file not in whitelist:
                folder = os.path.isdir(game_dir + f"\\{file}")
                if folder:  # check if file is a directory (dirs need specific deletion)
                    rmtree(game_dir + f"\\{file}")
                    print(f"Removed: {file}")
                else:  # If not a directory use normal deletion
                    os.remove(file)
                    print(f"Removed: {file}")
            else:  # If file is in whitelist "continue" on with loop
                continue
        print("\nCompleted!")  # End Of Program
        input("\nPress Enter to close")  # Stops cmd from closing
        exit()
    elif user_check == "n":
        print("\nProgram Ended")
        sleep(1)
        exit()
    else:
        continue
