#!/bin/bash

if [ -d "samples_testing" ]; then
    rm -rf "samples_testing"
fi

if [ -d "samples_original" ]; then
    cp -r "samples_original" "samples_testing"
    echo "OK! (✿ ◠ ‿ ◠)"
else
    echo "Error: 'samples_original' directory does not exist."
    exit 1
fi
