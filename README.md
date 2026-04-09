# Software-Quality-Assurance-Project

Aaron James, Ayaan Mustafa, Arad Ayntabli

|Name|Student ID|
|:-:|:-:
|Aaron James | 100830371|
|Ayaan Mustafa | 100871665|
|Arad Ayntabli | 100845722 |

## Phase 1

Test Plan and list of test cases can be found in **/Documentation**

Example input and output files can be found in **/tests**

## Phase 2

First version of our source code can be found in **/main**

Design Document can be found in **/Documentation**

UML diagram is in the Design Document

## Phase 3 

test results found in **/tests/test_results/frontend/reports/Test_summary.txt**

Failure Log in **/Documentation**

Script for the front end tests is under **/tests/test_cases/frontend/run_frontend_tests.sh**

## Phase 4

First version of the Backend source code found in **main/backend**

Backend design documnet can be found in **Documentation**

Backend UML diagram can be found in **UML_diagram**

## Phase 5

White box unit testing was done for both the `read_transactions()` and `perform_transactions()` methods in the Backend Classs in main/backend/backend.py. Statement coverage was done on `read_transactions()` and decision and loop coverage was done for `perform_transactions()`.

The unit tests for `read_transactions()` can be found in **tests/test_cases/backend/read_transactions**.

The unit tests for `perform_transactions()` can be found in **test/test_cases/backend/perform_transactions**.

Each directory has a read.md file that outlines what each test aims to achieve and run instructions

The failure log can be found in the **Documentation** directory in the `Phase  5 - Back End Unit Testing.pdf` file


## Phase 6

The Phase 6 shell scripts are found in **main/daily.sh** and **main/weekly.sh**.

The daily session input files used for the weekly simulation can be found in **main/daily_sessions**.

The daily session input file descriptions can be found under **Documentation/** in a file "Phase 6 - Integration & Delivery.pdf"

Before running the scripts, navigate to the **main** directory.

The Front End and Back End are run as separate programs through the shell scripts, and the session transaction files are written to and read from the **data** directory.

For the Daily script:

- run `./daily.sh` to provide transaction input through the terminal
- run `./daily.sh daily_sessions/<file_name>.txt` to execute a day using a prepared session input file
- the script runs the Front End, saves the individual session transaction files, merges them into a daily transaction file, and then runs the Back End on the merged file

For the Weekly script:

- run `./weekly.sh`
- the script is set up to run the Daily script seven times using the session files in **main/daily_sessions**
- each day simulates one day of banking activity using a different transaction session file
