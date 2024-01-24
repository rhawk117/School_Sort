# *** created by rhawk117 ***
# main.py -- puts the pieces together
import os
import sys 
from menu import Menu
from preset import Preset
import time 
from pprint import pprint 
from InquirerPy import prompt
import json

# implements the logic & classes of program
class MainMenu:
    # main menu title text
    @staticmethod
    def header() -> str:
        main_menu_txt = "=" * 60 + "\n"
        main_menu_txt += r"""
            __         _                 _                  _  __  
            / /___  ___| |__   ___   ___ | |  ___  ___  _ __| |_\ \ 
            / // __|/ __| '_ \ / _ \ / _ \| | / __|/ _ \| '__| __|\ \
            \ \\__ \ (__| | | | (_) | (_) | | \__ \ (_) | |  | |_ / /
            \_\___/\___|_| |_|\___/ \___/|_| |___/\___/|_|   \__/_/ 
                    
                    *** created by rhawk117 ***                                               
        """
        main_menu_txt += "=" * 60
        return main_menu_txt

    # handles the logic and checks performed whenever the program is run 
    @staticmethod
    def upon_start() -> None:

        '''
        performs a series of checks and set up & can 
        detect whenever program is run for the first time,
        if it is the help demonstration will display
        '''

        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        os.chdir(path)  # change CWD to program's dir

        # check if presets directory exists, if not make it for the user
        if not os.path.exists("presets"):
            print(('*' * 60) + '\n\n')
            os.mkdir("presets")
            print("""[!] NOTE: The presets directory could not be found likely due to the program being run for the first time,
            it has been created for future use. In order for the program to function 
            properly do not alter or modify this directory, temporarily pausing the program for 5 seconds [!] 
            """)
            print(('*' * 60) + '\n\n')
            # pause program for user to read
            print(']\n [i] temporarily pausing the program for 5 seconds... [i] \n')
            time.sleep(5)
            MainMenu.help_demonstration()

                   
        if not os.path.exists("presets\\usr_paths.json"):
            with open("presets\\usr_paths.json", mode='w') as _:
                pass
            print("[!] NOTE: To improve user experience all inputed directories will be saved in usr_paths.json for future reference [!]")
            print("[i] This allows you to easily revisit directories that contain course files\n" +
                   "you want to move without the need of user input, temporarily pausing program [i]"
            )
            time.sleep(3)
            print(('*' * 60) + '\n\n')
            input('[*] Press "Enter" to continue [*]\n'.center(60))

    @staticmethod
    def help_demonstration() -> None:

        '''
        displays the help demonstration, always runs the first time a program runs 
        and displays when 'help' is selected in main menu
        '''

        print('[i] When the Main Menu appears... [i]'.center(60))
        time.sleep(2)

        print('[>] Select << "Create a Preset" >> to create a preset file the program can use \n\n')
        time.sleep(4)

        print('\n[>] Then you will be asked to input the directory path to your couse directories or other desired sorted directory.\n\n')
        time.sleep(4)

        print('\n[>] From there the program will make a .json file automatically that looks like this \n\n')
        time.sleep(2)

        exmple_preset = {
            "3320": {
                "Src": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\AIST-3320",
                "HW": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\AIST-3320\\Homework",
                "Lec": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\AIST-3320\\Lecture Slides",
                "Notes": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\AIST-3320\\Notes",
                "Syl": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\AIST-3320\\Syllabus"
            },
            "3400": {
                "Src": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CSCI3400",
                "HW": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CSCI3400\\Homework"
            },
            "3100": {
                "Src": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CYBR-3100",
                "Lec": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CYBR-3100\\Lecture Slides",
                "M00": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CYBR-3100\\M00 Course Schedule.html",
                "Notes": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CYBR-3100\\Notes",
                "SAN": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CYBR-3100\\SANS_Cheat_Sheet",
                "Syl": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\CYBR-3100\\Syllabus"
            },
            "2650": {
                "Src": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\MINF-2650",
                "Ass": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\MINF-2650\\Assignments",
                "Syl": "C:\\Users\\Beast\\Desktop\\School\\Spring24\\MINF-2650\\Syllabus"
            }
        }
        pprint(exmple_preset, indent = 6)
        time.sleep(4)

        print(('*' * 60) + '\n\n')

        print('[>] After creating this preset, you will be able to autonomously sort files\n')
        print('[>] with the following naming conventions, lets use CSCI-3400  or "3400" in our example preset.\n')
        time.sleep(4)

        pprint(exmple_preset["3400"], indent=6)

        print('\n[>] Example #1: If I wanted to move a file into the Homework directory, after downloading I would name it..\n')
        time.sleep(4)
        print(' << 3400_HW_Homework1 >>'.center(60))
        print('[i] Naming a file this would move the file to -> C:\\Users\\Beast\\Desktop\\School\\Spring24\\CSCI3400\\Homework')
        time.sleep(4)

        print('[i] Example #2: Any course key or course number (3400 in example above) in our preset has ')
        print('[i] Has a key titled Src short for source, so if I wanted to move a file into the directory itself I would name it..\n')
        time.sleep(4)

        print('<< 3400_Src_Syllabus.pdf >>'.center(60))
        print('[i] Naming a file this would move the file to -> C:\\Users\\Beast\\Desktop\\School\\Spring24\\CSCI3400')
        time.sleep(4)

        print('\n[i] If you ever want to view this demonstration again select the [ Help ] option in the main menu')
        print('\n[i] This will relay this demonstration for you any time you launch the program.')


        time.sleep(3)
        print(('*' * 60) + '\n\n')
        input('[*] Press "Enter" to continue [*]\n'.center(60))

    # When the user selects 'Load a Preset'
    @staticmethod
    def handle_presetLoad() -> None:
        load_preset = Preset()
        # this handles selecting a previous generated preset 
        load_preset.load_preset_hndler()

        print(f"[ Please enter the directory you would like to sort course files in]")
        if not load_preset.check_prev_paths():
            load_preset.usr_dir_input()

        else:
            MainMenu.path_menu(load_preset)

        load_preset.fetch_files()
        # At this point all logic has been performed or an Exception has been thrown 
        finalMenu = Menu("[ Return to Main Menu to use Preset or Exit Program ]")
        finalMenu.add_options(
            [ "[ Go To Main Menu ]", "[ Exit Program ]" ]
        )
        finalMenu.add_handler(1, MainMenu.run_main_menu())
        finalMenu.add_handler(2, MainMenu.handle_exit())

        finalMenu.display()


    @staticmethod
    def path_menu(preset_obj):
        pathMenu = Menu("[ Select a previously used file path ]")
        pathMenu.add_options([
            "[ Previous File Paths ]",
            "[ Input new File Path ]"
            ]
        )
        pathMenu.add_handler(1, preset_obj.prev_dirs)
        pathMenu.add_handler(2, preset_obj.usr_dir_input)
        pathMenu.display()

    # When a user selects 'Create a Preset'
    @staticmethod
    def handle_createPreset() -> None:
        create_preset = Preset()
        if not create_preset.preset_check():
            MainMenu.path_menu(create_preset)
            create_preset.preset_creation()


            # Upon the creation of a preset, we ask the user if they want to return to the main menu so 
            # they can use it, or exit the Program, usrMenu below handles this
            usrMenu = Menu("[ Return to Main Menu to use Preset or Exit Program ]")
            usrMenu.add_options([
                "[ Go Back ]", "[ Exit Program ]"
            ])
            usrMenu.add_handler(1, MainMenu.run_main_menu)
            usrMenu.add_handler(2, MainMenu.handle_exit)
            usrMenu.display()


    # When a usr selects 'help'
    @staticmethod
    def handle_help() -> None:
        
        '''
            displays a demonstration of how name and sort files 
            with program, always runs at least once
        '''

        helpMenu = Menu(
            "[ ? Would you like to load a preset to check the naming conventions or display the program tutorial ? ]"
        )
        helpMenu.add_options([
            "[ Check Preset Naming Conventions ]", "[ View Program Tutorial ]"
        ])
        helpMenu.add_handler(1, MainMenu.hndle_preset_name)
        helpMenu.add_handler(2, MainMenu.hndle_tutorial)


    def hndle_preset_name():
        
        '''
            We need to find the user created presets to display
            the appropriate naming conventions to them, after we do
            that we call the attempt_preset_load func which upon
            successfully loading the preset, will display the naming
            conventions to the user 
        '''

        print("[i] Attempting to fetch user created presets... [i]")
        usr_options = MainMenu.attempt_preset_fetch()
        if not usr_options:
            print("[i] No program presets were found, please create one before selecting this option.. [i]".center(60))
            MainMenu.run_main_menu()
        else:
            slcted_preset = MainMenu.preset_menu(usr_options)
            MainMenu.attempt_preset_load(slcted_preset)

    def attempt_preset_load(preset):
        try:
            loaded_preset = {}
            with open(file = f'presets\\{preset}', mode = 'r') as config:
                loaded_preset = json.load(config)
        except Exception as ex:
            print(f"[!] An error occured while trying load {preset}... [!]".center(60))

        if not loaded_preset:
            print("[i] The preset you selected was empty, please try again with a valid one [i]".center(60))
            print('\n*** [i] Returning to Main Menu... [i] ***\n')
            MainMenu.run_main_menu()
            return
        else:
            print(f'[i] Successfully loaded preset, now displaying naming conventions for {preset}.. [i]'.center(60))
            MainMenu.show_preset_conventions(loaded_preset)
            MainMenu.run_main_menu()
    
    def show_preset_conventions(loaded_preset):
        print('[i] The naming convention requires you first specify the course number (e.g 3400) in the file name [i]')
        time.sleep(3)
        print(f'[i] Then seperated by an underscore, specify the abreviated corresponding folder. [i]')
        time.sleep(3)
        print('[i] Generally speaking, most abreviated subfolders are the first 3 characters of the folder name [i]')
        time.sleep(3)
        print(f'[i] However, the program has some generic abreviations for common directory names so always check your preset before naming a file [i]')
        time.sleep(3)
        print('[i] This is all of the data created by the program in your preset file you selected for this demonstration [i]')
        pprint(loaded_preset, indent = 6)
        time.sleep(5)
        for crns, dicts in loaded_preset:
            print(f'[i] For the course with the number {crns}... [i]'.center(60))
            time.sleep(4)
            print('[i] The naming conventions are based on the keys in the dictionary below which will each be explained below [i]')
            pprint(loaded_preset[crns], indent = 4)
            time.sleep(4)

            for key_abrv, paths in loaded_preset[crns]:
                print(f'[i] If I wanted to move a file to {crns} {os.path.basename(paths)} directory... [i]')
                time.sleep(4)
                print(f'\n [i] I would name the file => ("{crns}_{key_abrv}_File") \n')
                time.sleep(4)
                print(f'[i] A file with this name when loading this preset be moved to => {paths} [i]')
                time.sleep(4)


            print('[i] Lets move onto the next course stored in the dictionary. [i]')
            input('*** << Press "Enter" To Continue ***'.center(60))
        print('*' * 60 + '\n\n')
        input('*** Demonstration Complete Press Enter to Return to the main menu ***'.center(60))







    def preset_menu(options:list):
        
        '''
            When the user wants to view the naming conventions for 
            a given preset in the help menu this menu will then appear
            we return the choice which is the file name of a preset
            which we can open and parse appropriately  
        '''

        presetMenu = prompt(
                [
                    {
                        "type": "list",
                        "name": "usr_opt",
                        "message": "[ Would you like to create one ]",
                        "choices": options,
                    }
                ]
            )
        choice = presetMenu["usr_opt"]
        return choice 
    
        


    def attempt_preset_fetch() -> list:
        try:
            for _, __, files in os.walk("presets"):
                presets = [ file 
                            for file in files if file.endswith(".json") 
                            and file != "usr_paths.json"
                ]
            return presets
        except Exception:
            print("[!] An error occured while fetching program preset [!]".center(60))
            MainMenu.run_main_menu()
            
        
        

        

    
        

    def hndle_tutorial() -> None:
        
        '''
            When the user in the help menu selects "View Program Tutorial"
        '''

        print('*'*60+'\n\n')
        print('[*] Displaying program tutorial.. [*]'.center(60))
        MainMenu.help_demonstration()
        print('*'*60+'\n\n')
        MainMenu.run_main_menu()



    # When a usr selects 'Exit'
    @staticmethod
    def handle_exit() -> None:
        
        '''
        when 'Exit' is selected
        '''

        print("\n[*] Exiting Program [*]".center(60))
        sys.exit()

    # Constructs and runs the main menu of program
    @staticmethod
    def run_main_menu() -> None:
        '''
        Starts the program and runs the main menu and applies
        the appropriate handlers to each option
        '''
        MainMenu.upon_start()
        # Instantiate and create the Menu object
        mainMenu = Menu(f"{MainMenu.header()}\n" + "[ Select one of the following options listed below ]")

        # Create the menu options and supply each menu option with the correct handler
        mainMenu.add_options([
            "[ Load a Preset ]", "[ Create a Preset ]",
            "[ Help ]", "[ Exit ]"]
        )
        event_handlers = [
            (1, MainMenu.handle_presetLoad), (2, MainMenu.handle_createPreset),
            (3, MainMenu.handle_help), (4, MainMenu.handle_exit)
        ]

        for item, handler in event_handlers:
            mainMenu.add_handler(item, handler)
        
        # run the menu after set up
        mainMenu.display()
    
    


def main() -> None:
    MainMenu.run_main_menu()

    


if __name__ == '__main__':
    main()
