import sys
import os

# Define the list of built-in commands
BUILTINS = {"echo", "exit", "type"}

def find_executable(command):
    """Search for the command in the directories listed in $PATH."""
    paths = os.getenv("PATH", "").split(":")  # Get directories in $PATH
    for path in paths:
        executable_path = os.path.join(path, command)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path
    return None  # Command not found in $PATH

def main():
    while True:  # REPL loop
        sys.stdout.write("$ ")
        sys.stdout.flush()  # Ensure prompt is displayed immediately

        try:
            command = input().strip()  # Read input and strip extra spaces

            if command.startswith("exit"):  # Handle 'exit' command
                parts = command.split()
                exit_code = int(parts[1]) if len(parts) > 1 else 0
                sys.exit(exit_code)

            elif command.startswith("echo "):  # Handle 'echo' command
                print(command[5:])

            elif command.startswith("type "):  # Handle 'type' command
                cmd_name = command.split()[1]  # Extract the command name

                if cmd_name in BUILTINS:
                    print(f"{cmd_name} is a shell builtin")
                else:
                    executable = find_executable(cmd_name)
                    if executable:
                        print(f"{cmd_name} is {executable}")
                    else:
                        print(f"{cmd_name}: not found")

            else:
                print(f"{command}: command not found")  # Mock unknown commands

        except EOFError:  # Handle Ctrl+D (EOF)
            break
        except ValueError:  # Handle invalid exit codes
            print("exit: numeric argument required")
            sys.exit(255)  # Standard exit code for invalid exit args

if __name__ == "__main__":
    main()
