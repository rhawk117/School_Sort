import os
import keyboard
import time


class Menu:
    def __init__(self, prompt: str, options: list) -> None:
        self.set_menu(prompt, options)

    def set_menu(self, prompt: str, opt: list) -> None:
        # consturctor logic
        self.prompt = prompt
        self.options = opt
        self.slctedIndex = 0

    def clear_screen(self):
        # clears the console
        os.system('cls' if os.name == 'nt' else 'clear')

    # Displays List of options in the console, highlights the selected Index
    def display_lines(self):
        self.clear_screen()
        for i, choice in enumerate(self.options):
            if i == self.slctedIndex:
                # Hightlight the Selected Index
                print("\033[47m\033[30m" + ">>" +
                      choice.strip() + "\033[0m".center(60))
            else:
                print(choice.strip().center(60))

    # Core Logic of Menu
    def run_menu(self, eventHandler):
        while True:
            try:
                if keyboard.is_pressed('up'):
                    self.slctedIndex = max(0, self.slctedIndex - 1)
                    self.display_lines()
                    # Small delay to prevent overly rapid scrolling
                    time.sleep(0.1)

                elif keyboard.is_pressed('down'):
                    self.slctedIndex = min(
                        len(self.options) - 1, self.slctedIndex + 1)
                    self.display_lines(self.options, self.slctedIndex)
                    time.sleep(0.1)  # Small delay

                elif keyboard.is_pressed('enter'):
                    eventHandler(self.slctedIndex)
                    break

                elif keyboard.is_pressed('esc'):
                    break
            except:
                break  # Break on any keyboard-related exceptions
