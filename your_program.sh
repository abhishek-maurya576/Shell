#!/bin/bash

# Redirecting stdout (1>) and stderr (2>) correctly
ls -1 /tmp/qux > /tmp/baz/foo.md

echo 'Hello James' > /tmp/baz/qux.md  # Fixed redirection issue

echo 'Emily file cannot be found' 2> /tmp/bar/foo.md

ls -1 nonexistent 2> /tmp/bar/bar.md

cat /tmp/baz/banana nonexistent 2> /tmp/bar/qux.md
