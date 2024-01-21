import os
import sys 
from Menu import Menu
from preset import Preset



class MainMenu:
    @staticmethod
    def handle_presetLoad():
        load_preset = Preset()
        load_preset.load_preset_hndler()

    @staticmethod
    def handle_createPreset():
        create_preset = Preset()
        create_preset.preset_creation_hndler()
        MainMenu.run_menu()

    @staticmethod
    def handle_help():
        print('Incomplete option')

    @staticmethod
    def handle_exit():
        print("\n[*] Exiting Program [*]".center(60))
        sys.exit()

    @staticmethod
    def run_menu():
        mainMenu = Menu("[ Select one of the following options listed below ]")
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
    print('*'*60)

def upon_start() -> None:
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(path)  # change CWD to program's dir
    header()

def main() -> None:
    header()
    MainMenu.run_menu()

    

        

        


    


if __name__ == '__main__':
    main()
