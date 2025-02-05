import os
import sys
import subprocess
from shutil import which as find_executable

def execute_command(command, args=[], output_file=None, error_file=None):
    executable = find_executable(command)

    # Handle case where the command is not found
    if not executable:
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
        return  # Exit early if command is not found

    try:
        # Create directories if they don't exist
        if output_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
        if error_file:
            os.makedirs(os.path.dirname(error_file), exist_ok=True)

        # Run the command
        result = subprocess.run(
            [executable] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Redirect stdout to file if specified
        if output_file:
            with open(output_file, "w") as f:
                f.write(result.stdout)

        # Redirect stderr to file if specified
        if error_file:
            with open(error_file, "w") as f:
                f.write(result.stderr)

        # Print output to console
        if not output_file:
            print(result.stdout, end="")

        if not error_file:
            print(result.stderr, end="", file=sys.stderr)

    except Exception as e:
        print(f"Error executing {command}: {e}", file=sys.stderr)

