from InquirerPy import prompt
from preset import Preset
import sys


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

# Generic Re-Usable Menu Class 
class Menu:
    menu_stack: list = []  # Static stack to track menu history

    def __init__(self, prompt):
        # List of all user options
        self.options: list = []

        # Prompt for the User Input
        self.prompt_message: str = prompt

        # Event Handlers for each menu option
        self.handlers: dict = {}

        # Handler for the go_back option
        self.add_handler(None, self.go_back)
        

    def add_options(self, option_titles:list):
        self.options.extend(
            {"name": title, "value": index + 1}
            for index, title in enumerate(option_titles)
        )

    def add_back_option(self, title = "Back"):
        self.options.append({"name": title, "value": None})

    def clear_options(self):
        self.options = []
        self.handlers = {}
        self.add_handler(None, self.go_back)

    def add_handler(self, option_value, handler_function):
        self.handlers[option_value] = handler_function

    def display(self):
        Menu.menu_stack.append(self)
        formatted_options = self.options
        questions = [
            {
                "type": "list",
                "name": "choice",
                "message": self.prompt_message,
                "choices": formatted_options
            }
        ]
        response = prompt(questions)
        choice = response["choice"]
        handler = self.handlers.get(choice)

        if handler:
            handler()

    def go_back(self):
        if len(Menu.menu_stack) > 1:
            Menu.menu_stack.pop()  # Remove current menu
            previous_menu = Menu.menu_stack[-1]  # Get previous menu
            previous_menu.display()  # Display previous menu







    
    


    
    








