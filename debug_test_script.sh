#!/bin/bash

# Create directories for output files
mkdir -p ./baz
mkdir -p ./bar
echo "Directories created."

# Redirecting stdout (1>) and stderr (2>) correctly
ls -1 ./baz/foo.md > ./baz/foo.md
echo "Executed ls command."

echo 'Hello James' > ./baz/qux.md  # Fixed redirection issue
echo "Wrote to baz/qux.md."

echo 'Emily file cannot be found' 2> ./bar/foo.md
echo "Wrote error message to bar/foo.md."

ls -1 nonexistent 2> ./bar/bar.md
echo "Executed ls command for nonexistent file."

cat ./baz/banana nonexistent 2> ./bar/qux.md
echo "Executed cat command."
