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
            # Create parent directories if they don't exist
            for file in [output_file, error_file]:
                if file and os.path.dirname(file):
                    os.makedirs(os.path.dirname(file), exist_ok=True)

            # Open output and error files for redirection
            with open(output_file, "w") if output_file else None as stdout, \
                 open(error_file, "w") if error_file else None as stderr:
                result = subprocess.run(
                    [executable] + args,
                    stdout=stdout if output_file else subprocess.PIPE,
                    stderr=stderr if error_file else subprocess.PIPE,
                    text=True
                )

            # Print output if not redirected
            if not output_file and result.stdout:
                print(result.stdout.strip())

            if not error_file and result.stderr:
                print(result.stderr.strip(), file=sys.stderr)
                    
        except Exception as e:
            print(f"Error executing {command}: {e}", file=sys.stderr)
    else:
        error_message = f"{command}: command not found"
        if error_file:
            try:
                os.makedirs(os.path.dirname(error_file), exist_ok=True)
                with open(error_file, "w") as f:
                    f.write(error_message + "\n")
            except Exception as e:
                print(f"Error writing to {error_file}: {e}", file=sys.stderr)
        else:
            print(error_message, file=sys.stderr)

def parse_and_execute(user_input):
    """Parse input, detect redirection for stdout (>) and stderr (2>), and execute commands."""
    parts = shlex.split(user_input)
    if not parts:
        return

    output_file = None
    error_file = None
    new_parts = []

    i = 0
    while i < len(parts):
        if parts[i] == "2>" and i + 1 < len(parts):
            error_file = parts[i + 1]
            i += 2
        elif parts[i] == ">" and i + 1 < len(parts):
            output_file = parts[i + 1]
            i += 2
        else:
            new_parts.append(parts[i])
            i += 1

    if not new_parts:
        print("Syntax error: missing command before redirection", file=sys.stderr)
        return

    command = new_parts[0]
    args = new_parts[1:]

    if command == "exit":
        sys.exit(int(args[0]) if args else 0)

    elif command == "echo":
        output = " ".join(args)

        try:
            for file in [output_file, error_file]:
                if file and os.path.dirname(file):
                    os.makedirs(os.path.dirname(file), exist_ok=True)

            if output_file:
                with open(output_file, "w") as f:
                    f.write(output + "\n")
            else:
                print(output)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)

    elif command == "type":
        if not args:
            print("type: missing argument", file=sys.stderr)
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
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, "w") as f:
                    f.write(result + "\n")
            except Exception as e:
                print(f"Error writing to {output_file}: {e}", file=sys.stderr)
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
            print("exit: numeric argument required", file=sys.stderr)
            sys.exit(255)

if __name__ == "__main__":
    main()
