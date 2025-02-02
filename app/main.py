import sys
import os
import subprocess
import shlex

BUILTINS = {"echo", "exit", "type"}

def find_executable(command):
    """Search for the command in $PATH and return its absolute path if found."""
    paths = os.getenv("PATH", "").split(":")
    for path in paths:
        executable_path = os.path.join(path, command)
        if os.path.isfile(executable_path) and os.access(executable_path, os.X_OK):
            return executable_path
    return None

def execute_command(command, args, output_file=None):
    """Execute an external program with arguments and redirect output if needed."""
    executable = find_executable(command)
    if executable:
        try:
            if output_file:
                with open(output_file, "w") as out:
                    result = subprocess.run(
                        [command] + args, stdout=out, stderr=subprocess.PIPE, text=True
                    )
                    if result.stderr:
                        print(result.stderr.strip())  # Print errors if any
            else:
                result = subprocess.run(
                    [command] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                if result.stdout:
                    print(result.stdout.strip())  # Print stdout
                if result.stderr:
                    print(result.stderr.strip())  # Print stderr (for errors)
        except Exception as e:
            print(f"Error executing {command}: {e}")
    else:
        print(f"{command}: command not found")


def parse_and_execute(user_input):
    """Parse input, detect redirection, and execute commands accordingly."""
    parts = shlex.split(user_input)  # ✅ Handle quoted arguments properly
    if not parts:
        return

    # Detect redirection (`>` or `1>`)
    redirect_index = None
    if ">" in parts:
        redirect_index = parts.index(">")
    elif "1>" in parts:
        redirect_index = parts.index("1>")

    output_file = None
    if redirect_index is not None:
        if redirect_index + 1 < len(parts):  # Ensure a file is specified
            output_file = parts[redirect_index + 1]
            parts = parts[:redirect_index]  # Remove redirection part from command
        else:
            print("Syntax error: missing file for redirection")
            return

    if not parts:
        print("Syntax error: missing command before redirection")
        return

    command = parts[0]
    args = parts[1:]

    if command == "exit":
        sys.exit(int(args[0]) if args else 0)

    elif command == "echo":
        output = " ".join(args)
        if output_file:
            with open(output_file, "w") as f:
                f.write(output + "\n")
        else:
            print(output)

    elif command == "type":
        if not args:
            print("type: missing argument")
            return
        
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
        execute_command(command, args, output_file)

def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        try:
            user_input = input().strip()
            if user_input:
                parse_and_execute(user_input)

        except EOFError:
            break
        except ValueError:
            print("exit: numeric argument required")
            sys.exit(255)

if __name__ == "__main__":
    main()
