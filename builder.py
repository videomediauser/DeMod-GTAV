import os
from shutil import rmtree
cwd = os.getcwd()
build_dir = f'{cwd}\\BUILD'
app_dir = f'{build_dir}\\app'
update_dir = f'{build_dir}\\update'
misc_dir = f'{build_dir}\\__misc__'
root_app = f'{cwd}\\app'
root_update = f'{cwd}\\update'


# Verify Pyinstaller is installed
while True:
    installed = (os.system(f"pyinstaller"))
    os.system('cls')
    if installed == 1 or 2:  # 1 = not installed, 2 = installed
        if installed != 2:
            user = input("PyInstaller is not Installed on this System\nDo You Want to Install PyInstaller? (y, n)?\n> ") \
                .casefold()
            if user == 'y':
                os.system("pip install pyinstaller")
                continue
            elif user == 'n':
                os.system('cls')
                exit()
            else:
                continue
        else:  # If pyinstaller is installed
            break
    else:
        input("Failed to Verify PyInstaller Status\nPress ENTER to exit")
        exit()


# Verify File Locations
verify = True

app_required = ['main.py', 'mode_edit.py', 'class_animation.py', 'class_threadloading.py']
compare_app = []
app_missing = []
app_files = os.listdir(root_app)
for file in app_files:
    if file in app_required:
        compare_app.append(file)
if len(app_required) != len(compare_app):  # If all required files aren't found
    verify = False
    for f in app_required:
        if f not in compare_app:
            app_missing.append(f)
    print(f'Required files Missing from: {root_app}\n{app_missing}')

update_required = ['updater.py']
compare_update = []
update_missing = []
updater_files = os.listdir(root_update)
for file in updater_files:
    if file in update_required:
        compare_update.append(file)
if len(update_required) != len(compare_update):  # If all required files aren't found
    verify = False
    for f in update_required:
        if f not in compare_update:
            update_missing.append(f)
    print(f'Required files Missing from: {root_update}\n{update_missing}')

if verify is False:  # If any of the required files are missing
    input('\nPress ENTER to exit')
    exit()


def ico_check():
    """Verify if user wants to use icons
    Icons must be labeled "main_icon.ico" and "updater_icon.ico"
    Place these in the root of the repo"""
    while True:
        os.system('cls')
        usr = input('Use Icons (y, n)?\n').casefold()
        if usr == 'y':
            ico_files = ['main_icon.ico', 'updater_icon.ico']
            for icon in ico_files:
                if not os.path.exists(f'{cwd}\\{icon}'):
                    while True:
                        cont_usr = input('Icon files not found\nContinue (y, n)?\n> ').casefold()
                        if cont_usr == 'y':  # If user doesn't want to use icons
                            return False
                        elif cont_usr == 'n':
                            exit()
                        else:
                            continue
                else:  # If all Icon files are found
                    return True
        elif usr == 'n':  # If user doesn't want to use icons
            return False
        else:
            continue


def build(use_ico):
    """Build and store program"""
    os.system('cls')
    print(f'builder.py: Use Icons = {use_ico}')
    print('builder.py: BUILD Starting...\n')

    # Create BUILD folders
    print('builder.py: Creating BUILD Directory')
    if os.path.exists(build_dir):  # Clear BUILD folder
        try:
            rmtree(build_dir)
        except BaseException as rmerr:
            input(f'Failed to clear the BUILD folder\nERROR: {rmerr}')
            exit()
    try:  # Create BUILD directory's
        os.mkdir(build_dir)
        os.mkdir(app_dir)
        os.mkdir(update_dir)
        os.mkdir(misc_dir)
    except BaseException as mkerr:
        input(f'Failed to create BUILD folders\nERROR: {mkerr}')
        exit()
    print('builder.py: BUILD Directory Created')

    # Build program using pyinstaller
    if use_ico is True:
        main_command = f"pyinstaller --noconfirm --onefile --console --icon '{cwd}\\main_icon.ico' " \
                       f"--add-data '{root_app}\\class_animation.py;.' --add-data " \
                       f"'{root_app}\\class_threadloading.py;.' --add-data " \
                       f"'{root_app}\\mode_edit.py;.'  '{root_app}\\main.py' "
        updater_command = "pyinstaller --noconfirm --onefile --console --icon " \
                          f"'{cwd}\\updater_icon.ico'  '{root_update}\\updater.py' "
        main = main_command.replace("'", '"')
        updater = updater_command.replace("'", '"')

        print("\nbuilder.py: Compiling main.py")
        os.system(main)  # Compile main
        print("\nbuilder.py: main.py Compiled Successfully")

        print("\nbuilder.py: Compiling updater.py")
        os.system(updater)  # Compile updater
        print("\nbuild.py: updater.py Compiled Successfully")
    else:
        main_command = f"pyinstaller --noconfirm --onefile --console " \
                       f"--add-data '{root_app}\\class_animation.py;.' --add-data " \
                       f"'{root_app}\\class_threadloading.py;.' --add-data " \
                       f"'{root_app}\\mode_edit.py;.'  '{root_app}\\main.py' "
        updater_command = "pyinstaller --noconfirm --onefile --console " \
                          f"'{root_update}\\updater.py' "
        main = main_command.replace("'", '"')
        updater = updater_command.replace("'", '"')

        print("\nbuilder.py: Compiling main.py")
        os.system(main)  # Compile main
        print("\nbuilder.py: main.py Compiled Successfully")

        print("\nbuilder.py: Compiling updater.py")
        os.system(updater)  # Compile updater
        print("\nbuilder.py: updater.py Compiled Successfully")


# BUILD
while True:
    final_verify = input('Do you want to compile this program (y, n)?\n> ').casefold()
    if final_verify == 'y':
        os.system('cls')
        try:
            build(ico_check())
            break
        except BaseException as be:
            print(f"\nERROR While Building\nException: {be}")
            input('Press ENTER to exit')
            exit()
    elif final_verify == 'n':
        exit()
    else:
        continue


# Clean up
try:  # Move executables to their respected BUILD folders
    os.replace(f'{cwd}\\dist\\main.exe', f'{app_dir}\\main.exe')
    os.replace(f'{cwd}\\dist\\updater.exe', f'{update_dir}\\updater.exe')
    rmtree(f'{cwd}\\dist')
except FileNotFoundError:
    print("Compiled Files Not Found")

root_files = os.listdir(cwd)
build_files = os.listdir(build_dir)
root_movable_files = ['main.spec', 'updater.spec', 'main_icon.ico', 'updater_icon.ico']
build_movable_files = ['main', 'updater']

# Move everything else to __misc__
for r in root_files:
    if r in root_movable_files:
        os.replace(f'{cwd}\\{r}', f'{misc_dir}\\{r}')
for b in build_files:
    if b in build_movable_files:
        os.replace(f'{build_dir}\\{b}', f'{misc_dir}\\{b}')

# Remove __pycache__ from app and update folder
if os.path.exists(f'{root_app}\\__pycache__'):
    rmtree(f'{root_app}\\__pycache__')
if os.path.exists(f'{root_update}\\__pycache__'):
    rmtree(f'{root_update}\\__pycache__')

# Rename main.exe to DeModGTAV.exe
os.rename(f'{app_dir}\\main.exe', f'{app_dir}\\DeModGTAV.exe')


print('\nDONE\n')
exit()
