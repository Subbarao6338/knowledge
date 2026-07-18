# Windows Batch (.bat / .cmd) Cheatsheet

Batch files run via `cmd.exe`. `.bat` and `.cmd` are functionally almost identical (minor differences in error-level handling in some edge cases) — `.cmd` is generally preferred on modern Windows.

## Basics

```batch
@echo off
:: This is a comment (double colon is the common convention)
REM This is also a comment (classic style)

echo Hello, World!
echo.                     :: prints a blank line

pause                  :: "Press any key to continue..."
exit /b 0                    :: exit script with code 0 (use /b to exit only the script, not the whole cmd session)
```

`@echo off` at the top suppresses each command from being echoed to the console before its output — standard for almost every real script.

## Variables

```batch
set NAME=value
set "NAME=value"           :: quoted form — safer, avoids trailing space issues
echo %NAME%

set /a COUNT=1+2              :: arithmetic assignment
set /a COUNT+=1                  :: increment

set /p USERINPUT=Enter your name:      :: prompt for input, store in USERINPUT
echo Hello, %USERINPUT%

:: Environment variables
echo %USERNAME%
echo %COMPUTERNAME%
echo %PATH%
echo %CD%                  :: current directory
echo %DATE% %TIME%

setx MY_VAR "value"          :: set a PERSISTENT environment variable (new shells only, not current one)

:: Delayed expansion (needed inside loops/blocks where %VAR% is evaluated too early)
setlocal enabledelayedexpansion
set COUNT=0
for %%x in (1 2 3) do (
    set /a COUNT+=1
    echo Count is now: !COUNT!
)
```

## String Operations

```batch
set STR=Hello World
echo %STR:World=Batch%          :: substring replace -> "Hello Batch"
echo %STR:~0,5%                    :: substring: 5 chars starting at index 0 -> "Hello"
echo %STR:~6%                         :: from index 6 to end -> "World"
echo %STR:~-5%                           :: last 5 characters -> "World"
echo %STR:~0,-6%                            :: all but last 6 characters -> "Hello"

:: Concatenation
set A=Hello
set B=World
set C=%A% %B%
```

## Conditionals

```batch
if "%NAME%"=="Subbarao" (
    echo Match found
) else (
    echo No match
)

if exist "file.txt" echo File exists
if not exist "file.txt" echo File does not exist
if exist "C:\some\dir\" echo Directory exists

if "%1"=="" (
    echo No argument provided
    exit /b 1
)

:: Numeric comparisons
if %COUNT% GTR 10 echo Greater than 10
if %COUNT% LSS 10 echo Less than 10
if %COUNT% EQU 10 echo Equal to 10
:: Operators: EQU, NEQ, LSS, LEQ, GTR, GEQ

:: Case-insensitive string comparison
if /i "%NAME%"=="subbarao" echo Case-insensitive match

:: Errorlevel checks (exit code of last command)
if %errorlevel% NEQ 0 (
    echo Previous command failed
    exit /b %errorlevel%
)
if errorlevel 1 echo Command returned 1 or higher
```

## Loops

```batch
:: FOR over a list
for %%f in (a b c) do echo %%f

:: FOR over files matching a pattern
for %%f in (*.txt) do echo %%f
for %%f in (*.txt) do echo Processing: %%f && type "%%f"

:: FOR /R — recursive directory traversal
for /r %%f in (*.log) do echo %%f

:: FOR /D — iterate directories only
for /d %%d in (*) do echo %%d

:: FOR /L — numeric range loop (start, step, end)
for /l %%i in (1,1,10) do echo %%i

:: FOR /F — parse lines from a file or command output
for /f "delims=," %%a in (data.csv) do echo %%a
for /f "tokens=1,2 delims=," %%a in (data.csv) do echo Col1=%%a Col2=%%b
for /f "usebackq tokens=*" %%a in (`dir /b`) do echo %%a

:: In a .bat file, use %%x; at an interactive command prompt, use single %x
```

## Functions (Labels & CALL)

```batch
call :greet "Subbarao"
goto :eof

:greet
echo Hello, %~1
exit /b 0

:: %~1 strips surrounding quotes from the argument; %1 keeps them as-is
```

## Script Arguments

```batch
echo %0          :: script name/path
echo %1 %2 %3       :: positional arguments
echo %*                :: all arguments
echo %~dp0                 :: drive + path of the currently running script (very common pattern)

shift              :: shift all arguments down by one (%2 becomes %1, etc.)

:: Argument modifiers (common ones)
%~f1          :: full path
%~d1             :: drive letter only
%~p1                :: path only, no filename
%~n1                   :: filename without extension
%~x1                      :: extension only
%~s1                         :: short (8.3) path form
```

