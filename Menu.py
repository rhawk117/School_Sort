# *** created by rhawk117 ***
# menu.py -- implements a menu object that is re-usuable throughout program
from InquirerPy import prompt
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
        
    # method takes list parameter and sets the values to menu options
    def add_options(self, option_titles:list):
        self.options.extend(
            {"name": title, "value": index + 1}
            for index, title in enumerate(option_titles)
        )

    # if we want the menu to go back to the previous we can call this func
    def add_back_option(self, title = "Back"):
        self.options.append({"name": title, "value": None})

    # method resets all class attributes
    def clear_options(self):
        self.options = []
        self.handlers = {}
        self.add_handler(None, self.go_back)

    # method adds a handler for a specific option 
    def add_handler(self, option_value, handler_function):
        self.handlers[option_value] = handler_function

    # once all handlers and options are created this function runs the logic needed to run the menu
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
        response = prompt(questions) # display the menu 
        choice = response["choice"] # save the usrs choice
        handler = self.handlers.get(choice) # fetch the appropriate handler for the selected choice

        if handler:
            handler()

    # method for when we want to go back to the previous menu 
    def go_back(self):
        if len(Menu.menu_stack) > 1:
            Menu.menu_stack.pop()  # Remove current menu
            previous_menu = Menu.menu_stack[-1]  # Get previous menu
            previous_menu.display()  # Display previous menu




