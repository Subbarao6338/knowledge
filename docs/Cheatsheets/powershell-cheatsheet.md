# PowerShell Cheatsheet (.ps1)

PowerShell is object-oriented, not text-oriented — commands (cmdlets) pass structured .NET objects through the pipeline, not plain text.

## Basics

```powershell
# This is a comment
<#
Multi-line
comment block
#>

Write-Host "Hello, World!"           # prints directly to console
Write-Output "Hello"                    # sends to the pipeline (preferred for actual output/return values)
Write-Verbose "detail message"             # only shown if -Verbose is passed
Write-Warning "a warning"                     # yellow warning text
Write-Error "an error"                           # writes to error stream

# Running a script
.\script.ps1
powershell.exe -File script.ps1
powershell.exe -ExecutionPolicy Bypass -File script.ps1

Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser     # allow local scripts to run
```

## Variables & Types

```powershell
$name = "Subbarao"
$age = 30
$pi = 3.14
$isActive = $true
$nothing = $null

Write-Host "$name is $age years old"       # string interpolation inside double quotes
Write-Host '$name literal, no interpolation'   # single quotes: no interpolation

$name.GetType()               # show the .NET type
[int]"42"                        # explicit cast
[string]42
[datetime]"2026-07-17"

$env:PATH                  # environment variable
$env:MY_VAR = "value"

# Variable scopes
$global:MyVar = "global"
$script:MyVar = "script-scoped"
$local:MyVar = "local"

# Constants / read-only
Set-Variable -Name PI -Value 3.14159 -Option Constant
```

## Arrays & Hashtables

```powershell
$arr = @(1, 2, 3, 4)
$arr = 1, 2, 3, 4                # parens optional
$arr[0]                              # first element
$arr[-1]                                # last element
$arr[1..3]                                 # slice
$arr.Count                                    # length
$arr += 5                                        # append (creates a new array under the hood)

foreach ($item in $arr) { Write-Host $item }

$hash = @{ Name = "Subbarao"; Age = 30 }
$hash["Name"]
$hash.Name                         # dot access also works
$hash["City"] = "Berlin"              # add/update
$hash.Keys
$hash.Values
$hash.Remove("City")
foreach ($key in $hash.Keys) { Write-Host "$key = $($hash[$key])" }

# Ordered hashtable (preserves insertion order)
$ordered = [ordered]@{ First = 1; Second = 2 }

# Custom objects
$person = [PSCustomObject]@{
    Name = "Subbarao"
    Age  = 30
}
$person.Name
```

## Conditionals

```powershell
if ($age -gt 18) {
    Write-Host "Adult"
} elseif ($age -eq 18) {
    Write-Host "Just turned 18"
} else {
    Write-Host "Minor"
}

switch ($status) {
    "active"   { Write-Host "Running" }
    "stopped"  { Write-Host "Not running" }
    default    { Write-Host "Unknown" }
}

switch -Regex ($value) {
    "^\d+$" { Write-Host "All digits" }
}
```

**Comparison operators** (note: `-eq` not `==`): `-eq`, `-ne`, `-gt`, `-ge`, `-lt`, `-le`, `-like` (wildcard), `-notlike`, `-match` (regex), `-notmatch`, `-contains`, `-notcontains`, `-in`, `-notin`.

**Logical operators:** `-and`, `-or`, `-not` / `!`, `-xor`.

```powershell
if (Test-Path "C:\file.txt") { Write-Host "exists" }
if (-not (Test-Path "C:\file.txt")) { Write-Host "missing" }
if ($name -like "Sub*") { Write-Host "matches wildcard" }
if ($name -match "^\w+$") { Write-Host "matches regex" }
```

## Loops

```powershell
for ($i = 0; $i -lt 10; $i++) {
    Write-Host $i
}

foreach ($item in $arr) {
    Write-Host $item
}

$arr | ForEach-Object { Write-Host $_ }         # $_ = current pipeline item
$arr | ForEach-Object -Parallel { Write-Host $_ } -ThrottleLimit 5    # PowerShell 7+, parallel execution

$i = 0
while ($i -lt 10) {
    Write-Host $i
    $i++
}

do {
    Write-Host $i
    $i++
} while ($i -lt 10)

do { $i++ } until ($i -ge 10)

foreach ($f in Get-ChildItem *.txt) {
    Write-Host $f.Name
    if ($f.Name -eq "stop.txt") { break }
    if ($f.Length -eq 0) { continue }
}
```

