import sys
import os
import subprocess

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

def execute_command(command, args):
    """Execute an external program with arguments."""
    executable = find_executable(command)
    if executable:
        try:
            subprocess.run([executable] + args)  # Run the program with arguments
        except Exception as e:
            print(f"Error executing {command}: {e}")
    else:
        print(f"{command}: command not found")

def main():
    while True:  # REPL loop
        sys.stdout.write("$ ")
        sys.stdout.flush()  # Ensure prompt is displayed immediately

        try:
            user_input = input().strip()  # Read input and strip extra spaces
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":  # Handle 'exit' command
                exit_code = int(args[0]) if args else 0
                sys.exit(exit_code)

            elif command == "echo":  # Handle 'echo' command
                print(" ".join(args))

            elif command == "type":  # Handle 'type' command
                if not args:
                    print("type: missing argument")
                    continue
                
                cmd_name = args[0]

                if cmd_name in BUILTINS:
                    print(f"{cmd_name} is a shell builtin")
                else:
                    executable = find_executable(cmd_name)
                    if executable:
                        print(f"{cmd_name} is {executable}")
                    else:
                        print(f"{cmd_name}: not found")

            else:
                execute_command(command, args)  # Run external commands

        except EOFError:  # Handle Ctrl+D (EOF)
            break
        except ValueError:  # Handle invalid exit codes
            print("exit: numeric argument required")
            sys.exit(255)  # Standard exit code for invalid exit args

if __name__ == "__main__":
    main()
