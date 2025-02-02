import sys

def main():
    while True:  # Keep running the REPL
        sys.stdout.write("$ ")
        sys.stdout.flush()  # Ensure prompt appears immediately

        try:
            command = input().strip()  # Read and clean input

            if command.startswith("exit"):  # Handle 'exit' command
                parts = command.split()
                exit_code = int(parts[1]) if len(parts) > 1 else 0
                sys.exit(exit_code)

            elif command.startswith("echo "):  # Handle 'echo' command
                print(command[5:])  # Print everything after 'echo '

            else:
                print(f"{command}: command not found")  # Mock unknown commands

        except EOFError:  # Handle Ctrl+D (End of Input)
            break
        except ValueError:  # Handle invalid exit codes
            print("exit: numeric argument required")
            sys.exit(255)  # Standard exit code for invalid exit args

if __name__ == "__main__":
    main()