## File & Directory Operations

```batch
dir                    :: list directory contents
dir /b                    :: bare format (names only)
dir /s                       :: recursive

cd path\to\dir
cd /d D:\other\drive\dir       :: change drive AND directory
mkdir mydir
md mydir                          :: same as mkdir
rmdir mydir
rmdir /s /q mydir                     :: recursive + quiet (no confirmation)

copy file.txt dest\
copy /y file.txt dest\                :: overwrite without prompting
xcopy source\ dest\ /e /i               :: recursive copy including empty dirs
robocopy source\ dest\ /mir                :: modern, robust mirror copy (preferred over xcopy for large jobs)

move file.txt dest\
ren oldname.txt newname.txt
del file.txt
del /q /f *.tmp                    :: quiet, force delete matching pattern

type file.txt              :: print file contents (like cat)
more file.txt                  :: paginated view

attrib +h file.txt            :: set hidden attribute
attrib -h file.txt               :: remove hidden attribute
```

## Redirection & Piping

```batch
command > output.txt          :: stdout to file (overwrite)
command >> output.txt             :: stdout to file (append)
command 2> error.txt                 :: stderr to file
command > output.txt 2>&1               :: both stdout and stderr to file
command < input.txt                        :: stdin from file
command 2>nul                                 :: discard stderr (nul is the Windows equivalent of /dev/null)

command1 | command2         :: pipe
dir | findstr ".txt"            :: find lines matching a pattern (Windows equivalent of grep)
```

## Error Handling

```batch
command
if %errorlevel% neq 0 (
    echo Command failed with code %errorlevel%
    exit /b %errorlevel%
)

:: Chaining based on success/failure
command1 && echo Success || echo Failed
command1 & command2          :: run sequentially regardless of success/failure
```

## Common System Commands

```batch
tasklist                  :: list running processes
tasklist | findstr "python"
taskkill /IM notepad.exe /F      :: force kill by image name
taskkill /PID 1234 /F               :: force kill by PID

systeminfo               :: detailed system info
hostname
whoami
whoami /groups

ipconfig                :: network config
ipconfig /all
ipconfig /flushdns

ping google.com
ping -n 4 google.com

netstat -ano             :: list connections + owning PIDs
netstat -ano | findstr :8080

sc query servicename       :: query a Windows service
sc start servicename
sc stop servicename
net start servicename         :: alternate way to start a service
net stop servicename

schtasks /create /tn "MyTask" /tr "C:\script.bat" /sc daily /st 09:00
schtasks /query /tn "MyTask"
schtasks /delete /tn "MyTask" /f

reg query "HKCU\Software\MyApp"
reg add "HKCU\Software\MyApp" /v MyValue /t REG_SZ /d "data"
reg delete "HKCU\Software\MyApp" /v MyValue /f
```

## Common Script Template

```batch
@echo off
setlocal enabledelayedexpansion

:: Argument check
if "%~1"=="" (
    echo Usage: %~nx0 ^<name^>
    exit /b 1
)

set "NAME=%~1"
set "LOGFILE=%~dp0script.log"

echo [%date% %time%] Starting script for %NAME% >> "%LOGFILE%"

:: Main logic
if exist "input\%NAME%.txt" (
    echo Processing %NAME%...
    :: do work here
) else (
    echo File not found: input\%NAME%.txt
    exit /b 1
)

echo [%date% %time%] Done >> "%LOGFILE%"
endlocal
exit /b 0
```

## Common Gotchas

- `%VAR%` inside a `(...)` block (loops, if-blocks) is expanded **once**, when the block is parsed — not each iteration. Use `setlocal enabledelayedexpansion` and `!VAR!` to get updated values inside loops.
- Special characters (`&`, `|`, `<`, `>`, `^`, `%`) often need escaping with `^` in certain contexts, especially in `echo` or when passed as arguments.
- Batch is NOT case-sensitive for commands, but IS for string comparisons (`if "%A%"=="%B%"`) unless you use `/i`.
- Spaces around `=` in `set VAR = value` become part of the variable name/value — always write `set VAR=value` with no spaces (or use `set "VAR=value"` for safety).
- Batch has extremely limited error handling compared to PowerShell/Bash — `%errorlevel%` reflects the last command's exit code and must be checked immediately, since it can be overwritten by subsequent commands (including `if` itself in some cases).
- Batch scripting is largely legacy — for anything nontrivial on modern Windows, PowerShell (see the PowerShell cheatsheet) is generally preferred for its structured objects, error handling, and richer standard library.
