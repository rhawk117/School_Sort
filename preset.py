import os
from school_sort.School_Sort.main import Input
import sys
import json
import re as regex
from pprint import pprint


class Preset:
    def slct_preset():
        os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
        try:
            print('[*] Fetching Presets... [*]\n')
            options = []
            for _, __, files in os.walk("presets"):
                for file in files:
                    print("\t > " + file)
                    options.append(file)
            slction = Input.get_input(
                '[*] Pick one of the following presets list above [*]', options)
            with open(file='presets\\' + slction, mode='r') as preset:
                print(f'[*] Succesfully Opened Preset [*]')
                return json.load(preset)
        except Exception:
            print('[!] ERROR: Failed to select user preset, please try again [!]')
            sys.exit()

    @staticmethod
    def create_preset_file(preset: dict) -> None:
        # Create File Name
        file_name = ''
        while file_name == '' or not Input.check_file_name(file_name, 'json'):
            file_name = input(
                '[?] Enter the desired file name of the json preset with ".json" at the end: ')

        # Create a dump dictionary data into JSON
        try:
            with open(file=f'presets\\{file_name}', mode='w') as file_preset:
                json.dump(preset, file_preset, indent=4)
        except Exception:
            print(
                f'[!] An error occured while trying to create your JSON preset, pleas try again [!] ')
            sys.exit()

        print('[*] Preset Successfully Created [*]')

    @staticmethod
    def auto_preset_data(dir_path) -> dict:

        # Directory Path Doesn't exist
        if not os.path.exists(dir_path):
            print(f'[!] ERROR: The file path provided does not exist')
            sys.exit()

        # Directory is Empty
        if not any(os.scandir(dir_path)):
            print(
                f"[!] ERROR: The File Path ({dir_path}) provided is empty, cannot create preset")
            sys.exit()

        # Directory has no Sub Directories
        if not any(items.is_dir() for items in os.scandir(dir_path)):
            print(
                f"[!] ERROR: The File Path ({dir_path}) provided did not contain any sub directories, cannot create preset")
            sys.exit()

        data = {}
        for path, subdirs, _ in os.walk(dir_path):
            # Get the depth of the current directory by counting os.sep in path
            depth = path[len(dir_path):].count(os.sep)
        # create keys in nested dictionary with first layer of subdirs (only) with key being the name and value being the path
            if depth == 1:  # First level subdirectories
                numPattern = regex.compile(r'\d+')
                sub_dir_name = os.path.basename(path)
                sub_dir_name = "".join(numPattern.findall(sub_dir_name))
                data[sub_dir_name] = {}
                data[sub_dir_name].update({"DirPath": path})
                data[sub_dir_name].update(
                    {
                        sub[:3]: os.path.join(path, sub) for sub in subdirs
                    }
                )

        print('\n[*] Preset Data Succesfully Generated [*]\n'.center(60))
        pprint(data, indent=6)

        # No Data was created
        if not data:
            print(f"[!] ERROR: Failed to create any presets, try again [!]")
            sys.exit()
        return data

    @staticmethod
    def list_cmds() -> None:
        print('[*] PRESET COMMANDS [*]'.center(60))
        print('\n\t > [auto]: automatically generates a preset')
        print('\n\t > [manual]: uses user input to generate a preset')
