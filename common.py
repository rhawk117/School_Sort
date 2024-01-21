import os 
import re as regex 


# Input Validation methods
class Input:
    @staticmethod
    def get_path_input(prompt: str):
        file_path = input('[?] Enter the courses associated file path: ').strip(
            '"')  # remove double quotes
        try:
            parsed_path = os.path.normpath(file_path.replace("\\", "\\\\"))
            if os.path.exists(parsed_path) and os.path.isdir(parsed_path):
                return parsed_path
            
            print('[!] USER INPUT INVALID [!]\n' +
                  f'> The File Path provided ({parsed_path}) does not exist!')
        except ValueError:
            print(
                '[!] Could not normalize file path provided, please re-enter the key and file path for this entry [!]')

        # recursive call only executed if exception occurs or if the path provided is invalid
        return Input.get_path_input(prompt)

    @staticmethod
    def get_input(prompt: str, options: list) -> str:
        usr_input = input('[?] ' + prompt)
        if usr_input.lower() in options:
            return usr_input.lower()
        print(f'[!] User Input Invalid [!]\n > Options: ' + ' , '.join(options))
        return Input.get_input(prompt, options)

    @staticmethod
    def check_file_name(file_name: str, extension: str) -> bool:
        '''
        checks the file name inputed by user to see if it's a 
        valid file name returning true if it is, false otherwise
        '''
        if file_name == '':
            return False

        prefix = '[!] Invalid File Name [!]\n'
        expression = regex.compile(r"^[A-Za-z0-9_.-]*$")
        if not regex.match(expression, file_name):
            print(prefix + 'Cannot create a file with invalid characters')
            return False

        # Check for valid extension
        if not file_name.endswith('.' + extension):
            print(prefix + f'Files must end with the .{extension} extension')
            return False

        # Check for maximum length
        if len(file_name) > 25:
            print(prefix + 'File names should be less than 25 characters')
            return False

        # Check for reserved names
        if file_name.lower() in ["con", "prn", "nul"]:
            print(prefix + 'File names cannot be reserved')
            return False

        # Check in Presets folder if file with same name exists
        if os.path.isfile('output\\' + file_name):
            print(prefix + 'A file with the same name already exist!')
            return False

        return True  # file name passes all checks, return True
