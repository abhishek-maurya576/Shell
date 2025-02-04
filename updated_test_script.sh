#!/bin/bash

# Create directories for output files
mkdir -p ./baz
mkdir -p ./bar

# Redirecting stdout (1>) and stderr (2>) correctly
ls -1 ./baz/foo.md > ./baz/foo.md

echo 'Hello James' > ./baz/qux.md  # Fixed redirection issue

echo 'Emily file cannot be found' 2> ./bar/foo.md

ls -1 nonexistent 2> ./bar/bar.md

cat ./baz/banana nonexistent 2> ./bar/qux.md
