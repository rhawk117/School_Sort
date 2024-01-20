import os
from pathlib import Path
import sys 
from Menu import Menu
from preset import Preset
from common import Input
    


                
        
        



def main_menu_handler(selectedIndex:int):
    format_util = "*"*60
    print(format_util)
    if selectedIndex == 0: # usr wants to load a preset
        User = Preset()
        User.slct_preset()
        
    elif selectedIndex == 1: # usr wants to create a preset 

        path = Input.get_path_input(
            '[?] Enter the file path containing your course directories: '
        )
        new_preset = Preset.auto_preset_data(path)
        Preset.create_preset_file(new_preset)

    elif selectedIndex == 2: # usr wants help prompt to appear 
        pass

    elif selectedIndex == 3: # usr wants to exit program
        pass




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
    MainMenu = Menu("Select One of the Following",["Load a Preset", "Create a Preset", "Help", "QU"])
    MainMenu.run_menu(main_menu_handler)

    

        

        


    


if __name__ == '__main__':
    main()