## Functions

```powershell
function Greet {
    param(
        [string]$Name = "World",
        [switch]$Loud
    )
    $message = "Hello, $Name!"
    if ($Loud) { $message = $message.ToUpper() }
    return $message
}

Greet -Name "Subbarao"
Greet -Name "Subbarao" -Loud
Greet                          # uses default

# Advanced function with typed, validated parameters
function New-User {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$Username,

        [Parameter(Mandatory = $false)]
        [ValidateRange(0, 150)]
        [int]$Age = 0,

        [ValidateSet("Admin", "User", "Guest")]
        [string]$Role = "User"
    )
    Write-Verbose "Creating user $Username"
    [PSCustomObject]@{ Username = $Username; Age = $Age; Role = $Role }
}

New-User -Username "srao" -Age 30 -Role Admin -Verbose

# Pipeline-aware function
function Process-Item {
    param(
        [Parameter(ValueFromPipeline = $true)]
        [string]$Item
    )
    process {
        Write-Host "Processing: $Item"
    }
}
"a", "b", "c" | Process-Item
```

## The Pipeline

```powershell
Get-Process | Where-Object { $_.CPU -gt 100 }
Get-Process | Sort-Object CPU -Descending
Get-Process | Select-Object -First 5
Get-Process | Select-Object Name, CPU, Id
Get-Process | ForEach-Object { $_.Name }
Get-Process | Measure-Object CPU -Sum -Average
Get-ChildItem *.log | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | Remove-Item

# Aliases for common pipeline cmdlets: ? = Where-Object, % = ForEach-Object, select = Select-Object
Get-Process | ? { $_.CPU -gt 100 } | % { $_.Name }

# Group and count
Get-ChildItem | Group-Object Extension | Sort-Object Count -Descending
```

## Error Handling

```powershell
try {
    Get-Item "C:\doesnotexist.txt" -ErrorAction Stop
} catch {
    Write-Host "Error: $($_.Exception.Message)"
} finally {
    Write-Host "Cleanup runs regardless"
}

# ErrorAction options: Continue (default), Stop, SilentlyContinue, Inquire
Get-Item "missing.txt" -ErrorAction SilentlyContinue
Get-Item "missing.txt" -ErrorAction Stop

$ErrorActionPreference = "Stop"    # make ALL cmdlets treat errors as terminating, script-wide

# Custom errors
throw "Something went wrong"
try { throw [System.InvalidOperationException]::new("bad state") }
catch [System.InvalidOperationException] { Write-Host "Caught: $_" }

# Check the last command's success
if ($?) { Write-Host "Last command succeeded" }
$LASTEXITCODE           # exit code from the last native (non-PowerShell) executable
```

## File & Directory Operations

```powershell
Get-ChildItem                    # ls / dir
Get-ChildItem -Recurse -Filter *.txt
Get-ChildItem -Path C:\logs -File
Get-ChildItem -Path C:\ -Directory

New-Item -ItemType Directory -Path "mydir"
New-Item -ItemType File -Path "file.txt"
Remove-Item "file.txt"
Remove-Item "mydir" -Recurse -Force
Copy-Item "source.txt" "dest.txt"
Copy-Item "sourcedir" "destdir" -Recurse
Move-Item "old.txt" "new.txt"
Rename-Item "old.txt" "new.txt"
Test-Path "file.txt"                # true/false existence check

Get-Content "file.txt"
Get-Content "file.txt" -Tail 10          # last 10 lines
Get-Content "file.txt" -Wait                # like tail -f
Set-Content "file.txt" "content"
Add-Content "file.txt" "more content"          # append

Select-String -Path "*.log" -Pattern "ERROR"      # like grep
(Get-Content file.txt) -replace "old", "new" | Set-Content file.txt

Get-Item "file.txt" | Select-Object Name, Length, LastWriteTime
```

## Process & Service Management

