# Frontend Failure Log

| Test Name | What was being tested | Nature of failure | Code/Test error cause | Actions taken to fix |
|---|---|---|---|---|
| `paybill` menu dispatch | Paybill operation routing | Paybill path not executed from main menu | `main_menu` used `self.paybill` instead of `self.paybill()` | Updated [atm_class.py](/Users/aaron/Documents/softwareQualityAssurance/Software-Quality-Assurance-Project/main/atm_class.py) to call `self.paybill()` |
| `withdraw` invalid amount handling | Withdraw robustness on malformed amounts | Runtime crash (`ValueError`) on non-integer amount input | Direct `int(input(...))` conversion without validation loop | Refactored withdraw to use `_validate_positive_int()` loop and retry safely in [atm_class.py](/Users/aaron/Documents/softwareQualityAssurance/Software-Quality-Assurance-Project/main/atm_class.py) |
| Multiple frontend tests | Input/output consistency | `Traceback`/`EOFError` captured as expected output | Legacy/incomplete input streams ended before clean logout | Rewrote affected `.in.txt` files to complete valid sessions ending with `q` then `y`; regenerated expected outputs |
| `login`, `paybill`, `transfer`, `withdrawl`, `delete` legacy cases | Requirements test realism | Expected outputs included repeated invalid admin prompt errors | Old command-style test inputs (e.g., `login user1...`) and inline notes were interpreted as raw prompt answers | Converted legacy command-style files to real interactive token streams matching ATM prompts |
| Frontend suite naming | Test organization and pairing | Non-standard filename/directory conventions (`output/`, mixed extensions) | Mixed historical naming patterns | Standardized to `input/<case>.in.txt`, `expected_output/<case>.exp.txt`, `expected_atf/<case>.atf`; runner now enforces strict basename pairing |
| Failure log readability | Reporting completeness | Empty-looking failure table when all tests passed | Log only emitted rows for failed tests | Added explicit “No failures observed” row and preserved resolved-change history in this file |

