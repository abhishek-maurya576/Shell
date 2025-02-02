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
    """Execute an external program with arguments and redirect stdout and/or stderr if needed."""
    executable = find_executable(command)
    if executable:
        try:
            # Open redirection files if provided.
            stdout_target = open(output_file, "w") if output_file else subprocess.PIPE
            stderr_target = open(error_file, "w") if error_file else subprocess.PIPE

            result = subprocess.run(
                [command] + args, stdout=stdout_target, stderr=stderr_target, text=True
            )

            # Close the file handles if we opened them.
            if output_file:
                stdout_target.close()
            if error_file:
                stderr_target.close()

            # If no redirection was provided, print any output.
            if not output_file and result.stdout:
                print(result.stdout.strip())
            # Don't print stderr if it is redirected to a file.
            if not error_file and result.stderr:
                print(result.stderr.strip())
        except Exception as e:
            print(f"Error executing {command}: {e}")
    else:
        error_message = f"{command}: command not found"
        if error_file:
            try:
                with open(error_file, "w") as f:
                    f.write(error_message + "\n")
            except Exception as e:
                print(f"Error writing to {error_file}: {e}")
        else:
            print(error_message)

def parse_and_execute(user_input):
    """Parse input, detect redirection for stdout (>) and stderr (2>), and execute commands."""
    parts = shlex.split(user_input)  # Handle quoted arguments properly
    if not parts:
        return

    output_file = None
    error_file = None

    # Check for stderr redirection first.
    if "2>" in parts:
        error_index = parts.index("2>")
        if error_index + 1 < len(parts):
            error_file = parts[error_index + 1]
            # Remove the redirection token and file from the parts.
            parts = parts[:error_index] + parts[error_index+2:]
        else:
            print("Syntax error: missing file for stderr redirection")
            return

    # Now check for stdout redirection.
    if ">" in parts:
        output_index = parts.index(">")
        if output_index + 1 < len(parts):
            output_file = parts[output_index + 1]
            # Remove the redirection token and file from the parts.
            parts = parts[:output_index]  # Remove everything from ">" onward.
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
        # For builtins, if redirection is given, write to that file.
        if output_file:
            try:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            except Exception as e:
                print(f"Error writing to {output_file}: {e}")
        elif error_file:
            try:
                with open(error_file, "w") as f:
                    f.write(output + "\n")
            except Exception as e:
                print(f"Error writing to {error_file}: {e}")
        else:
            print(output)

    elif command == "type":
        if not args:
            print("type: missing argument")
            return
        
        cmd_name = args[0]
        if cmd_name in BUILTINS:
            result = f"{cmd_name} is a shell builtin"
        else:
            executable = find_executable(cmd_name)
            if executable:
                result = f"{cmd_name} is {executable}"
            else:
                result = f"{cmd_name}: not found"

        if output_file:
            try:
                with open(output_file, "w") as f:
                    f.write(result + "\n")
            except Exception as e:
                print(f"Error writing to {output_file}: {e}")
        elif error_file:
            try:
                with open(error_file, "w") as f:
                    f.write(result + "\n")
            except Exception as e:
                print(f"Error writing to {error_file}: {e}")
        else:
            print(result)

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
