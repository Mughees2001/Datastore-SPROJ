#!/bin/bash

TESTCOMMAND="python3 test_master.py"


for j in $(seq 16 1 1500)
do
echo "Creating directory $j"
mkdir log/$j

for i in $(seq 10 10 100)
do
    # echo "Running test case $i"
    # Run the test cases
    $TESTCOMMAND $i $j
done
echo "Done with directory $j"
done
