import sys
import os
import subprocess

BUILTINS = {"echo", "exit", "type"}

def find_executable(command):
    """Search for the command in $PATH and return its absolute path if found."""
    paths = os.getenv("PATH", "").split(":")
    for path in paths:
        executable_path = os.path.join(path, command)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path
    return None

def execute_command(command, args):
    """Execute an external program with arguments, ensuring Arg #0 is just the command name."""
    executable = find_executable(command)
    if executable:
        try:
            subprocess.run([command] + args)  # Pass only command name, not full path
        except Exception as e:
            print(f"Error executing {command}: {e}")
    else:
        print(f"{command}: command not found")

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input().strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                sys.exit(int(args[0]) if args else 0)

            elif command == "echo":
                print(" ".join(args))

            elif command == "type":
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

        except EOFError:
            break
        except ValueError:
            print("exit: numeric argument required")
            sys.exit(255)

if __name__ == "__main__":
    main()
