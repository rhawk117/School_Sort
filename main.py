import os
import sys 
from Menu import Menu
from preset import Preset



class MainMenu:

    # handles the logic and checks performed whenever the program is run 
    @staticmethod
    def upon_start() -> None:
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        os.chdir(path)  # change CWD to program's dir

        # check if presets directory exists, if not make it for the user
        if not os.path.exists("presets"):
            print("""
                [!] NOTE The presets directory could not be found likely due to the program being run for the first time, 
                it has been created for future use [!] 
            """.center(60))
            print('''\n[*] Restart the program and select 'Create a Preset'
                to create a preset to be used to sort the directory containing your courses [*]''')
            os.mkdir("presets")
            sys.exit()


    # When the user selects 'Load a Preset'
    @staticmethod
    def handle_presetLoad():
        load_preset = Preset()
        load_preset.load_preset_hndler()

    # When a user selects 'Create a Preset'
    @staticmethod
    def handle_createPreset():
        create_preset = Preset()
        create_preset.preset_creation_hndler()
        MainMenu.run_main_menu()


    # When a usr selects 'help'
    @staticmethod
    def handle_help():
        print('Incomplete option')

    # When a usr selects 'Exit'
    @staticmethod
    def handle_exit():
        print("\n[*] Exiting Program [*]".center(60))
        sys.exit()

    # Constructs and runs the main menu of program
    @staticmethod
    def run_main_menu():
        # Instantiate and create the Menu object
        mainMenu = Menu(f"{header()}[ Select one of the following options listed below ]")
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
    
    
def header() -> str:
    main_menu_txt = r"""
        __         _                 _                  _  __  
        / /___  ___| |__   ___   ___ | |  ___  ___  _ __| |_\ \ 
        / // __|/ __| '_ \ / _ \ / _ \| | / __|/ _ \| '__| __|\ \
        \ \\__ \ (__| | | | (_) | (_) | | \__ \ (_) | |  | |_ / /
        \_\___/\___|_| |_|\___/ \___/|_| |___/\___/|_|   \__/_/ 
                                                                """
    main_menu_txt += "\n*** created by rhawk117 ***\n"
    return main_menu_txt




def main() -> None:
    MainMenu.run_main_menu()

    

if __name__ == '__main__':
    main()
