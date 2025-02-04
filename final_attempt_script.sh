#!/bin/bash

# Create directories for output files
mkdir -p ./baz
mkdir -p ./bar
echo "Directories created."

# Redirecting stdout (1>) and stderr (2>) correctly
if ls -1 ./baz/foo.md > ./baz/foo.md; then
    echo "Executed ls command for baz/foo.md."
else
    echo "Failed to execute ls command for baz/foo.md."
fi

if echo 'Hello James' > ./baz/qux.md; then
    echo "Wrote to baz/qux.md."
else
    echo "Failed to write to baz/qux.md."
fi

if echo 'Emily file cannot be found' 2> ./bar/foo.md; then
    echo "Wrote error message to bar/foo.md."
else
    echo "Failed to write error message to bar/foo.md."
fi

if ls -1 nonexistent 2> ./bar/bar.md; then
    echo "Executed ls command for nonexistent file."
else
    echo "Failed to execute ls command for nonexistent file."
fi

if cat ./baz/banana nonexistent 2> ./bar/qux.md; then
    echo "Executed cat command."
else
    echo "Failed to execute cat command."
fi
