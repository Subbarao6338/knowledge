# Shell Scripting Cheatsheet (.sh / Bash)

## Script Basics

```bash
#!/bin/bash
# Shebang — tells the OS which interpreter to use. Common alternatives:
#!/bin/sh          # POSIX sh — more portable, fewer features than bash
#!/usr/bin/env bash    # portable way to find bash on PATH

chmod +x script.sh        # make executable
./script.sh                  # run it
bash script.sh                  # or run explicitly with the interpreter
```

## Safe Script Header (recommended defaults)

```bash
#!/bin/bash
set -euo pipefail
# -e: exit immediately if any command fails
# -u: error on use of an unset variable
# -o pipefail: a pipeline fails if ANY command in it fails, not just the last one
IFS=$'\n\t'    # safer word-splitting default (avoids issues with spaces in filenames)
```

## Variables

```bash
NAME="value"                # no spaces around =
echo "$NAME"                    # always quote variable expansions
echo "${NAME}"                     # braces disambiguate: "${NAME}_suffix"
readonly CONST="fixed"                # cannot be reassigned
unset NAME                               # remove a variable

# Default values
echo "${VAR:-default}"        # use "default" if VAR is unset or empty (doesn't set VAR)
echo "${VAR:=default}"           # same, but ALSO assigns VAR=default
echo "${VAR:+alt}"                  # use "alt" only if VAR IS set
echo "${VAR:?error message}"           # error out with message if VAR is unset

# String length / substring
echo "${#NAME}"                # length of string
echo "${NAME:0:3}"                # substring: 3 chars starting at index 0
echo "${NAME: -3}"                   # last 3 characters (space before - is required)

# Search and replace
echo "${NAME/old/new}"        # replace first match
echo "${NAME//old/new}"          # replace all matches
echo "${NAME#prefix}"               # strip shortest matching prefix
echo "${NAME##prefix}"                 # strip longest matching prefix
echo "${NAME%suffix}"                     # strip shortest matching suffix
echo "${NAME%%suffix}"                       # strip longest matching suffix

echo "${NAME^^}"          # uppercase
echo "${NAME,,}"             # lowercase
```

## Command Substitution & Arithmetic

```bash
RESULT=$(command)             # preferred syntax
RESULT=`command`                 # legacy backtick syntax

COUNT=$((1 + 2))             # arithmetic expansion
COUNT=$((COUNT + 1))
((COUNT++))                     # increment
let COUNT=COUNT+1                  # alternate arithmetic syntax

echo $(( 10 / 3 ))          # integer division -> 3
echo $(( 10 % 3 ))             # modulo -> 1
echo $(( 2 ** 8 ))                # exponent -> 256

bc <<< "10 / 3"              # floating point math (bash has none natively)
python3 -c "print(10/3)"        # alternative for float math
```

## Arrays

```bash
ARR=(apple banana cherry)
ARR[3]="date"
echo "${ARR[0]}"                # first element
echo "${ARR[@]}"                    # all elements
echo "${ARR[*]}"                       # all elements as a single string
echo "${#ARR[@]}"                         # number of elements
echo "${!ARR[@]}"                            # list of indices

for item in "${ARR[@]}"; do
    echo "$item"
done

ARR+=("elderberry")            # append
unset 'ARR[1]'                    # remove an element (leaves a gap)

# Associative arrays (bash 4+)
declare -A MAP
MAP[key1]="value1"
MAP[key2]="value2"
echo "${MAP[key1]}"
for key in "${!MAP[@]}"; do
    echo "$key = ${MAP[$key]}"
done
```

## Conditionals