```powershell
Get-Process
Get-Process | Where-Object { $_.CPU -gt 50 }
Get-Process -Name notepad
Stop-Process -Name notepad
Stop-Process -Id 1234 -Force
Start-Process notepad.exe
Start-Process "script.ps1" -Verb RunAs      # run elevated (UAC prompt)

Get-Service
Get-Service -Name "wuauserv"
Start-Service -Name "wuauserv"
Stop-Service -Name "wuauserv"
Restart-Service -Name "wuauserv"

Get-Job                     # background jobs
Start-Job -ScriptBlock { Get-Process }
Receive-Job -Id 1
Wait-Job -Id 1
Remove-Job -Id 1
```

## Networking

```powershell
Test-Connection google.com               # like ping
Test-NetConnection google.com -Port 443       # test a specific port

Invoke-WebRequest -Uri "https://api.example.com"
Invoke-RestMethod -Uri "https://api.example.com/data" -Method Get
Invoke-RestMethod -Uri "https://api.example.com/data" -Method Post -Body $jsonBody -ContentType "application/json"

Get-NetIPAddress
Get-NetAdapter
Resolve-DnsName example.com

Invoke-WebRequest -Uri "https://example.com/file.zip" -OutFile "file.zip"
```

## Working with JSON / CSV / XML

```powershell
$data = Get-Content "data.json" | ConvertFrom-Json
$data.name

$json = $obj | ConvertTo-Json -Depth 10
$obj | ConvertTo-Json | Set-Content "out.json"

Import-Csv "data.csv" | ForEach-Object { Write-Host $_.Name }
$data | Export-Csv "out.csv" -NoTypeInformation

[xml]$xml = Get-Content "data.xml"
$xml.root.item

Invoke-RestMethod "https://api.example.com/data" | ConvertTo-Json -Depth 5
```

## Registry, Environment, and System Info

```powershell
Get-ItemProperty -Path "HKCU:\Software\MyApp"
New-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting" -Value "1"
Set-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting" -Value "2"
Remove-ItemProperty -Path "HKCU:\Software\MyApp" -Name "Setting"

Get-ComputerInfo
Get-WmiObject Win32_OperatingSystem       # legacy WMI (use Get-CimInstance on modern systems)
Get-CimInstance Win32_OperatingSystem
[System.Environment]::OSVersion
$PSVersionTable                              # PowerShell version info

whoami
$env:USERNAME
$env:COMPUTERNAME
```

## Modules

```powershell
Get-Module -ListAvailable          # all installed modules
Import-Module Az
Install-Module -Name Az -Scope CurrentUser
Update-Module -Name Az
Remove-Module Az
Get-Command -Module Az                # list commands in a module

Find-Module -Name "*azure*"        # search PowerShell Gallery
```

## Cloud CLI Integration (Az / AWS / GCP modules)

```powershell
# Azure PowerShell module
Connect-AzAccount
Get-AzSubscription
Get-AzResourceGroup
Get-AzVM

# AWS Tools for PowerShell
Install-Module -Name AWS.Tools.EC2
Set-AWSCredential -AccessKey $key -SecretKey $secret -StoreAs default
Get-EC2Instance
```

## Script Template

```powershell
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

try {
    Write-Log "Starting script for $InputPath"

    if (-not (Test-Path $InputPath)) {
        throw "Input path not found: $InputPath"
    }

    # main logic here

    Write-Log "Done"
}
catch {
    Write-Error "Script failed: $($_.Exception.Message)"
    exit 1
}
```

## Common Gotchas

- PowerShell's pipeline passes **objects**, not text — piping to `Where-Object`/`Select-Object` filters/projects on object properties, not raw strings, which is fundamentally different from Bash pipes.
- Comparison operators are `-eq`/`-ne`/`-gt`/etc., not `==`/`!=`/`>` — the latter are for numeric operations or redirection in different contexts, not comparisons.
- Case-insensitivity by default — `-eq` is case-insensitive for strings; use `-ceq` (and other `-c`-prefixed operators) for case-sensitive comparisons.
- `$_` refers to the current pipeline object inside `ForEach-Object`/`Where-Object` script blocks — easy to shadow accidentally with a variable of the same name in nested scopes.
- Execution policy (`Restricted` by default on some systems) can silently block script execution — `Set-Execution Policy RemoteSigned` (or run with `-ExecutionPolicy Bypass`) is often needed before a `.ps1` will run at all.
- Array unwrapping surprises — a pipeline or cmdlet that returns exactly one object may return it directly rather than as a one-element array, which can break code assuming `.Count` or indexing always works; wrap with `@(...)` to force array context when needed.
