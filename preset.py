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
from send2trash import send2trash 
import shutil 
from threading import Thread

# handles all logic related to loading and creating a preset
class Preset:
    # Class Properties
    # avlble_preset => list of all found .json files found in the presets dir
    # slcted_preset => the preset the user has selected from avlble_preset
    # loaded_preset => the json preset that was selected and successfully opened
    # created_preset => the preset that was created by the user 
    # target_files => list of TargetFile Objects that will be moved 
    # prev_paths => a dictionary loaded from usr_paths.json 
    # all_jsons => list of all jsons in presets
    def __init__(self):
        self.slcted_preset = "unset"


    def _fetch_presets(self) -> None:
        
        '''          
             private function that walks through the preset directory
             sets the avlble_preset field to generate list of user choices
        '''

        # change to .py file dir
        os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))


        # program has successfully found presets dir and attempts to walk and find all .json files    
        self.avlble_preset = []
        try:
            for _, __, files in os.walk("presets"):
                for file in files:
                    self._preset_filter(file)
        except:
            print("[!] ERROR: Could not find / walk the presets directory [!]")
            return 
            

        # No Presets were found
        if not self.avlble_preset:
            print(
                """[!] ERROR: No presets could be found in the presets dir, the directory [!]
                   [>] This is either due to the presets directory not existing or having not
                   [>] created a .json preset. 
                """.center(60)
            )
            choices = [
                "[ Create a preset ]", 
                "[ exit program ]"
            ]

            yes_no_menu = prompt(
                [
                    {
                        "type": "list",
                        "name": "usr_opt",
                        "message": "[ Would you like to create one ]",
                        "choices": choices,
                    }
                ]
            )
            choice = yes_no_menu["usr_opt"]
            if choice == choices[0]:
                self.usr_dir_input()
                self.preset_creation()

            elif choice == choice[1]:
                print("[i] Exiting Program [i]".center(60))
                sys.exit()

    # the logic for filtering files in presets dir by extension and passes usr_paths.json
    def _preset_filter(self, file):
        if file.endswith(".json"): 
            # The user should not be able to select usr_paths
            if file != "usr_paths.json":
                self.avlble_preset.append(file)

     
    # private function that generates a menu for the usr to select the desired preset
    def _slct_preset(self) -> None:
        try:
            print('[i] Fetching Presets... [i]\n'.center(60))
            self._fetch_presets() # get list of options a usr can select
            self._check_presets() # Check if any file paths in all presets are invalid before loading or displaying them
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


    # private function that checks all of the paths of nested dictionaries in avlble_preset
    def _check_presets(self) -> None:
        for files in self.avlble_preset:
            print(f'[i] Checking the {files} for invalid file paths...')
            path = os.path.join("presets", files)
            self._check_preset_paths(path)
        

    def _check_preset_paths(self, file_path):
        # checking each of the paths in a preset for paths that don't exist
        tmp = {}
        with open(file_path, mode='r') as tmp_preset:
            tmp = json.load(tmp_preset)

        file_name = os.path.basename(file_path)

        # .json preset opened is empty
        if not tmp:
            self._invalid_preset_menu(file_path)
        
        for dicts in tmp.values():
            if self._check_course_path(dicts):
                self._invalid_preset_menu(file_path)
                self.avlble_preset.remove(file_name)

    # iterates through the values of in the dictionary param and checks if the values are invalid file paths
    def _check_course_path(self, course_data:dict) -> bool:
        '''
            checks if a dictionary contains invalid course paths
        '''
        bad_paths = False
        for paths in course_data.values():
            if not os.path.exists(paths):
                print(f"[!] {paths} does not exist [!]".center(60))
                bad_paths = True

        return bad_paths

    # Menu that appears upon discovering an invalid file path in a preset
    def _invalid_preset_menu(self, file_path) -> None:
        
        '''
            While checking the .json file paths if a .json file
            has a value in a nested dictionary with a file path that
            doesn't exist it asks the user if they'd like to delete it 
            to help imporve program reliability
        '''

        file_name = os.path.basename(file_path)
        warning = f"""
            [!] WARNING: while validating the path of your presets {file_name}, 
            the script found a file path that does not exist or discovered the preset was empty
            \n[ ? Would you like to remove it ?]
        """
        dir_menu = prompt(
                [
                    {
                        "type": "list",
                        "name": "usr_opt",
                        "message": warning,
                        "choices": ["[  << Remove Invalid Preset >>  ]", "[ <x> Leave invalid Preset <x> ]"],
                    }
                ]
            )
        usr_choice = dir_menu["usr_opt"]
        if usr_choice == "[ Remove Preset ]":
            print(f"[i] Sending {file_name} to your recycling bin to recover in case of an error from the script... [i]".center(60))
            send2trash(file_path)
            return 
        
        else:
            print(f'[i] Leaving invalid preset behind.. [i]'.center(60))
            
                
    # private function that attempts to open the selected json 
    def _file_slct_hndler(self) -> bool:

        '''
            Upon successfully selecting a preset this private function
            sets the loaded_preset property to the value of the json preset
            selected, returning true if successful
        '''

        print(f"[i] Attempting to Open {self.slcted_preset}... [i]".center(60))
        try:
            tmp = {}
            with open(file='presets\\' + self.slcted_preset, mode='r') as preset:
                print(f'[i] Succesfully Opened Preset [i]'.center(60))
                tmp = json.load(preset)

        except Exception:
            print("[!] ERROR: An error occured while trying to open the preset file, try again [!]")
            return False

        # if the loaded json is null
        if not tmp:
            print("[!] ERROR: Could not use preset due to it being empty [!]")
            return False

        # set value to class attribute to allow us to chain multiple functions together
        self.loaded_preset = tmp
        return True

    # attempts to load previously inputed file paths from the user
    def check_prev_paths(self) -> bool:
        if not os.path.exists("presets\\usr_paths.json"):
            print(
                '[!] NOTE: The usr_paths.json file in presets was not found, user input will be required for path fields [!]'.center(60)
            )
            return False
        
        try:

            # Attempt to load usr_paths.json
            tmp = {}
            with open("presets\\usr_paths.json", mode='r') as usr_data:
                tmp = json.load(usr_data)
            
            # usr_paths.json is empty
            if not tmp:
                print(
                    "[i] No previous file paths were found in usr_paths.json, user input required for path fields[i]".center(60))
                return False
            
            # all checks passed, user can select a previously used file path
            self.prev_paths = tmp
            return True
        
        except Exception as ex:
            print(
                f'''
                [!] ERROR: An error occured while trying load previous user file paths likely due to the program running for the first time 
                [>] User input will now be required for path fields, error details below [!]
                '''.center(60)
            )
            print(f'[ << i >> ] {ex}')
            return False
        

    
    def save_path_input(self, path_input) -> None:

        '''
            any time we recieve a file path from the user
            we can save it to usr_paths.json, so next time they have to input one
            we can create a previous paths menu for easy re-use 
        '''

        try:
            # Check if the file exists and is not empty
            if os.path.exists("presets\\usr_paths.json") and os.path.getsize("presets\\usr_paths.json") > 0:
                with open("presets\\usr_paths.json", 'r') as file:
                    data = json.load(file)
            else:
                # the usr_paths.json is empty
                data = {}
            
            key_check = os.path.basename(path_input)
            if key_check in data:
                print("[i] The inputted file path already exists in usr_paths.json, not saving input [i]")
                return 
            
            new_data = { key_check : path_input }
            
            # Update data & save into class property
            data.update(new_data)
            self.prev_paths = data

            # Write the new data back to the file
            with open("presets\\usr_paths.json", 'w') as file:
                json.dump(self.prev_paths, file, indent = 4)

        except Exception as ex:
            print("[!] ERROR: An error occured while trying to save the file path inputed, details on next line[!]")
            print(f'{ex}')

            
    # For manual user directory input 
    def usr_dir_input(self) -> None:
        prompt = "[ Enter the path of the directory containing the course files you'd like to move or create a preset from ]"
        tmp = Input.get_path_input(prompt)
        self.usr_slct_dir = tmp
        self.save_path_input(tmp)

    # Optional Menu that displays previously entered directories by the user in a menu 
    def prev_dirs(self):
        '''
            function attempts to use the keys from usr_paths.json dict
            which when selected in the menu,
            returns the corresponding 
            inputs which are just the basenames of directory (i.e dir name) 
        '''

        # this check should almost always be redundant but better safe than sorry
        if self.prev_dirs:
            # generate file path menu 
            options = list(self.prev_paths.keys())
            options.append("[ Input a New Path Instead ]")
            dir_menu = prompt(
                [
                    {
                        "type": "list",
                        "name": "select_path",
                        "message": "[?] Select a preset file or directory to sort:",
                        "choices": options,
                    }
                ]
            )
            file_path_key = dir_menu["select_path"]

            # The last index of options will always be "[ Input a New Path Instead ]" since we appended it 
            # if block has to run first or an error will occur since it's not a file path
            if file_path_key == options[len(options) - 1]:
                # the last index of options is the option to enter a new file path
                self.usr_dir_input()
                return  

            elif file_path_key not in self.prev_paths:
                print(
                    "[!] Due to an error with the path keys you must type the file path to proceed, sorry lol [!]"
                )
                self.usr_dir_input()
                return 
            
            else:           
                try:

                    self.usr_slct_dir = self.prev_paths[file_path_key]
                    print(
                        f"[i] User input successfully recieved, attempting to sort {self.usr_slct_dir} [i]".center(60)
                    )
                except Exception as ex:
                    print("[!] An error occured while trying to use the file path provided, please enter it manually")
                    self.usr_dir_input()
                # method end
        else:
            print("[!] Due to an error trying to load your previous paths, user input is required ")
            self.usr_dir_input()

        

    # using base name and file name in the usr selected directory function performs a series of
    # checks and attempts to parse it using the loaded preset returning a TargetFile object
    def _process_file(self, root, file):
        # _is_movable checks if the file contains underscores, then the length of the split string
        if not self._is_movable(file):
            print(f'> Skipped {file}')
            return None

        # fetch the course number which should go first and then the abreviated directory it goes to
        course_number, dir_abbreviation = file.split('_')[:2]

        # check if the CRN is a key in the preset, then if dictionary in the
        # CRN key contains the abreviated directory key in the file name
        if course_number not in self.loaded_preset or dir_abbreviation not in self.loaded_preset[course_number]:
            print(f' > Skipped {file}, {dir_abbreviation} not in keys'.center(60))
            return None

        # access the key of destination path in the nested dictionary
        destination = self.loaded_preset[course_number][dir_abbreviation]
        if not os.path.exists(destination):
            raise Exception("[!] CRITICAL ERROR: The destination file path in the json preset does not exist [!]\n" +
                            "[!] The preset loaded should not be used again and needs to be reconfigured [!]"
                            )

        source = os.path.abspath(os.path.join(root, file))
        return TargetFile(destination, source)

    # checks param for underscores and checks if it can be parsed
    def _is_movable(self, file):
        # movable files contain underscores, they start with the CRN,
        # then abbreviated path & then name of file, so the length should be > 3
        return '_' in file and file[0:3].isdigit() and len(file.split('_')) >= 3
        
    # core logic of find movable files, puts the pieces together
    def _comb_dir(self):
        if not os.path.exists(self.usr_slct_dir):
            print("[i] The user selected file path does not exist, perhaps a previously saved path in usr_paths.json no longer exists [i]")

        # .json preset is empty 
        if not self.loaded_preset:
            print(
                "[!] ERROR: Cannot use a null preset, try again with a valid preset [!]")
            return False

        try:
            # fetch a list of movable files, _process_file() has a series of checks to 
            # skip unparsable files 
            movable = [self._process_file(root, file) 
                       for root, _, files in os.walk(self.usr_slct_dir) 
                       for file in files
                    ]
            # check for possibly void items in the list we generated 
            self.target_files = [file for file in movable if file]
            if not self.target_files:
                print(
                    "[!] ERROR: No files were found or could be parsed [!]".center(60)
                )
                return False
            # all checks passed
            return True 

        except Exception as ex:
            print(
                f'[!] ERROR: Failed to fetch files from ({self.usr_slct_dir}), cannot sort files error details below [!]\n'
            )
            print(ex)
            return False

    # Displays TargetFiles ToString method to user before moving them
    def _display_move_files(self):
        if not self.target_files:
            print("[!] No Files are in the target_files list, cannot display them to the console [!]")
            return 
        
        # Display TargetFile Objects in the Console to User to Confirm Moving Action
        for targets in self.target_files:
            print(targets)
        
        options = ["[  YES  ]", "[ NO ]"]
        dir_menu = prompt(
            [
                {
                    "type": "list",
                    "name": "usr_opt",
                    "message": "[ ? Proceed with File Sort ? ]",
                    "choices": ["[  YES  ]", "[ NO ]"],
                }
            ]
        )
        choice = dir_menu["usr_opt"]
        if choice == options[0]:
            self._move_files()

        elif choice == options[1]:
            print("[ Exiting Program ]".center(60))
            sys.exit()
    

    def _move_files(self) -> None:
        
        '''
            upon the creation of the target_files attribute,
            this method will be called to start the threads need
            before joining them 
        '''

        app_threads = []
        for files_moved in self.target_files:
            src, dst = files_moved.source, files_moved.destination
            fileThread = Thread(
                target = self._safe_move,
                args=(src, dst)
            )
            app_threads.append(fileThread)
            fileThread.start()

        # Run created threads to sort files for efficency
        for threads in app_threads:
            threads.join()
        
        input('*** PRESS ENTER TO CONTINUE ***'.center(60))
    

    def _safe_move(self, src, dst):
        try:
            shutil.move(src, dst)
            print(f"\n[ Moved => {src} to => {dst} ]\n".center(60))
        except Exception as ex:
            print(
                f""" [ Cannot Move => {src}] to => file_obj.destination due to an Exception ] \n
                     \t\t[ <<!>> Please Try Again <<!>> ] \n
                """.center(60)
            )
            print("[ Exception Information ]" + f"\n{ex}\n")



    # public function that uses the private class methods used for handling the logic of loading a preset 
    def load_preset_hndler(self) -> None:
        # when load preset in the main menu is selected 
        self._slct_preset() # handles most of the logic we need to perform with selecteding a json preset 
        if not self._file_slct_hndler():
            self._slct_preset()

    # public function that incorporates the logic of the previous private ones in _comb_dir()
    def fetch_files(self):
        if not self._comb_dir():
            print(f"[!] An occured occured while combing {self.usr_slct_dir}, cannot move files please try again")

        else:
            self._display_move_files()

    # the checks performed to ensure a preset can be created with the supplied directory
    def _auto_preset_checks(self, dir_path) -> bool:
        
        '''
            list of checks to ensure a preset can be made 
            before performing any action, true if possible
            false otherwise
        '''

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
        
        '''
            autonomously creates json preset data after 
            the user selects a directory
        '''

        # See if the directory entered by the user or selected in the menu can be used 
        if not self._auto_preset_checks(self.usr_slct_dir):
            print("""
                  [!] Cannot Proccess User Request, invalid directory input provided [!]
                  """
        )
        self.loaded_preset = {}
        for path, subdirs, _ in os.walk(self.usr_slct_dir):
            # Get the depth of the current directory by counting os.sep in path
            depth = path[len(self.usr_slct_dir):].count(os.sep)

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

                    elif sub == "Assignments" or sub == "assignments":
                        sub_key = 'Asn' # so the abreviation isn't 'ass' lol

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
        
        '''
            upon recieving a file name from the user 
            we create a .json preset with it saved to
            the presets dir
        '''

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
                f'[!] An error occured while trying to create your JSON preset, pleas try again [!] '
            )
            sys.exit()

        print('[*] Preset Successfully Created [*]'.center(60))
    
    
    def preset_check(self) -> bool:
        if self.check_prev_paths():
            return False
        else:
            self.usr_dir_input()
            self.preset_creation()
            return True

    def preset_creation(self):
        
        '''
            upon recieving directory input
            this method uses auto_preset_data
            & create_preset file to perform all
            actions required for preset creation
        '''

        self._auto_preset_data()
        self._create_preset_file()

    
            

# representation of the source and destination of files that will be moved
@dataclass
class TargetFile:
   destination: str
   source: str
   # ToString Method to display all of the files that are about to be moved to the user
   def __str__(self) -> str:
       return f"[ File => {os.path.basename(self.source)} is being moved to => {self.destination} ]\n".center(60)
        

    
