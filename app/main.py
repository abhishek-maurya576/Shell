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

def execute_command(command, args, output_file=None, error_file=None):
    """Execute an external program with arguments and redirect output if needed."""
    executable = find_executable(command)
    if executable:
        try:
            stdout_target = open(output_file, "w") if output_file else subprocess.PIPE
            stderr_target = open(error_file, "w") if error_file else subprocess.PIPE

            result = subprocess.run(
                [command] + args, stdout=stdout_target, stderr=stderr_target, text=True
            )

            if output_file:
                stdout_target.close()
            if error_file:
                stderr_target.close()

            # Print stdout and stderr if not redirected
            if result.stdout and not output_file:
                print(result.stdout.strip())
            if result.stderr and not error_file:
                print(result.stderr.strip())

        except Exception as e:
            print(f"Error executing {command}: {e}")
    else:
        error_message = f"{command}: command not found"
        if error_file:
            with open(error_file, "w") as f:
                f.write(error_message + "\n")
        else:
            print(error_message)

def parse_and_execute(user_input):
    """Parse input, detect redirection for stdout (>) and stderr (2>), and execute commands."""
    parts = shlex.split(user_input)  # ✅ Handle quoted arguments properly
    if not parts:
        return

    output_file = None
    error_file = None

    # Detect `>` (stdout redirection) and `2>` (stderr redirection)
    if "2>" in parts:
        error_index = parts.index("2>")
        if error_index + 1 < len(parts):
            error_file = parts[error_index + 1]
            parts = parts[:error_index]  # Remove redirection part from command
        else:
            print("Syntax error: missing file for stderr redirection")
            return

    if ">" in parts:
        output_index = parts.index(">")
        if output_index + 1 < len(parts):
            output_file = parts[output_index + 1]
            parts = parts[:output_index]  # Remove redirection part from command
        else:
            print("Syntax error: missing file for stdout redirection")
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
        execute_command(command, args, output_file, error_file)

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
