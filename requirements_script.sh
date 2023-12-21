#!/bin/bash

REQUIREMENTS_FILE="requirements.txt"

while IFS= read -r line; do
    pip install "$line" > /dev/null 2>&1

    if [ $? -ne 0 ]; then
        echo "Failed to install: $line"
    fi
done < "$REQUIREMENTS_FILE"

# Note: This version, the > /dev/null 2>&1 redirects both standard output and standard error to /dev/null, effectively suppressing the error message from the failed installation. Instead, it just prints a message indicating which dependency failed.