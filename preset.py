# *** created by rhawk117 ***
# preset.py -- the core logic of preset creation & loading presets
import os
from common import Input
import sys
import json
import re as regex
from pprint import pprint
from InquirerPy import prompt
from dataclasses import dataclass


# handles all logic related to loading and creating a preset
class Preset:
    # Class Properties
    # avlble_preset => list of all found .json files found in the presets dir
    # slcted_preset => the preset the user has selected from avlble_preset
    # loaded_preset => the json preset that was selected and successfully opened
    # created_preset => the preset that was created by the user 
    # target_files => list of TargetFile Objects that will be moved 


    # private function that walks through the preset directory
    # sets the avlble_preset field to generate list of user choices
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
    def _slct_preset(self) -> None:
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
                print(f'[i] Succesfully Opened Preset [i]'.center(60))
                tmp = json.load(preset)

        except Exception:
            print("[!] ERROR: An error occured while trying to open the preset file, try again [!]")
            sys.exit()

        # if the loaded json is null
        if not tmp:
            print("[!] ERROR: Could not open preset ")
            sys.exit()

        # set value to class attribute to allow us to chain multiple functions together
        self.loaded_preset = tmp

    def comb_dir(self, dir_path):
        if not self.loaded_preset:
            print(
                "[!] ERROR: Cannot use a null preset, try again with a valid preset [!]"
            )
            return

        movable = []  # find a list of movable files
        try:
            for root, _, files in os.walk(dir_path):
                for file in files:
                    # All sorted files should contain an underscore and the first 4 digits should be the course number
                    if '_' in file and file[0:3].isdigit():
                        tmp = file.split('_')
                        # when the length is less than 3 that means either there isn't a crn, abreviated output dir or file name
                        # tmp[0] is the course number which should be a key in the dictionary
                        if not tmp or len(tmp) < 3 or tmp[0] not in self.loaded_preset.keys():
                            print(f'> Skipped {file}')
                            continue

                        crse_data = self.loaded_preset.get(tmp[0])
                        # The 2nd index of tmp is the abreviated key for the output directory, check to see if it's in the file
                        if tmp[1] not in crse_data.keys():
                            print(f' > Skipped {file}, {tmp[1]} not in keys')
                            continue

                        # tmp[1] is the abreviated destination directory which we use to access it's value, the destination path
                        destination = crse_data.get(tmp[1])
                        source = os.path.abspath(
                            os.path.join(root, file)
                        )
                        if not os.path.exists(destination):
                            raise Exception("[!] CRITICAL ERROR: The destination file path in the json preset does not exist [!]\n" +
                                            "[!] The preset loaded should not be used again and needs to be reconfigured [!]"
                                            )

                        # Create our Data Class for the file we want to move with all the information we need
                        tmp = TargetFile(destination, source)
                        movable.append(tmp)
            if not movable:
                print(
                    f"[!] ERROR: No files were found or could be parsed [!]".center(60))
            # All checks have been passed
            self.target_files = movable
        
        except Exception as ex:
            print(
                f'[!] ERROR: Failed to fecth files from ({dir_path}), cannot sort files [!]')
            print(ex)
            return []
    

    

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
        

        self.loaded_preset = {}
        for path, subdirs, _ in os.walk(dir_path):
            # Get the depth of the current directory by counting os.sep in path
            depth = path[len(dir_path):].count(os.sep)

            # create keys in nested dictionary with first layer of subdirs (only) 
            # with key being the name and value being the path
            if depth == 1:  # First level of subdirectories
                numPattern = regex.compile(r'\d+')
                sub_dir_name = os.path.basename(path)
                sub_dir_name = "".join(numPattern.findall(sub_dir_name))
                sub_dir_data = { "Src": path }

                # Iterate over each subdirectory and add to sub_dir_data
                for sub in subdirs:
                    sub = sub.strip()

                    if sub == 'Homework' or sub == 'homework':
                        sub_key = 'HW'

                    elif sub == 'Notes' or sub == 'notes':
                        sub_key = 'Notes'

                    elif len(sub) < 3:
                        sub_key = sub
                    
                    else:
                        sub_key = sub[:3]

                    sub_value = os.path.join(path, sub) # save the path to the directory 
                    sub_dir_data[sub_key] = sub_value

                # Add subdirectory self.loaded_preset to main self.loaded_preset dictionary
                self.loaded_preset[sub_dir_name] = sub_dir_data


        print('\n[*] Preset Data Succesfully Generated [*]\n'.center(60))
        pprint(self.loaded_preset, indent = 6)

        # No Data was created
        if not self.loaded_preset:
            print(f"[!] ERROR: Failed to create any presets, try again [!]")
            sys.exit()

        self.created_preset = self.loaded_preset

    # private function that creates the file after recieving all preset information
    def _create_preset_file(self) -> None:

        # Prompt usr for a file name for the new preset created
        file_name = ''
        while file_name == '' or not Input.check_file_name(file_name, 'json'):
            file_name = input(
                '[?] Enter the desired file name of the json preset with ".json" at the end: '
            )

        # Create and dump dictionary self.loaded_preset into the newly named and created json
        try:
            with open(file=f'presets\\{file_name}', mode='w') as file_preset:
                json.dump(self.created_preset, file_preset, indent = 4)

        except Exception:
            print(
                f'[!] An error occured while trying to create your JSON preset, pleas try again [!] ')
            sys.exit()

        print('[*] Preset Successfully Created [*]'.center(60))
    
    # public function that handles the "Create A Preset Logic"
    def preset_creation_hndler(self):
        self._auto_preset_data()
        self._create_preset_file()

        
            

# representation of the source and destination of files that will be moved
@dataclass
class TargetFile:
   destination: str
   source: str
   # ToString Method to display all of the files that are about to be moved to the user
   def __str__(self) -> str:
       return f"[ File => {os.path.basename(self.source)} is being moved to => {self.destination} ]".center(60)
        

    
