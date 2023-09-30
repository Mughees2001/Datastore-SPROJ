#!/bin/bash

TESTCOMMAND="python3 test_master.py"

# Run the test cases 100 times
for i in $(seq 1010 10 5000)
do
    echo "Running test case $i"
    # Run the test cases
    $TESTCOMMAND $i
done