```bash
if [ "$a" == "$b" ]; then
    echo "equal"
elif [ "$a" -gt "$b" ]; then
    echo "a > b"
else
    echo "a < b"
fi

# [[ ]] is bash-specific, safer than [ ] (no word-splitting/glob issues, supports && || directly)
if [[ "$a" == "$b" && "$c" == "$d" ]]; then
    echo "both match"
fi

# String tests
[[ -z "$var" ]]        # true if empty
[[ -n "$var" ]]           # true if non-empty
[[ "$str" == pattern* ]]     # glob pattern match (only inside [[ ]])
[[ "$str" =~ ^[0-9]+$ ]]        # regex match (only inside [[ ]])

# Numeric tests: -eq -ne -gt -ge -lt -le
[[ "$a" -eq "$b" ]]

# File tests
[[ -f "$file" ]]        # regular file exists
[[ -d "$dir" ]]            # directory exists
[[ -e "$path" ]]              # exists (any type)
[[ -r "$file" ]]                 # readable
[[ -w "$file" ]]                    # writable
[[ -x "$file" ]]                       # executable
[[ -s "$file" ]]                          # exists and is non-empty
[[ -L "$file" ]]                             # is a symlink

# Combine conditions
[[ -f "$file" && -r "$file" ]]
[[ "$a" == "1" || "$a" == "2" ]]

# Ternary-like pattern
result=$([[ "$a" -gt 5 ]] && echo "big" || echo "small")

# case statement
case "$1" in
    start)
        echo "starting"
        ;;
    stop|halt)
        echo "stopping"
        ;;
    *)
        echo "unknown command"
        ;;
esac
```

## Loops

```bash
for i in 1 2 3 4 5; do
    echo "$i"
done

for i in {1..10}; do
    echo "$i"
done

for i in {0..20..5}; do        # start..end..step
    echo "$i"
done

for f in *.txt; do
    echo "$f"
done

for ((i = 0; i < 10; i++)); do
    echo "$i"
done

while [[ $count -lt 10 ]]; do
    echo "$count"
    ((count++))
done

until [[ $count -ge 10 ]]; do
    echo "$count"
    ((count++))
done

while read -r line; do
    echo "$line"
done < file.txt

while IFS=',' read -r col1 col2 col3; do    # parse CSV-like lines
    echo "$col1 | $col2 | $col3"
done < data.csv

for i in {1..100}; do
    [[ $i -eq 50 ]] && break
    [[ $((i % 2)) -eq 0 ]] && continue
    echo "$i"
done
```

## Functions

```bash
greet() {
    local name="$1"           # always use `local` for function-scoped variables
    echo "Hello, $name!"
}
greet "World"

function greet2 {              # alternate syntax
    echo "Hi, $1"
}

# Return values: functions "return" an exit code (0-255), not data
is_even() {
    local n="$1"
    return $(( n % 2 == 0 ? 0 : 1 ))
}
if is_even 4; then echo "even"; fi

# For actual data return, echo it and capture with command substitution
get_greeting() {
    echo "Hello, $1"
}
MSG=$(get_greeting "World")

# Default parameter pattern
greet_or_default() {
    local name="${1:-Guest}"
    echo "Hello, $name"
}
```

## Positional Parameters & Arguments

```bash
echo "$0"                # script name
echo "$1" "$2"               # first, second argument
echo "$#"                       # number of arguments
echo "$@"                          # all arguments, each quoted separately (preferred)
echo "$*"                             # all arguments as a single string
echo "$?"                                # exit code of last command

shift               # discard $1, shift all args down by one
shift 2                 # discard first two

# Argument parsing with getopts
while getopts "n:v" opt; do
    case $opt in
        n) NAME="$OPTARG" ;;
        v) VERBOSE=true ;;
        \?) echo "Invalid option: -$OPTARG"; exit 1 ;;
    esac
done
shift $((OPTIND - 1))          # remove parsed options, leaving positional args

# Simple manual long-option parsing
while [[ $# -gt 0 ]]; do
    case "$1" in
        --name) NAME="$2"; shift 2 ;;
        --verbose) VERBOSE=true; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done
```

## Input / Output & Redirection

```bash
read -r input                 # read a line into $input
read -r -p "Enter name: " name    # prompt + read
read -rs -p "Password: " pw          # silent (no echo) input

echo "text"
echo -n "no newline"
echo -e "line1\nline2"          # interpret escape sequences
printf "%s is %d years old\n" "$name" "$age"

command > file.txt          # stdout to file
command >> file.txt            # append
command 2> err.txt                # stderr to file
command &> all.txt                   # both stdout+stderr
command < input.txt                     # stdin from file
command 2>&1 | tee log.txt                 # merge stderr into stdout AND display + save

exec 3< file.txt                    # open a custom file descriptor for reading
while read -r line <&3; do echo "$line"; done
exec 3<&-                                # close it
```

## Error Handling

