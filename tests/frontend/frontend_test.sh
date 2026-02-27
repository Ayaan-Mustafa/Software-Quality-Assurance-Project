#!/bin/bash

# --- Color Variables ---
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color (Reset)

# Define your files, directories, and limits
PYTHON_FILE="../main/main.py"
TARGET_DIR="input"       
OUTPUT_DIR="output"
EXPECTED_DIR="expected"
RESULT_DIR="results"
ERROR_DIR="errors"
ERROR_LOG="$ERROR_DIR/errors.log"
SUMMARY_FILE="summary.txt"
TIMEOUT_SEC=10  

# Initialize our summary counters
SUCCESS_COUNT=0
FAIL_COUNT=0

# First, check if the Python script actually exists
if [ ! -f "$PYTHON_FILE" ]; then
    echo -e "${RED}Error: $PYTHON_FILE not found.${NC}"
    exit 1
fi

# Create all necessary directories safely
mkdir -p "$OUTPUT_DIR" "$ERROR_DIR" "$RESULT_DIR"

# Clear the error log and initialize the summary file
> "$ERROR_LOG"
echo "Test Suite Summary - $(date +"%Y-%m-%d %H:%M:%S")" > "$SUMMARY_FILE"
echo "Arguments passed to Python: $@" >> "$SUMMARY_FILE" # Log the arguments!
echo "=========================================" >> "$SUMMARY_FILE"
echo "Failed Tests:" >> "$SUMMARY_FILE"

echo "Scanning for .txt files recursively in '$TARGET_DIR'..."
echo "Running '$PYTHON_FILE' with arguments: '$@'"
echo "========================================="

# Find all .txt files recursively and pipe them into a while loop
while IFS= read -r INPUT_FILE; do
    
    REL_PATH="${INPUT_FILE#$TARGET_DIR/}"
    OUTPUT_FILE="$OUTPUT_DIR/$REL_PATH"
    EXPECTED_FILE="$EXPECTED_DIR/$REL_PATH"
    RESULT_FILE="$RESULT_DIR/$REL_PATH"
    
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    mkdir -p "$(dirname "$RESULT_FILE")"
    
    TEMP_ERR="temp_err.txt"  
    
    echo "Processing: $REL_PATH"
    
    # Forward all shell arguments ("$@") directly to the Python script
    timeout "$TIMEOUT_SEC" python3 "$PYTHON_FILE" "$@" < "$INPUT_FILE" > "$OUTPUT_FILE" 2> "$TEMP_ERR"
    EXIT_CODE=$?
    
    # 1. Check for Timeout
    if [ $EXIT_CODE -eq 124 ]; then
        echo "[$TIMESTAMP] TIMEOUT: Processing '$INPUT_FILE' exceeded $TIMEOUT_SEC seconds." >> "$ERROR_LOG"
        echo "---------------------------------------------------" >> "$ERROR_LOG"
        echo -e "  -> ${RED}Error: Timed out!${NC}"
        echo "- $REL_PATH (Timeout after ${TIMEOUT_SEC}s)" >> "$SUMMARY_FILE"
        ((FAIL_COUNT++))
        
    # 2. Check for normal Python execution errors
    elif [ -s "$TEMP_ERR" ] || [ $EXIT_CODE -ne 0 ]; then
        TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
        echo "[$TIMESTAMP] Error processing file: $INPUT_FILE" >> "$ERROR_LOG"
        cat "$TEMP_ERR" >> "$ERROR_LOG"
        echo "---------------------------------------------------" >> "$ERROR_LOG"
        echo -e "  -> ${RED}Warning: Python script crashed! Logged.${NC}"
        echo "- $REL_PATH (Python Crash)" >> "$SUMMARY_FILE"
        ((FAIL_COUNT++))
        
    # Python succeeded, now compare against the expected output
    else
        # 3. Check if the expected file is missing
        if [ ! -f "$EXPECTED_FILE" ]; then
            echo -e "  -> ${RED}Warning: Expected file missing! Cannot verify.${NC}"
            echo "- $REL_PATH (Missing Expected File)" >> "$SUMMARY_FILE"
            ((FAIL_COUNT++))
            
        else
            # 4. Compare the files
            diff -u "$EXPECTED_FILE" "$OUTPUT_FILE" > "$RESULT_FILE"
            DIFF_STATUS=$?
            
            if [ $DIFF_STATUS -eq 0 ]; then
                echo -e "  -> ${GREEN}PASS: Output matches expected perfectly.${NC}"
                ((SUCCESS_COUNT++))
                rm -f "$RESULT_FILE" 
            else
                echo -e "  -> ${RED}FAIL: Output differs from expected.${NC}"
                echo "- $REL_PATH (Output Mismatch)" >> "$SUMMARY_FILE"
                ((FAIL_COUNT++))
            fi
        fi
    fi
    
    rm -f "$TEMP_ERR"
    
done < <(find "$TARGET_DIR" -type f -name "*.txt")

if [ $FAIL_COUNT -eq 0 ]; then
    echo "(None! All tests passed perfectly.)" >> "$SUMMARY_FILE"
fi

echo "=========================================" >> "$SUMMARY_FILE"
echo "Tests Passed: $SUCCESS_COUNT" >> "$SUMMARY_FILE"
echo "Tests Failed: $FAIL_COUNT" >> "$SUMMARY_FILE"

# Print the final summary to the terminal
echo "========================================="
echo "Test Suite Completed!"
echo -e "${GREEN}Passed: $SUCCESS_COUNT${NC} | ${RED}Failed: $FAIL_COUNT${NC}"
echo "A full report has been saved to '$SUMMARY_FILE'."
echo "========================================="