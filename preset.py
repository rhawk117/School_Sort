import os
from common import Input
import sys
import json
import re as regex
from pprint import pprint
from InquirerPy import prompt





# handles all logic related to loading and creating a preset
class Preset:

    # private function that walks through the preset directory
    # sets the avlble_preset field to generate list of user choices\

    def _fetch_presets(self) -> None:
        # change to .py file dir
        os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))


        # program has successfully found presets dir and attempts to walk and find all .json files    
        usr_choices = []
        try:
            # walk presets
            for _, __, files in os.walk("presets"):
                for file in files:
                    if file.endswith(".json"):
                        print("\t > " + file)
                        usr_choices.append(file)
                    
        except:
            print("[!] ERROR: Could not find / walk the presets directory [!]")
            sys.exit()

        # No Presets were found
        if not usr_choices:
            print(
                "[!] ERROR: No presets could be found, cannot perform sorting actions [!]"
            )
            sys.exit()

        self.avlble_preset = usr_choices
     
        
    # private function that generates a menu for the usr to select the desired preset
    def _slct_preset(self):
        try:
            print('[*] Fetching Presets... [*]\n'.center(60))
            self._fetch_presets() # get list of options a usr can select
            preset_menu = prompt(
            [
                {
                    "type": "list",
                    "name": "selected_preset",
                    "message": "[?] Select a preset file:",
                    "choices": self.avlble_preset,
                }
            ]
            )
            self.slcted_preset = preset_menu["selected_preset"]


        except Exception as e:
            print(f'[!] ERROR: Failed to select user preset, please try again [!] -> {e}')
            sys.exit()

    # private function that attempts to open the selected json 
    def _file_slct_hndler(self):
        print(f"[*] Attempting to Open {self.slcted_preset}... [*]".center(60))
        try:
            tmp = {}
            with open(file='presets\\' + self.slcted_preset, mode='r') as preset:
                print(f'[*] Succesfully Opened Preset [*]')
                tmp = json.load(preset)

        except Exception:
            print("[!] ERROR: An error occured while trying to open the preset file, try again [!]")
            sys.exit()

        # if the loaded json is null
        if not tmp:
            print("[!] ERROR: Could not open preset ")
            sys.exit()

        self.loaded_preset = tmp

    
    # public function that uses the private class methods used for handling the logic of loading a preset 
    def load_preset_hndler(self):
        # when load preset in the main menu is selected 
        self._slct_preset() # handles most of the logic we need to perform with selecteding a json preset 
        self._file_slct_hndler()

    # the checks performed to ensure a preset can be created with the supplied directory
    def _auto_preset_check(self, dir_path) -> bool:

        # list of checks performed before the auto_preset_method
        if not os.path.exists(dir_path):
            print(f'[!] ERROR: The file path provided does not exist')
            return False

        # Directory is Empty
        if not any(os.scandir(dir_path)):
            print(
                f"[!] ERROR: The File Path ({dir_path}) provided is empty, cannot create preset")
            return False

        # Directory has no Sub Directories
        if not any(items.is_dir() for items in os.scandir(dir_path)):
            print(
                f"[!] ERROR: The File Path ({dir_path}) provided did not contain any sub directories, cannot create preset")
            return False
        
        return True

    # private function that autonomously creates a preset without user interaction
    def _auto_preset_data(self) -> None:
        # prompt user for directory 

        dir_path = Input.get_path_input(
            "[?] Enter the file path to your course directory: "
        )

        if not self._auto_preset_check(dir_path):
            raise Exception("[!] Cannot Proccess User Request [!]".center(60))
        

        data = {}
        for path, subdirs, _ in os.walk(dir_path):
            # Get the depth of the current directory by counting os.sep in path
            depth = path[len(dir_path):].count(os.sep)

            # create keys in nested dictionary with first layer of subdirs (only) 
            # with key being the name and value being the path
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
        pprint(data, indent = 6)

        # No Data was created
        if not data:
            print(f"[!] ERROR: Failed to create any presets, try again [!]")
            sys.exit()

        self.created_preset = data

    # private function that creates the file after recieving all preset information
    def _create_preset_file(self) -> None:
        # Create File Name from user input
        file_name = ''
        while file_name == '' or not Input.check_file_name(file_name, 'json'):
            file_name = input(
                '[?] Enter the desired file name of the json preset with ".json" at the end: '
            )

        # Create and dump dictionary data into JSON
        try:
            with open(file=f'presets\\{file_name}', mode='w') as file_preset:
                json.dump(self.created_preset, file_preset, indent = 4)

        except Exception:
            print(
                f'[!] An error occured while trying to create your JSON preset, pleas try again [!] ')
            sys.exit()

        print('[*] Preset Successfully Created [*]')
    
    # public function that handles the "Create A Preset Logic"
    def preset_creation_hndler(self):
        self._auto_preset_data()
        self._create_preset_file()


        

    
