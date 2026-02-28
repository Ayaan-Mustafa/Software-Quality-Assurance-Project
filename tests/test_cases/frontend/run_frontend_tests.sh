#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/tests/test_cases/frontend"
MAIN_DIR="$ROOT_DIR/main"
RESULTS_DIR="$ROOT_DIR/tests/test_results/frontend"
BASELINE_ACCOUNTS="$RESULTS_DIR/accounts_baseline.txt"

UPDATE_EXPECTED=0
if [[ "${1:-}" == "--update-expected" ]]; then
  UPDATE_EXPECTED=1
fi

mkdir -p "$RESULTS_DIR/actual/stdout" "$RESULTS_DIR/actual/atf" "$RESULTS_DIR/reports"

if [[ ! -f "$BASELINE_ACCOUNTS" ]]; then
  cp "$MAIN_DIR/accounts.txt" "$BASELINE_ACCOUNTS"
fi

orig_accounts_backup="$(mktemp)"
cp "$MAIN_DIR/accounts.txt" "$orig_accounts_backup"
cleanup() {
  cp "$orig_accounts_backup" "$MAIN_DIR/accounts.txt"
  rm -f "$orig_accounts_backup"
}
trap cleanup EXIT

SUMMARY_FILE="$RESULTS_DIR/reports/test_summary.txt"

{
  echo "Frontend Test Summary"
  echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
  echo
} > "$SUMMARY_FILE"

normalize_stdout() {
  local src="$1"
  local dst="$2"
  sed -E \
    -e 's#Saved to: .*transactions_[0-9]{4}-[0-9]{2}-[0-9]{2}_[0-9]{2}-[0-9]{2}-[0-9]{2}\.txt#Saved to: <TRANSACTION_FILE>#g' \
    "$src" > "$dst"
}

intention_from_case() {
  local category="$1"
  local case_name="$2"
  local msg="$category case: ${case_name//_/ }"
  echo "$msg"
}

total=0
passed=0
failed=0

while IFS= read -r category_dir; do
  category="$(basename "$category_dir")"
  input_dir="$category_dir/input"

  expected_stdout_dir="$category_dir/expected_output"
  expected_atf_dir="$category_dir/expected_atf"
  mkdir -p "$expected_stdout_dir" "$expected_atf_dir"
  mkdir -p "$RESULTS_DIR/actual/stdout/$category" "$RESULTS_DIR/actual/atf/$category"

  while IFS= read -r input_file; do
    total=$((total + 1))

    input_name="$(basename "$input_file")"
    case_name="${input_name%.in.txt}"
    expected_stdout="$expected_stdout_dir/${case_name}.exp.txt"
    expected_atf="$expected_atf_dir/${case_name}.atf"

    raw_stdout="$RESULTS_DIR/actual/stdout/$category/${case_name}.raw.out.txt"
    norm_stdout="$RESULTS_DIR/actual/stdout/$category/${case_name}.out.txt"
    actual_atf="$RESULTS_DIR/actual/atf/$category/${case_name}.atf"

    cp "$BASELINE_ACCOUNTS" "$MAIN_DIR/accounts.txt"
    rm -f "$MAIN_DIR"/transactions/transactions_*.txt

    temp_input="$(mktemp)"
    cat "$input_file" > "$temp_input"
    printf '\n' >> "$temp_input"

    (
      cd "$MAIN_DIR" || exit 1
      python3 main.py < "$temp_input" > "$raw_stdout" 2>&1
    )
    exit_code=$?
    rm -f "$temp_input"

    normalize_stdout "$raw_stdout" "$norm_stdout"

    latest_atf="$(ls -1t "$MAIN_DIR"/transactions/transactions_*.txt 2>/dev/null | head -n 1)"
    if [[ -n "$latest_atf" ]]; then
      cp "$latest_atf" "$actual_atf"
    else
      : > "$actual_atf"
    fi

    if [[ "$UPDATE_EXPECTED" -eq 1 ]]; then
      cp "$norm_stdout" "$expected_stdout"
      cp "$actual_atf" "$expected_atf"
      echo "[UPDATED] $category/$input_name" | tee -a "$SUMMARY_FILE"
      passed=$((passed + 1))
      continue
    fi

    stdout_ok=0
    atf_ok=0

    if [[ -f "$expected_stdout" ]] && diff -u "$expected_stdout" "$norm_stdout" > "$RESULTS_DIR/reports/${category}_${case_name}.stdout.diff"; then
      stdout_ok=1
    fi

    if [[ -f "$expected_atf" ]] && diff -u "$expected_atf" "$actual_atf" > "$RESULTS_DIR/reports/${category}_${case_name}.atf.diff"; then
      atf_ok=1
    fi

    if [[ "$stdout_ok" -eq 1 && "$atf_ok" -eq 1 ]]; then
      echo "[PASS] $category/$input_name" | tee -a "$SUMMARY_FILE"
      passed=$((passed + 1))
      rm -f "$RESULTS_DIR/reports/${category}_${case_name}.stdout.diff" "$RESULTS_DIR/reports/${category}_${case_name}.atf.diff"
    else
      echo "[FAIL] $category/$input_name" | tee -a "$SUMMARY_FILE"
      failed=$((failed + 1))

      reason=""
      if [[ "$stdout_ok" -eq 0 && "$atf_ok" -eq 0 ]]; then
        reason="terminal output and transaction file differ"
      elif [[ "$stdout_ok" -eq 0 ]]; then
        reason="terminal output differs"
      else
        reason="transaction file differs"
      fi

      intention="$(intention_from_case "$category" "$case_name")"
      echo "[FAILURE] $category/$input_name :: $intention :: $reason" >> "$SUMMARY_FILE"
    fi

  done < <(find "$input_dir" -maxdepth 1 -type f -name '*.in.txt' | sort)
done < <(find "$FRONTEND_DIR" -mindepth 1 -maxdepth 1 -type d | sort)

echo >> "$SUMMARY_FILE"
echo "Totals: $passed / $total passed, $failed failed" | tee -a "$SUMMARY_FILE"

echo
if [[ "$UPDATE_EXPECTED" -eq 1 ]]; then
  echo "Expected outputs refreshed for all tests under tests/test_cases/frontend."
else
  echo "Summary: $passed / $total passed, $failed failed"
  echo "Summary report: $SUMMARY_FILE"
fi
