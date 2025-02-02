import sys

def main():
    sys.stdout.write("$ ")
    sys.stdout.flush()  # Ensure prompt is displayed immediately
    input()  # Wait for user input

if __name__ == "__main__":
    main()
