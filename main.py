# *** created by rhawk117 ***
# main.py -- puts the pieces together
 
import os
import sys 
from menu import Menu
from preset import Preset
import time 
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
            # pause program for user to read
            print('[i] temporarily pausing the program for 5 seconds... [i]')
            time.sleep(5)
            print('''\n\a\a\a[i] When the Main Menu appears 
                  -> Select <<'Create a Preset'>> to create a preset that the program can use 
                  to sort the directory 
                  containing your courses [i]''')
            time.sleep(3)
            print('''[i] If you would like to learn how the program works and how it sorts files, select the <<'help'>> option in the main menu to ensure you understand the naming conventions required to sort files [i]
                        \n''')
            time.sleep(3)
            print(('*' * 60) + '\n\n')
            input('[*] Press "Enter" to continue [*]\n'.center(60))
            
            
    # When the user selects 'Load a Preset'
    @staticmethod
    def handle_presetLoad() -> None:
        load_preset = Preset()
        load_preset.load_preset_hndler()

    # When a user selects 'Create a Preset'
    @staticmethod
    def handle_createPreset() -> None:
        create_preset = Preset()
        create_preset.preset_creation_hndler()

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
        print('Incomplete option')

    # When a usr selects 'Exit'
    @staticmethod
    def handle_exit() -> None:
        print("\n[*] Exiting Program [*]".center(60))
        sys.exit()

    # Constructs and runs the main menu of program
    @staticmethod
    def run_main_menu() -> None:
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
        mainMenu.display()
    
    


def main() -> None:
    MainMenu.run_main_menu()

    

if __name__ == '__main__':
    main()
