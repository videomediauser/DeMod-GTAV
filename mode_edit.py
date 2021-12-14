import yaml
from os import system
import os

appdata = os.getenv('APPDATA')
owned_roaming = appdata + "\\Retards-With-Computers"
assets = owned_roaming + "\\assets"

whitelist = {'config': {'default_whitelist': [
    "x64a.rpf", "x64b.rpf", "x64c.rpf", "x64d.rpf", "x64e.rpf", "x64f.rpf", "x64g.rpf", "x64h.rpf", "x64i.rpf",
    "x64j.rpf", "x64k.rpf", "x64l.rpf", "x64m.rpf", "x64n.rpf", "x64o.rpf", "x64p.rpf", "x64q.rpf", "x64r.rpf",
    "x64s.rpf", "x64t.rpf", "x64u.rpf", "x64v.rpf", "x64w.rpf", "steam_api64.dll", "PlayGTAV.exe",
    "GTAVLauncher.exe", "GTAVLanguageSelect.exe", "GTA5.exe", "GFSDK_TXAA_AlphaResolve.win64.dll",
    "GFSDK_TXAA.win64.dll", "GFSDK_ShadowLib.win64.dll", "d3dcsx_46.dll", "d3dcompiler_46.dll", "common.rpf",
    "commandline.txt", "bink2w64.dll", "x64", "update", "Installers", "installscript.vdf", "Redistributables",
    ".egstore", "ReadMe", "licenses", "GPUPerfAPIDX-x64.dll", "EOSSDK-Win64-Shipping.dll", "Gwen.dll",
    "Gwen.UnitTest.dll", "LMS.Common.dll", "LMS.PortableExecutable.dll", "Microsoft.Expression.Drawing.dll",
    "Microsoft.VisualStudio.QualityTools.UnitTestFramework.dll", "NvPmApi.Core.win64.dll",
    "System.ValueTuple.dll", "FW1FontWrapper", "GPUPerfAPIDX11-x64.dll", "version.txt"
],
    'custom_whitelist': [
        'Example_File.dll', 'Example_Folder'
    ]
}
}


def dump_whitelist():
    with open(f'{assets}\\whitelist.yaml', "w") as f:
        yaml.dump(whitelist, f, default_flow_style=False)
    f.close()


def whitelist_add(filename):
    with open(f'{assets}\\whitelist.yaml', "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    file_descriptor.close()
    data["config"]["custom_whitelist"].append(filename)
    with open(f'{assets}\\whitelist.yaml', 'w') as f:
        yaml.dump(data, f)
    f.close()


def whitelist_del(filename):
    with open(f'{assets}\\whitelist.yaml', "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    file_descriptor.close()
    data["config"]["custom_whitelist"].remove(filename)
    with open(f'{assets}\\whitelist.yaml', 'w') as f:
        yaml.dump(data, f)
    f.close()


def display_whitelist(viewall):
    iox = 0
    group = 1
    with open(f'{assets}\\whitelist.yaml', "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    file_descriptor.close()
    custom_whitelist = data['config']["custom_whitelist"]
    default_whitelist = data['config']['default_whitelist']
    all_data = custom_whitelist + default_whitelist
    if viewall is True:
        print("##Group 1##")
        for item in all_data:
            print(item)
            iox += 1
            if iox == 5:
                group += 1
                iox = 0
                print(f"\n##Group {group}##")
        print("\n############\n[Edit Mode]\n############\n")
        print("add = Add Item")
        print("del = Remove Item")
        print("viewless = Show Custom Items Only")
        print("open = Edit config Manually")
        print("0 = Exit Edit Mode")
    if viewall is False:
        print("##Group 1##")
        for item in custom_whitelist:
            print(item)
            iox += 1
            if iox == 5:
                group += 1
                iox = 0
                print(f"\n##Group {group}##")
        print("\n############\n[Edit Mode]\n############\n")
        print("add = Add Item")
        print("del = Remove Item")
        print("viewall = Show Default and Custom Items")
        print("open = Edit config Manually")
        print("0 = Exit Edit Mode")


def run():
    viewall = False
    while True:
        system('cls')
        if viewall is True:
            display_whitelist(True)
        if viewall is False:
            display_whitelist(False)
        var = input("\n> ").casefold()
        if var != "0":
            if var == "add":
                print("Adding File")
                while True:
                    user_input = input("Enter File/Folder Name\n0 to Exit\n> ")
                    if user_input == "0":
                        break
                    else:
                        whitelist_add(user_input)
                        break
            elif var == "del":
                print("Deleting File")
                while True:
                    user_input = input("Enter File/Folder Name\n0 to Exit\n> ")
                    if user_input == "0":
                        break
                    else:
                        try:
                            whitelist_del(user_input)
                            break
                        except ValueError:
                            print("Item not in Whitelist")
                            continue
            elif var == "viewall":
                viewall = True
                continue
            elif viewall is True and var == "viewless":
                viewall = False
                continue
            elif var == "open":
                os.startfile(f'{assets}\\whitelist.yaml')
                continue
            else:
                print("Invalid Input")
        else:
            system('cls')
            break
