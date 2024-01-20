import os
from pathlib import Path
import shutil
import json
import re as regex
from pprint import pprint 
import sys 
import keyboard
import time
from school_sort.School_Sort.Menu import Menu


    

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
            slction = Input.get_input('[*] Pick one of the following presets list above [*]', options)
            with open(file='presets\\' + slction, mode = 'r') as preset:
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
            file_name = input('[?] Enter the desired file name of the json preset with ".json" at the end: ')

        # Create a dump dictionary data into JSON
        try:
            with open(file=f'presets\\{file_name}', mode='w') as file_preset:
                json.dump(preset, file_preset, indent=4)
        except Exception:
            print(f'[!] An error occured while trying to create your JSON preset, pleas try again [!] ')
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
            print(f"[!] ERROR: The File Path ({dir_path}) provided is empty, cannot create preset")
            sys.exit()

        # Directory has no Sub Directories
        if not any(items.is_dir() for items in os.scandir(dir_path)):
            print(f"[!] ERROR: The File Path ({dir_path}) provided did not contain any sub directories, cannot create preset")
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

                
        
        
# Input Validation methods 
@staticmethod
class Input:

    def get_path_input(prompt:str):
        file_path = input('[?] Enter the courses associated file path: ').strip('"') # remove double quotes 
        try:
            parsed_path = os.path.normpath(file_path.replace("\\", "\\\\"))
            if os.path.exists(parsed_path) and os.path.isdir(parsed_path):
                return parsed_path
            print('[!] USER INPUT INVALID [!]\n' + f'> The File Path provided ({parsed_path}) does not exist!')
        except ValueError:
            print('[!] Could not normalize file path provided, please re-enter the key and file path for this entry [!]')

        return Input.get_path_input(prompt) # recursive call only executed if exception occurs or if the path provided is invalid


    def get_input(prompt: str, options: list) -> str:
        usr_input = input('[?] ' + prompt)
        if usr_input.lower() in options:
            return usr_input.lower()
        print(f'[!] User Input Invalid [!]\n > Options: ' + ' , '.join(options))
        return Input.get_input(prompt, options)


    def check_file_name(file_name: str, extension: str) -> bool:
        '''
        checks the file name inputed by user to see if it's a 
        valid file name returning true if it is, false otherwise
        '''
        if file_name == '':
            return False
        
        prefix = '[!] Invalid File Name [!]\n'
        expression = regex.compile(r"^[A-Za-z0-9_.-]*$")
        if not regex.match(expression, file_name):
            print(prefix + 'Cannot create a file with invalid characters')
            return False

        # Check for valid extension
        if not file_name.endswith('.' + extension):
            print(prefix + f'Files must end with the .{extension} extension')
            return False

        # Check for maximum length
        if len(file_name) > 25:
            print(prefix + 'File names should be less than 25 characters')
            return False

        # Check for reserved names
        if file_name.lower() in ["con", "prn", "nul"]:
            print(prefix + 'File names cannot be reserved')
            return False

        # Check in Presets folder if file with same name exists
        if os.path.isfile('output\\' + file_name):
            print(prefix + 'A file with the same name already exist!')
            return False

        return True  # file name passes all checks, return True



def main_menu_handler(selectedIndex:int):
    if selectedIndex == 1:
        path = Input.get_path_input(
            '[?] Enter the file path containing your course directories: ')
        new_preset = Preset.auto_preset_data(path)
        Preset.create_preset_file(new_preset)

    elif selectedIndex == 0:
        data = Preset.slct_preset()
        usrDir = Input.get_path_input(
            '[?] Specify the file path of the directory of your course files you want to move: ')
    



def header() -> None:
    print('*'*60)
    print(r"""
   __         _                 _                  _  __  
  / /___  ___| |__   ___   ___ | |  ___  ___  _ __| |_\ \ 
 / // __|/ __| '_ \ / _ \ / _ \| | / __|/ _ \| '__| __|\ \
 \ \\__ \ (__| | | | (_) | (_) | | \__ \ (_) | |  | |_ / /
  \_\___/\___|_| |_|\___/ \___/|_| |___/\___/|_|   \__/_/ 
                                                          """.center(60))
    print('** created by: rhawk117 **\n'.center(60))
    print('\t[*] Type > "preset" to create a new json preset')
    print('\t[*] Type > "sort" to move files from a json preset')
    print('*'*60)

def upon_start() -> None:
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  # change CWD to program's dir
    header()

def main() -> None:
    upon_start()
    # 
    MainMenu = Menu("Select One of the Following",["Load Preset", "Create Preset", "Help"])
    MainMenu.run_menu()

    

        

        


    


if __name__ == '__main__':
    main()