```bash
set -e            # exit on any error
command || echo "command failed, but continuing"     # handle a specific failure without exiting
command || { echo "failed"; exit 1; }

trap 'echo "Error on line $LINENO"' ERR
trap 'cleanup' EXIT              # always run cleanup, success or failure
trap 'echo "Interrupted"; exit 1' INT TERM

cleanup() {
    rm -f "$TMPFILE"
}
trap cleanup EXIT

# Check a command's exit code explicitly
if ! command; then
    echo "command failed with code $?"
    exit 1
fi
```

## Working with Files & Temp Files

```bash
TMPFILE=$(mktemp)
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPFILE" "$TMPDIR"' EXIT

if [[ -f "$file" ]]; then
    echo "exists"
fi

# Read a file into a variable
CONTENT=$(<file.txt)
CONTENT=$(cat file.txt)

# Read a file into an array, line by line
mapfile -t LINES < file.txt
readarray -t LINES < file.txt        # same as mapfile
```

## Here-Documents & Here-Strings

```bash
cat << EOF
Multi-line text
with $VARIABLE expansion
EOF

cat << 'EOF'                 # quoting the delimiter disables variable expansion
Literal $VARIABLE, not expanded
EOF

cat <<- EOF                 # the - allows the closing EOF to be indented (leading TABS stripped)
	indented text
	EOF

grep "pattern" <<< "$VARIABLE"    # here-string — feed a variable as stdin
```

## Debugging

```bash
bash -x script.sh          # trace every command as it executes
set -x                          # enable tracing mid-script
set +x                             # disable tracing

bash -n script.sh              # syntax check only, don't execute

shellcheck script.sh              # static analysis tool — catches common bugs (install separately)
```

## Useful Built-ins & Idioms

```bash
type command             # is it a builtin, alias, function, or binary?
command -v mytool           # check if a command exists (portable)
if command -v docker &> /dev/null; then
    echo "docker is installed"
fi

basename "$path"      # strip directory + optionally extension
dirname "$path"           # get containing directory
$(dirname "$0")               # directory the running script lives in

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)   # robust script-dir resolution

sleep 5                # pause 5 seconds
date +%Y-%m-%d              # formatted date
date -d "+1 day" +%Y-%m-%d      # date arithmetic (GNU date)

xargs -P4 -I{} command {}    # run in parallel, 4 at a time

# Idempotent directory creation
[[ -d "$DIR" ]] || mkdir -p "$DIR"

# Check running as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi
```

## Script Template (production-ready starting point)

```bash
#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LOG_FILE="/tmp/$(basename "$0").log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cleanup() {
    log "Cleaning up..."
    # remove temp files, etc.
}
trap cleanup EXIT
trap 'log "Error on line $LINENO"; exit 1' ERR

usage() {
    echo "Usage: $0 [-v] [-n NAME]"
    exit 1
}

VERBOSE=false
while getopts "vn:h" opt; do
    case $opt in
        v) VERBOSE=true ;;
        n) NAME="$OPTARG" ;;
        h) usage ;;
        \?) usage ;;
    esac
done

log "Starting script with NAME=${NAME:-unset}"
# ... main logic here ...
log "Done"
```

## Common Gotchas

- Always quote variable expansions (`"$var"`, not `$var`) — unquoted variables undergo word-splitting and glob expansion, breaking on filenames/values with spaces.
- `[ ]` vs `[[ ]]`: `[[ ]]` is bash-only but safer (no need to quote as carefully, supports `&&`/`||`/regex directly); `[ ]` is POSIX-portable but stricter about quoting.
- `$(command)` is preferred over backticks — nests cleanly and is more readable.
- Assigning a command's output with trailing/leading whitespace can produce surprises — `$()` strips trailing newlines but not all whitespace.
- Arithmetic context `$(( ))` doesn't need `$` before variable names inside it (`$((count + 1))` works even though `count` isn't prefixed).
- A `local` variable inside a function only applies if declared separately from an assignment that uses command substitution — `local var=$(cmd)` masks the command's exit code; split into `local var; var=$(cmd)` when you need `$?` from `cmd`.
- `set -e` doesn't trigger inside conditionals (`if command; then`), inside `&&`/`||` chains, or inside functions called within a condition — it's a common source of "why didn't set -e catch this."
