__version__ = "3.0"


"""
Main function of Second 3.0.
Called by second3.py or used as source file in second3.exe.
"""
def main():
    
    try:

        import ctypes
        from os import system, mkdir, startfile, remove, chdir
        from os.path import isfile, isdir, basename, expanduser
        from sys import exit as exitSys
        from getpass import getuser
        from platform import system as platSys, release as platRel, version as platVer
        from pathlib import Path
        from shutil import copy2, copytree, rmtree, which as Shuwhich
        from datetime import datetime as dt, date as d

        system('')

        header = "\033[95m"
        blue = "\033[94m"
        cyan = "\033[96m"
        green = "\033[92m"
        yellow = "\033[93m"
        red = "\033[91m"
        reset = "\033[0m"
        bold = "\033[1m"
        underline = "\033[4m"
        cls = "\033[H\033[J"

        class helpContents:

            def cdHelp():
                print(fr"""{bold}{green}CD:{reset}
{green}CD command allows the user to change the current working directory of Second.
File operations with relative paths take place from the current working directory.

{bold}{cyan}Syntax:{reset}
{cyan}CD ('/")<path>('/"){reset}

{yellow}Please note that when using the CD command, if you want to change to your root directory (i.e., drive, like C:\), please insert a backslash at the end (e.g., cd "C:{underline}\{reset}{yellow}") as without backslash it is interpreted as input to change the drive letter.

{green}{underline}Examples:{reset}
cd "myfolder"
cd "E:\example\new"
cd "custom\main"
""")

            def copyHelp():
                print(fr"""{bold}{green}COPY:{reset}
{green}COPY command allows the user to copy a file or folder from a source location to destination location.
This command can parse relative paths (from current working directory).

{bold}{cyan}Syntax:{reset}
{cyan}COPY ('/")<source>('/") ('/")<destination>('/"){reset}

{underline}Examples:{reset}
copy "myfolder" "e:\Folder"
copy "pictures\images.png" "desktop"
""")

            def delHelp():
                print(fr"""{bold}{green}DEL:{reset}
{green}DEL command allows the user to remove a file/directory from a given location.
This command can parse relative commands (from current working directory).

{bold}{cyan}Syntax:{reset}
{cyan}DEL ('/")<location>('/"){reset}

{underline}Examples:{reset}
del "myfolder"
del "documents\haha"
del "desktop\new.exe"
""")
            
            def mdirHelp():
                print(fr"""{bold}{green}MDIR:{reset}
{green}MDIR command allows the user to create a new directory.
This command can parse relative commands (from current working directory).

{bold}{cyan}Syntax:{reset}
{cyan}MDIR ('/")<pathWithDirectoryName>('/"){reset}

{underline}Examples:{reset}
mdir "myfolder"
mdir "desktop\new"
""")

            def helpMenu():
                print(f"""{bold}{underline}{green}Help:{reset} {green}\n
{bold}{cyan}CD{reset}        {green}Changes the current working direcory (CWD).
{bold}{cyan}CLS{reset}       {green}Clears the screen.
{bold}{cyan}COPY{reset}      {green}Copies file/directory to another directory
{bold}{cyan}DATE{reset}      {green}Displays today's date.
{bold}{cyan}DEL{reset}       {green}Delete a file/directory.
{bold}{cyan}EXIT{reset}      {green}Terminates Second.
{bold}{cyan}MDIR{reset}      {green}Creates a new directory.
{bold}{cyan}PROMPT{reset}    {green}Changes the prompt variable.
{bold}{cyan}SECOND{reset}    {green}Displays version compactibility and author.
{bold}{cyan}START{reset}     {green}Opens a file/directory.
{bold}{cyan}TIME{reset}      {green}Displays current time.
{bold}{cyan}TITLE{reset}     {green}Changes the title of the window.{reset}

{green}(Note: all commands work in any case.)
{reset}""")
            
            def secondPrint():
                print(f"""{blue}Second by CPythonist, Infinite, Inc.
{green}OS: {bold}Windows{reset}
{green}Compatible versions: {bold}10/11{reset}
{green}Administrative privileges required for some operations.{reset}
""")
            
            def promptHelp():
                print(fr"""{bold}{green}PROMPT:{reset}
{green}PROMPT command allows the user to change the Second prompt string.

{bold}{cyan}Syntax:{reset}
{cyan}PROMPT ('/")<customPrompt>('/")
This command when given given without any other data, restores the original prompt of the Second.

{underline}{green}Variables:{reset}
{cyan}%U    {green}Username of the user
{cyan}%S    {green}OS
{cyan}%R    {green}OS Release
{cyan}%P    {green}Current working directory (CWD)
{cyan}%%    {green}% symbol

{underline}Examples:{reset}
prompt "myPrompt"
prompt ">>>"
prompt "%U%P>"
""")
            
            def startHelp():
                print(fr"""{bold}{green}START:{reset}
{green}START command allows the user to open a file/directory.
This command when given given without any other data, restores the original title of the window.

{bold}{cyan}Syntax:{reset}
{cyan}START [('/")<fileOrDirectory>('/")]{reset}

{underline}Examples:{reset}
start "E:\new folder"
start "second"
""")
            
            def titleHelp():
                print(fr"""{bold}{green}TITLE:{reset}
{green}TITLE command allows the user to set the title of the console window in which Second is running.
This command when given given without any other data, restores the original title of the window.

{bold}{cyan}Syntax:{reset}
{cyan}TITLE [('/")<customTitle>('/")]{reset}

{underline}Examples:{reset}
title "myTitle"
title (-> Original title restored)
""")
        #############################################################################


        #############################################################################
        """
        Only one type of string is allowed in each of the individual commands.
        This function checks if the string passed to it has only one type of string.
        If it has two types, True and -1 is returned signifying improper quotes.
        If it has one type:
            1 is returned if the quotes used is single quotes, or
            2 is returned if the quotes used is double quotes
        If no quotes are present, 0 is returned.
        """
        def detectNoOrMultipleQuotes(string):
            countSingle, countDouble = 0, 0
            for i in string:
                if i == '\'':
                    countSingle += 1
                elif i == '\"':
                    countDouble += 1
            
            if (countSingle != 0 and countDouble != 0):
                return True, -1
            elif (countSingle == 0 and countDouble == 0):
                return True, 0
            else:
                if countSingle != 0:
                    return False, 1
                elif countDouble != 0:
                    return False, 2
        #############################################################################

        
        #############################################################################
        """
        Change directory command. Changes the current working directory for file operations.

        Returns the parsed path and change status as a tuple -> (path, changed)
        """
        def cd(remaining):

            if (temp:=detectNoOrMultipleQuotes(remaining))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command." if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                chdir(path)
                args = []
                appendToArgs = args.append
                quotes = '\'' if temp[1] == 1 else '\"'
                remaining = [i for i in remaining.split(quotes) if not (i.isspace() or i == '')]
                pathPresent = False
                completed = False

                for i in remaining:
                    if i.startswith('/'):
                        if len(i) == 2:
                            appendToArgs(i)
                        else:
                            return f"Invalid argument: '{i}'. CWD is unchanged.\n", False
                
                remaining = [i for i in remaining if i not in args]

                if len(args) == 1:
                    if len(remaining) == 0:
                        if args[0] in ("/h", "/?"):
                            return 'cdHelp', None
                        else:
                            return f"Unknown argument: '{args[0]}'. CWD is unchanged.\n", False
                    else:
                        return "Invalid format of data given. Please check the format of the command. Type help for the help menu. CWD is unchanged.\n", False
                
                elif len(args) == 0:
                    if len(remaining) == 1:
                        if isdir(remaining[0]):
                            pathTemp = str(Path(i).resolve())
                            chdir(pathTemp)
                            print()
                            return pathTemp, True
                        else:
                            return f"Directory not found: '{str(Path(remaining[0]).resolve())}'. CWD is unchanged.\n", False
                    else:
                        return f"Too many paths given. CWD is unchanged.\n", False
                
                else:
                    return "No path was given. CWD is unchanged.\n", False
        #############################################################################

                
        #############################################################################
        """
        Copies a file/directory to another directory, if destination directory and
        source file/directory exists, provided, permissions are available for read
        and write for source file/directory and destination folder.

        Returns copy message and copy status.
        """
        def copy(remaining):

            if (temp:=detectNoOrMultipleQuotes(remaining))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command.\n" if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                try:
                    args = []
                    appendToArgs = args.append
                    quotes = '\'' if temp[1] == 1 else '\"'
                    remaining = [i for i in remaining.split(quotes) if not (i.isspace() or i == '')]
                    count = 0
                    source, dest = None, None
                    sourceType = None

                    for i in remaining:
                        if i.startswith('/'):
                            if len(i) == 2:
                                appendToArgs(i)
                            else:
                                return f"Unknown argument: '{i}'. No file/directory was copied.\n", False
                        elif isfile(i):
                            if count == 0: source = i; sourceType = 'F'
                            elif count == 1: return "Destination cannot be a file.\n"
                            else: return "Two locations already given as input. No file was copied.\n", False
                            count += 1
                        elif isdir(i):
                            if count == 0: source = i; sourceType = 'D'
                            elif count == 1: dest = i
                            else: return "Two locations already given as input. No directory was copied.\n", False
                            count += 1
                        else:
                            return "File or directory not found. No file/directory was copied.\n", False
                    
                    for i in args:
                        if i in ("/h", "/?"):
                            return "copyHelp", None
                    
                    if (source != None) and (dest != None):
                        source = str(Path(source).resolve())
                        dest = str(Path(dest).resolve())
                        if sourceType == 'F':
                            try:
                                copy2(source, dest)
                                return "Copied successfully.\n", True
                            except PermissionError:
                                return f"Permissions not available for copying files from {source} to {dest}.\n", False
                        elif sourceType == 'D':
                            try:
                                temp = basename(source)
                                if not isdir(f"{dest}\\{temp}"): mkdir(f"{dest}\\{temp}")
                                copytree(source, f"{dest}\\{temp}", dirs_exist_ok=True)
                                return "Copied successfully.\n", True
                            except PermissionError:
                                return f"Required permissions not available to copy '{source}'. Process was terminated.\n", False
                    
                    else:
                        if source == None:
                            return "Source missing. No changed were made.\n", False
                        elif dest == None:
                            return "Destination missing. No changes were made.\n", False
                except:
                    return "Unknown error while copying. Process terminated.\n", False
        #############################################################################


        #############################################################################
        """
        Deletes a file/directory if it exists, provided permissions are available for deleting
        a file/directory in the parent directory.

        Returns delete message and delete status.
        """
        def delete(remaining):

            if (temp:=detectNoOrMultipleQuotes(remaining))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command." if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                args = []
                appendToArgs = args.append
                quotes = '\'' if temp[1] == 1 else '\"'
                remaining = [i for i in remaining.split(quotes) if not (i.isspace() or i == '')]

                for i in remaining:
                    if i.startswith('/'):
                        if len(i) == 2:
                            appendToArgs(i)
                        else:
                            return f"Unknown argument: '{i}'. No file/folder was deleted.\n", False
                
                remaining = [i for i in remaining if i not in args]

                if len(args) == 1:
                    if args[0] in ("/h", "/?"):
                        return "delHelp", None
                    else:
                        return f"Unknown argument: '{args[0]}'.", False
                
                elif len(args) == 0:
                    for i in remaining:
                        if (temp1:=isfile(path + '\\' + i)) or (isfile(i)):
                            actualPath = (path + '\\' + i) if temp1 else i
                            try:
                                remove(temp:=str(Path(actualPath).resolve()))
                                return f"File '{str(Path(temp).resolve())}' deleted successfully.\n", True
                            except PermissionError:
                                return f"Permissions unavailable for deleting '{str(Path(actualPath).resolve())}'. Process was terminated.\n", False
                        
                        elif (temp1:=isdir(path + '\\' + i)) or (isdir(i)):
                            actualPath = (path + '\\' + i) if temp1 else i
                            try:
                                rmtree(temp:=str(Path(actualPath).resolve()))
                                return f"Directory '{temp}' successfully deleted.\n", True
                            except PermissionError:
                                return f"Permissions unavailable for deleting {str(Path(actualPath).resolve())}. Process was terminated.\n", False
                        else:
                            return f"File/Directory not found: '{i}'.\n", False
                
                else:
                    return "Unknown arguments given. No directory was created.\n", False
        #############################################################################


        #############################################################################
        """
        Creates a new directory if the parent directory exists, provided write permissions are
        available in the parent directory.
        
        Returns text message and status.
        """
        def mdir(remaining):

            if (temp:=detectNoOrMultipleQuotes(remaining))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command." if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                args = []
                appendToArgs = args.append
                quotes = '\'' if temp[1] == 1 else '\"'
                remaining = [i for i in remaining.split(quotes) if not (i.isspace() or i == '')]

                for i in remaining:
                    if i.startswith('/'):
                        if len(i) == 2:
                            appendToArgs(i)
                        else:
                            return f"Invalid argument: '{i}'. No changes were made.\n", False
                
                remaining = [i for i in remaining if i not in args]
                
                if len(args) == 1:
                    if args[0] in ("/h", "/?"):
                        return "mdirHelp", None
                    else:
                        return f"Unknown argument: '{args[0]}'.\n", False
                
                elif len(args) == 0:
                    for i in remaining:
                        try:
                            mkdir(path + '\\' + i)
                            return "Directory successfully created.\n", True
                        except OSError:
                            return f"Illegal character used in a directory name: {i}", False
                        except FileNotFoundError:
                            return f"Second is unable to find the location: {i}", False
                
                else:
                    return "Unknown arguments given. No directory was created.\n", False
        #############################################################################

        
        #############################################################################
        """
        Changes the prompt of Second. When new prompt is specified, Second updates prompt variable
        to the new value.
        
        Returns prompt value or text message, and status.
        """
        def promptChanger(remainingUnchanged):
            if (temp:=detectNoOrMultipleQuotes(remainingUnchanged))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command." if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                args = []
                appendToArgs = args.append
                quotes = '\'' if temp[1] == 1 else '\"'
                remaining = [i for i in remainingUnchanged.split(quotes) if not (i.isspace() or i == '')]

                for i in remaining:
                    if i.startswith('/'):
                        if len(i) == 2:
                            appendToArgs(i)
                        else:
                            return f"Unknown argument: '{i}'.\n", False
                    
                remaining = [i for i in remaining if i not in args]

                if len(args) == 1:
                    if args[0] in ("/h", "/?"):
                        return "promptHelp", None
                    else:
                        return f"Unknown argument: '{args[0]}'.\n", False
                
                elif len(args) == 0:
                    if len(remaining) == 1:
                        return remaining[0], True
                    elif len(remaining) == 0:
                        return '', True
                    else:
                        return "Too many prompts given. Prompt is unchanged.\n", False
                
                else:
                    return "Unknown arguments given. Prompt is unchanged.\n", False
        #############################################################################


        #############################################################################
        """
        Starts a file/directory, or file in the PATH directories, if read permissions are available
        for opening the file/directory.
        
        Returns start message and start status.
        """
        def start(remaining):
            if (temp:=detectNoOrMultipleQuotes(remaining))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command." if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                args = []
                appendToArgs = args.append
                quotes = '\'' if temp[1] == 1 else '\"'
                remaining = [i for i in remaining.split(quotes) if not (i.isspace() or i == '')]

                for i in remaining:
                    if i.startswith('/'):
                        if len(i) == 2:
                            appendToArgs(i)
                        else:
                            return f"Invalid argument: '{i}'.\n", False
                
                remaining = [i for i in remaining if i not in args]

                if len(args) == 1:
                    if args[0] in ("/h", "/?"):
                        return "startHelp", None
                    else:
                        return f"Unknown argument: '{i}'", False
                
                elif len(args) == 0:
                    if len(remaining) == 1:
                        temp1 = isfile(path + '\\' + remaining[0])
                        temp2 = isfile(remaining[0])
                        temp3 = isdir(path + '\\' + remaining[0])
                        if (temp1) or (temp2) or (temp3) or (isdir(remaining[0])):
                            if temp1 or temp3:
                                try:
                                    startfile(path + '\\' + remaining[0])
                                    if temp1:
                                        return f"File '{str(Path(remaining[0]).resolve())}' opened successfully.\n", True
                                    return f"Directory {str(Path(remaining[0]).resolve())} opened successfully.\n", True
                                except PermissionError:
                                    return f"Error while opening file '{i}': Access is denied.\n", False
                            else:
                                startfile(str(Path(remaining[0]).resolve()))
                                if temp2:
                                    return f"File '{str(Path(remaining[0]).resolve())}' opened successfully.\n", True
                                return f"Directory '{str(Path(remaining[0]).resolve())}' opened successfully.\n", True
                        
                        try:
                            locate = Shuwhich(remaining[0])
                            if not (locate == None):
                                startfile(locate)
                                return f"File '{i}' successfully opened.\n", True
                            return f"The file/directory was not found: '{remaining[0]}'.\n", False
                        except PermissionError:
                            return f"Permissions required for opening file '{remaining[0]}' was not available.\n", False
                    else:
                        return "More than one file/directory was given. Process was terminated.\n", False
                else:
                    return f"Unknown arguments given. Process was terminated.\n", False
        #############################################################################


        #############################################################################
        """
        Changes the title of Second window.
        
        Returns title message and change status.
        """
        def title(remainingUnchanged):

            if (temp:=detectNoOrMultipleQuotes(remainingUnchanged))[0]:    #temp is declared here!
                return ("Multiple types of quotes detected. Only one type of quote is allowed in \
each command." if temp[1] == -1 else "No quotes detected. Quotes must be used.\n"), False

            else:
                args = []
                appendToArgs = args.append
                quotes = '\'' if temp[1] == 1 else '\"'
                remaining = [i for i in remainingUnchanged.split(quotes) if not (i.isspace() or i == '')]

                for i in remaining:
                    if i.startswith('/'):
                        if len(i) == 2:
                            appendToArgs(i)
                        else:
                            return f"Invalid argument: {i}. Title is unchanged.\n", False

                remaining = [i for i in remaining if i not in args]
                
                if len(args) == 1:
                    if args[0] in ("/h", "/?"):
                        return "titleHelp", None
                    else:
                        return f"Unknown argument: {args[0]}. Title is unchanged.\n", False
                
                elif len(args) == 0:
                    if len(remaining) == 1:
                        try:
                            ctypes.windll.kernel32.SetConsoleTitleW(remaining[0])
                            return "Title changed successfully.\n", True
                        except:
                            return f"Unable to change title to '{remaining[0]}'. Title is unchanged.\n", False
                    elif len(remaining) == 0:
                        return "Empty title is not allowed. Title is unchanged.\n", False
                    else:
                        return "Too many titles given. Title is unchanged.\n", False
                else:
                    return "Unknown arguments given. No changes were made in the title.\n", False
        #############################################################################


        #############################################################################
        """
        Function IO(path, prompt) manages the input/output of Second.
        Works:
        1. Updates prompt variables.
        2. Takes input.
        3. Parses input string.
        4. Checks if parsed command is valid.
        5. Calls necessary functions/displays necessary information if command is valid.
        6. Displays appropriate error messages if command is invalid.

        Returns path and prompt so that these can be passed to IO(path, prompt) again.
        """
        def IO(path, prompt):
            promptTemp = prompt[:]
            if '%' in promptTemp:
                
                windowsVersion = platVer()
                windowsRelease = platRel()

                if int(windowsVersion.split('.')[0]) == 10:
                    if int(windowsVersion.split('.')[2]) > 22000:
                        windowsRelease = '11'
                    else:
                        windowsRelease = '10'
                
                promptTemp = promptTemp.replace("%P", path).replace("%U", getuser()).replace("%S", platSys()).replace("%R", windowsRelease)

                promptTemp = promptTemp.replace(r"%p", path).replace(r"%u", getuser()).replace(r"%s", platSys()).replace(r"%r", windowsRelease).replace(r"%%", '%')

            commandFull = input(promptTemp)
            commandFullUnchanged, commandFull = commandFull, commandFull.lower()

            command = commandFull
            remaining = ''
            remainingUnchanged = ''

            if commandFull in valid:
                command = commandFull
            else:
                for i in range(len(commandFull)):
                    if commandFull[i] == ' ':
                        command = commandFull[:i]
                        remaining = commandFull[i+1:]
                        remainingUnchanged = commandFullUnchanged[i+1:]
                        break
            
            if command == valid[0]:
                if remaining == '' or remaining.isspace():
                    print(f"{red}Required data to change directory was not given. CWD is unchanged.\n{reset}")
                else:
                    result = cd(remaining)
                    if result[1] == True:
                        path = result[0]
                    elif result[1] == None:
                        helpContents.cdHelp()
                    else:
                        print(red + result[0] + reset)
            
            elif command == valid[1]:
                system("cls")
                print()
                # if remaining == '' or remaining.isspace():
                #     system("cls")
                #     print()
                # else:
                #     print(f"{red}Unknown arguments given. No changes were made to console.\n{reset}")
            
            elif command == valid[2]:
                if remaining == '' or remaining.isspace():
                    print(f"{red}Required data for copying is not given. No file/folder was copied.\n{reset}")
                else:
                    result = copy(remaining)
                    if result[1]:
                        print(green + result[0] + reset)
                    elif result[1] == None:
                        helpContents.copyHelp()
                    else:
                        print(red + result[0] + reset)
            
            elif command == valid[3]:
                if remaining == '' or remaining.isspace():
                    date = d.today().strftime(r"%d.%m.%Y (%d %B %Y)")
                    print(f"{green}Date today: {date} (dd.mm.yyyy)\n{reset}")
                else:
                    print(f"{red}Unknown arguments given.\n{reset}")
            
            elif command == valid[4]:
                if remaining == '' or remaining.isspace():
                    print(f"{red}Location for deletion is required. No changes were made.\n{reset}")
                else:
                    result = delete(remaining)
                    if result[1]:
                        print(green + result[0] + reset)
                    elif result[1] == None:
                        helpContents.delHelp()
                    else:
                        print(red + result[0] + reset)
            
            elif command == valid[5]:
                print(f"{green}Program exited with code 0.{reset}")
                exitSys(0)
                
            elif command == valid[6]:
                if not (remaining == '' or remaining.isspace()):
                    print(f"{red}Unknown arguments given.\n{green}\nHelp menu is still printed as \
no other argument/data is required by it in any case.\n{reset}")
                
                helpContents.helpMenu()
            
            elif command == valid[7]:
                if remaining == '' or remaining.isspace():
                    print(f"{red}Required data for making a directory was not given. No changes were made.\n{reset}")
                else:
                    result = mdir(remaining)
                    if result[1]:
                        print(green + result[0] + reset)
                    elif result[1] == None:
                        helpContents.mdirHelp()
                    else:
                        print(red + result[0] + reset)
            
            elif command == valid[8]:
                if remaining == '' or remaining.isspace():
                    prompt = "%U@%S%R&&%P:~ $"
                    print()
                else:
                    result = promptChanger(remaining)
                    if result[1]:
                        prompt = result[0]
                        print()
                    elif result[1] == None:
                        helpContents.promptHelp()
                    else:
                        print(red + result[0] + reset)
            
            elif command == valid[9]:
                if remaining == '' or remaining.isspace():
                    helpContents.secondPrint()
                else:
                    print(f"{red}Unknown arguments given.\n{reset}")
            
            elif command == valid[10]:
                if remaining == '' or remaining.isspace():
                    print(f"{red}Required data for opening a file/directory was not given.\n{reset}")
                else:
                    result = start(remaining)
                    if result[1]:
                        print(green + result[0] + reset)
                    elif result[1] == None:
                        helpContents.startHelp()
                    else:
                        print(red + result[0] + reset)

            elif command == valid[11]:
                if remaining == '' or remaining.isspace():
                    time = dt.now().strftime("%I:%M.%S [%f] %p (%d %B %Y)")
                    print(f"{green}Time now: {time} (hh.mm.ss [microseconds] am/pm)\n{reset}")
                else:
                    print(f"{red}Unknown arguments given.\n{reset}")
            
            elif command == valid[12]:
                if remaining == '' or remaining.isspace():
                    try:
                        ctypes.windll.kernel32.SetConsoleTitleW("Second 3.0")
                        print()
                    except:
                        print(f"{red}Unable to restore default title.\n{reset}")
                else:
                    result = title(remainingUnchanged)
                    if result[1]:
                        print(green + result[0] + reset)
                    elif result[1] == None:
                        helpContents.titleHelp()
                    else:
                        print(red + result[0] + reset)
                
            else:
                if command == '':
                    print()
                else:
                    print(f"{red}Invalid command: '{bold}{command}{reset}{red}'.\n{reset}")
            
            return path, prompt
        #############################################################################


        ctypes.windll.kernel32.SetConsoleTitleW("Second 3.0")

        print(f"""
{cyan}Infinite Second 3.0{reset}
Made by ... <NameError: Name not found>
Developed in CPython 3.9.6, 3.10.0, 3.11.6, 3.12.0
Compiled in CPython 3.11.6
Thanks to stackoverflow.com for helping me out!

Type 'help' without quotes for the help menu.
""")

        valid = ("cd", "cls", "copy", "date", "del", "exit", "help", "mdir", "prompt", "second", "start", "time", "title")

        path = expanduser('~')
        prompt = "%U@%S%R&&%P:~ $"  #prompt = f"{getuser()}@{platSys()}{platRel()}&&{path}:~ $"
        
        while True:
            try:
                path, prompt = IO(path, prompt)
            
            except KeyboardInterrupt:
                print()
            
            except EOFError:
                print(f"{green}Program exited with code 0.{reset}")
                exitSys(0)
    
    
    except Exception as excep:
        excepName = type(excep).__name__
        print(f"Fatal error:\n{excepName}:{excep}")
        try:
            print(excepName, ': ', excep, sep='')
            from datetime import datetime as dt
            from pickle import dump
            with open("crashReports.dat", 'ab+') as f:
                f.seek(0)
                now = dt.now()
                dump(f"{now} =====> {excepName}: --> {str(excep)}", f)
        except FileNotFoundError:
            try:
                from datetime import datetime as dt
                from pickle import dump
                from os import makenod
                makenod("crashReports.dat")
                with open("crashReports.dat", 'ab+') as f:
                    f.seek(0)
                    now = dt.now()
                    dump(f"Previous 'crashReports.dat' file not found. New file created on {now}.", f)
                    dump(f"{now} =====> {excepName}: --> {str(excep)}", f)
            except:
                pass
        except:
            pass
#Viewed by Prithvi and verified.