# *** created by rhawk117 ***
# main.py -- puts the pieces together
import os
import sys 
from menu import Menu
from preset import Preset
import time 
from pprint import pprint 
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
