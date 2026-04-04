# Daily script that simulates 1 day of transactions on the banking system
# can be either run with a text file as input or with manual input to the system
# optional command line argument of the file path to the input file

# prompt user for input method
echo "How would you like to provide input to the frontend?"
echo "[f] Use an input file"
echo "[m] Manually provide input in the terminal"
read -p "Enter your choice (f/m): " INPUT_MODE

# execute based on user choice
if [[ "$INPUT_MODE" == "f" || "$INPUT_MODE" == "F" ]]; then
    
    # validate that an input file path was provided
    if [ "$#" -ne 1 ]; then
        echo "Error: You chose file mode but did not provide a file path."
        echo "Usage: $0 <path_to_input_txt_file>"
        exit 1
    fi

    INPUT_FILE="$1"

    # check if provided file exists
    if [ ! -f "$INPUT_FILE" ]; then
        echo "Error: Input file '$INPUT_FILE' does not exist."
        exit 1
    fi

    echo "Starting frontend processing with input file: $INPUT_FILE..."
    python3 frontend/main.py < "$INPUT_FILE"

elif [[ "$INPUT_MODE" == "m" || "$INPUT_MODE" == "M" ]]; then
    
    echo "Starting frontend processing in manual mode..."
    # run python script with manual input
    python3 frontend/main.py

else
    echo "Error: Invalid choice '$INPUT_MODE'. Please run the script again and select 'f' or 'm'."
    exit 1
fi

# check if frontend script executed successfully
if [ $? -ne 0 ]; then
    echo "Error: frontend/main.py encountered an issue. Aborting."
    exit 1
fi

# define directories and generate the timestamped filename
SESSION_DIR="data/session_transactions"
DAILY_DIR="data/daily_transactions"
TIMESTAMP=$(date +"%Y_%m_%d_%H_%M_%S")
MERGED_FILE="${DAILY_DIR}/${TIMESTAMP}_sessions.txt"

# ensure the daily transactions directory exists
mkdir -p "$DAILY_DIR"

# merge all text files into the new daily transaction file
echo "Merging session transaction files..."
if ls ${SESSION_DIR}/*.txt 1> /dev/null 2>&1; then
    cat ${SESSION_DIR}/*.txt > "$MERGED_FILE"
else
    echo "No .txt files found in $SESSION_DIR to merge. Creating an empty daily file."
    touch "$MERGED_FILE"
fi

# clear session_transactions directory
echo "Clearing session transactions..."
rm -f ${SESSION_DIR}/*.txt

# pass newly created merged file to backend/backend.py as a command line argument
echo "Starting backend processing..."
python3 backend/backend.py "$MERGED_FILE"

echo "Workflow complete!"