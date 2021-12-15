import os
from shutil import rmtree
from time import sleep

cwd = os.getcwd()
main_out = f'{cwd}\\main-out'
updater_out = f'{cwd}\\updater-out'
files = f'{cwd}\\files'


def compile_main():
    main = main_command.replace("'", '"')
    os.system(main)


def compile_updater():
    updater = updater_command.replace("'", '"')
    os.system(updater)


def cleanup():
    delete_list = ["__pycache__", "build", "dist", "main.spec", "updater.spec"]
    for item in dir_files:
        if item not in delete_list:
            folder = os.path.isdir(cwd + f"\\{item}")
            if folder:
                pass
            else:
                os.replace(f'{cwd}\\{item}', f'{files}\\{item}')
        else:
            folder = os.path.isdir(cwd + f"\\{item}")
            if folder:
                rmtree(cwd + f"\\{item}")
            else:
                os.remove(item)


try:
    # Clean output paths
    if os.path.exists(main_out):
        rmtree(main_out)
    os.mkdir(main_out)
    if os.path.exists(updater_out):
        rmtree(updater_out)
    os.mkdir(updater_out)
    if os.path.exists(files):
        pass
    else:
        os.mkdir(files)

    main_command = f"pyinstaller --noconfirm --onefile --console --icon '{cwd}\\main_png.ico' " \
                   f"--add-data '{cwd}\\class_animation.py;.' --add-data " \
                   f"'{cwd}\\class_threadloading.py;.' --add-data " \
                   f"'{cwd}\\mode_edit.py;.'  '{cwd}\\main.py' "

    updater_command = "pyinstaller --noconfirm --onefile --console --icon " \
                      f"'{cwd}\\updater_png.ico'  '{cwd}\\updater.py' "

    compile_main()
    compile_updater()
    sleep(1)
    os.replace(f'{cwd}\\dist\\main.exe', f'{main_out}\\main.exe')
    os.replace(f'{cwd}\\dist\\updater.exe', f'{updater_out}\\updater.exe')

    # Gather file info in cwd
    raw_dir = os.listdir(cwd)
    dir_files = []
    ico_files = []
    py_files = []
    for file in raw_dir:
        if file == "builder.py":  # ignore builder program
            continue
        elif file[-3:] == "ico":
            ico_files.append(file)
        elif file[-2:] == "py":
            py_files.append(file)
        dir_files.append(file)

    cleanup()


except Exception as error:
    print()
    print(f'Build.py ERROR: {error}')
    print()
    print("Names of files must be exact in commands")
    input()
