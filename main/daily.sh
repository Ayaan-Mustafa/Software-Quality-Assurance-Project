#!/bin/bash

# 1. Validate that an input file path was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_input_txt_file>"
    exit 1
fi

INPUT_FILE="$1"

# Check if the provided file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' does not exist."
    exit 1
fi

# 2. Feed the file line-by-line into frontend/main.py as sequential terminal inputs
echo "Starting frontend processing..."
# The '<' operator maps the file to sys.stdin. 
# Each call to input() in main.py will read the next line of the file.
python3 frontend/main.py < "$INPUT_FILE"

# Check if frontend script executed successfully
if [ $? -ne 0 ]; then
    echo "Error: frontend/main.py encountered an issue. Aborting."
    exit 1
fi

# 3. Define directories and generate the timestamped filename
SESSION_DIR="data/session_transactions"
DAILY_DIR="data/daily_transactions"
TIMESTAMP=$(date +"%Y_%m_%d_%H_%M_%S")
MERGED_FILE="${DAILY_DIR}/${TIMESTAMP}_sessions.txt"

# Ensure the daily transactions directory exists
mkdir -p "$DAILY_DIR"

# 4. Merge all text files into the new daily transaction file
echo "Merging session transaction files..."
# Check if there are actually files to merge to prevent cat errors
if ls ${SESSION_DIR}/*.txt 1> /dev/null 2>&1; then
    cat ${SESSION_DIR}/*.txt > "$MERGED_FILE"
else
    echo "No .txt files found in $SESSION_DIR to merge. Creating an empty daily file."
    touch "$MERGED_FILE"
fi

echo "$MERGED_FILE"

# 5. Clear the session_transactions directory
echo "Clearing session transactions..."
rm -f ${SESSION_DIR}/*.txt

# 6. Pass the newly created merged file to backend/backend.py as a command line argument
echo "Starting backend processing..."
python3 backend/backend.py "$MERGED_FILE"

echo "Workflow complete!"