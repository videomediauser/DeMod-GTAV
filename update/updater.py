import os
import time
import pickle
from sys import exit
import sys
import yaml
from shutil import rmtree

time.sleep(1)
program_location = None
appdata = os.getenv('APPDATA')
owned_roaming = appdata + "\\Retards-With-Computers"
assets = owned_roaming + "\\assets"

print("FINAL CHECKS\n")
animation = ["[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]",
             "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]

for i in range(len(animation)):
    time.sleep(0.2)
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
print("\n")


try:
    stored_dir = open(f"{assets}\\origin.dat", "rb")
    program_location = pickle.load(stored_dir)
    stored_dir.close()
except FileNotFoundError:
    print("Cannot Find Program")
    input("Press Enter to close")
    exit()

old_program = f"{program_location}\\DeModGTAV.exe"
new_program = f"{owned_roaming}\\DeModGTAV.exe"

if os.path.exists(old_program):
    pass
else:
    print("ERROR")
    input("Press Enter to close")
    exit()
if os.path.exists(new_program):
    pass
else:
    print("Program Not Found")
    input("Press Enter to close")
    exit()

os.replace(new_program, old_program)

with open(f'{assets}\\whitelist.yaml', "r") as file_descriptor:
    asset_data = yaml.safe_load(file_descriptor)
file_descriptor.close()
custom_whitelist = asset_data['config']["custom_whitelist"]
store_items = []
for item in custom_whitelist:
    if item == 'Example_File.dll':
        continue
    elif item == 'Example_Folder':
        continue
    store_items.append(item)
length_store_items = len(store_items)
if length_store_items > 0:
    f = open(f'{owned_roaming}\\item_backup.yaml', 'w')
    f.close()
    temp = {'temp': [

    ]
    }
    with open(f'{owned_roaming}\\item_backup.yaml', "w") as f:
        yaml.dump(temp, f, default_flow_style=False)
    f.close()
    with open(f'{owned_roaming}\\item_backup.yaml', "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    file_descriptor.close()
    for item in store_items:
        if item == 'Example_File.dll':
            continue
        elif item == 'Example_Folder':
            continue
        data["temp"].append(item)
    with open(f'{owned_roaming}\\item_backup.yaml', 'w') as f:
        yaml.dump(data, f)
    f.close()

rmtree(assets)
time.sleep(.2)

os.startfile(f'{program_location}\\DeModGTAV.exe')
exit()
