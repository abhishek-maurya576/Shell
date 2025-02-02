import sys

def main():
    while True:  # Keep running the REPL
        sys.stdout.write("$ ")
        sys.stdout.flush()  # Ensure prompt appears immediately
        
        try:
            command = input()
            print(f"{command}: command not found")  # Mock command handling
        except EOFError:  # Handle Ctrl+D (End of Input)
            break

if __name__ == "__main__":
    main()
