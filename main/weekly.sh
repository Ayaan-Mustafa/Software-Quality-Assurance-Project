# Define the directory containing the text files
DIR="daily_sessions"

# Check if the directory exists to prevent errors
if [ ! -d "$DIR" ]; then
  echo "Error: Directory '$DIR' does not exist."
  exit 1
fi

# Loop through each .txt file in the directory
for file in "$DIR"/*.txt; do
  # Check if the file exists (handles the case where the directory is empty or has no .txt files)
  if [ -f "$file" ]; then
    echo "Running daily.sh for: $file"
    ./daily.sh "$file"
  fi
done

echo "All sessions processed."