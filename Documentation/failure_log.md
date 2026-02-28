# Frontend Failure Log

| Test Name | What was being tested | Nature of failure | Code/Test error cause | Actions taken to fix |
|---|---|---|---|---|
| `paybill` menu dispatch | Paybill operation routing | Paybill path not executed from main menu | `main_menu` used `self.paybill` instead of `self.paybill()` | Updated atm_class.py to call `self.paybill()` |
| `withdraw` invalid amount handling | Withdraw robustness on malformed amounts | Runtime crash (`ValueError`) on non-integer amount input | Direct `int(input(...))` conversion without validation loop | Refactored withdraw to use `_validate_positive_int()` loop and retry in atm_class.py |
| Frontend suite naming | Test organization and pairing | Fixed non-standard naming conventions in testing directories. | Mixed naming patterns | Standardized to `input/<case>.in.txt`, `expected_output/<case>.exp.txt`, `expected_atf/<case>.atf`; runner enforces the basename patterns |

