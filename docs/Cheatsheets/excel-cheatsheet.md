# Excel Cheatsheet

## Navigation Shortcuts

```text
Ctrl+Arrow keys         Jump to edge of data region
Ctrl+Home / Ctrl+End        Go to A1 / last used cell
Ctrl+G or F5                Go To dialog (jump to a specific cell/range/name)
Ctrl+F / Ctrl+H                Find / Find & Replace
Page Up / Page Down               Scroll one screen up/down
Alt+Page Up / Alt+Page Down          Scroll one screen left/right
Ctrl+Tab                                Switch between open workbooks
Ctrl+PageUp / Ctrl+PageDown                Switch between worksheet tabs
Tab / Shift+Tab                                Move right / left one cell
Enter / Shift+Enter                               Move down / up one cell
```

## Selection Shortcuts

```text
Shift+Arrow keys              Extend selection one cell
Ctrl+Shift+Arrow keys             Extend selection to edge of data region
Ctrl+Shift+End                       Select to last used cell
Ctrl+A                                   Select entire sheet (or current region first press)
Ctrl+Space                                  Select entire column
Shift+Space                                    Select entire row
Ctrl+Shift+Space                                  Select entire sheet / current region + summary rows
Ctrl+Click                                           Add non-adjacent cells to selection
Shift+Click                                             Extend selection to clicked cell
```

## Editing Shortcuts

```text
Ctrl+C / Ctrl+X / Ctrl+V        Copy / Cut / Paste
Ctrl+Alt+V                          Paste Special dialog
F4                                      Repeat last action / toggle absolute references while editing a formula
Ctrl+Z / Ctrl+Y                            Undo / Redo
Ctrl+D                                        Fill down (copy cell above)
Ctrl+R                                            Fill right (copy cell to the left)
Ctrl+; / Ctrl+Shift+;                                Insert current date / current time
Alt+Enter                                               New line within the same cell
Ctrl+1                                                     Format Cells dialog
Ctrl+B / Ctrl+I / Ctrl+U                                       Bold / Italic / Underline
Ctrl+5                                                            Strikethrough
Ctrl+Shift+$                                                         Currency format
Ctrl+Shift+%                                                            Percentage format
Ctrl+Shift+#                                                               Date format
Ctrl+Shift+~                                                                  General format
Ctrl+K                                                                          Insert hyperlink
Delete                                                                             Clear cell contents (keeps formatting)
Ctrl+-                                                                                Delete cell/row/column
Ctrl++                                                                                   Insert cell/row/column
F2                                                                                          Edit active cell
Esc                                                                                            Cancel cell edit
```

## Formula Basics

```excel
=A1+B1
=A1-B1
=A1*B1
=A1/B1
=A1^2
=A1&" "&B1              ' text concatenation
=A1=B1                     ' returns TRUE/FALSE

' Cell references
A1              ' relative — shifts when copied
$A$1               ' absolute — stays fixed when copied
$A1                    ' column locked, row relative
A$1                       ' row locked, column relative
Sheet2!A1                    ' reference another sheet
[Book2.xlsx]Sheet1!A1            ' reference another workbook
```

## Lookup & Reference Functions

```excel
=VLOOKUP(lookup_value, table_array, col_index, [range_lookup])
=VLOOKUP(A2, Sheet2!A:D, 3, FALSE)          ' exact match lookup

=HLOOKUP(lookup_value, table_array, row_index, [range_lookup])

=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])
=XLOOKUP(A2, B:B, C:C, "Not Found")            ' modern replacement for VLOOKUP — no column counting, searches any direction

=INDEX(array, row_num, [col_num])
=MATCH(lookup_value, lookup_array, [match_type])
=INDEX(C:C, MATCH(A2, B:B, 0))                    ' classic INDEX/MATCH combo — more flexible than VLOOKUP

=OFFSET(reference, rows, cols, [height], [width])       ' dynamic range reference
=INDIRECT("A1")                                            ' build a reference from a text string

=CHOOSE(index_num, val1, val2, ...)
=LOOKUP(lookup_value, lookup_vector, result_vector)

=FILTER(array, include, [if_empty])          ' modern dynamic array filtering
=FILTER(A2:C100, B2:B100="Active")

=SORT(array, [sort_index], [sort_order])
=SORTBY(array, by_array, [order])
=UNIQUE(array, [by_col], [exactly_once])
```

## Math & Statistical Functions

```excel
=SUM(A1:A10)
=SUMIF(range, criteria, [sum_range])
=SUMIFS(sum_range, criteria_range1, criteria1, criteria_range2, criteria2, ...)
=SUMPRODUCT(array1, array2, ...)          ' element-wise multiply then sum — powerful for conditional math

=AVERAGE(A1:A10)
=AVERAGEIF(range, criteria, [average_range])
=AVERAGEIFS(average_range, criteria_range1, criteria1, ...)

=COUNT(A1:A10)             ' counts numeric cells
=COUNTA(A1:A10)                ' counts non-empty cells
=COUNTBLANK(A1:A10)               ' counts empty cells
=COUNTIF(range, criteria)
=COUNTIFS(criteria_range1, criteria1, criteria_range2, criteria2, ...)

=MAX(A1:A10) / =MIN(A1:A10)
=MAXIFS(max_range, criteria_range1, criteria1, ...)
=MINIFS(min_range, criteria_range1, criteria1, ...)
=MEDIAN(A1:A10)
=MODE.SNGL(A1:A10)
=STDEV.S(A1:A10)          ' sample standard deviation
=STDEV.P(A1:A10)             ' population standard deviation
=VAR.S(A1:A10) / =VAR.P(A1:A10)

=ROUND(A1, 2)          ' round to 2 decimals
=ROUNDUP(A1, 0)
=ROUNDDOWN(A1, 0)
=CEILING(A1, 1)
=FLOOR(A1, 1)
=ABS(A1)
=MOD(A1, 3)               ' remainder
=INT(A1)                     ' round down to integer
=TRUNC(A1, 0)                    ' truncate decimals without rounding
=RAND() / =RANDBETWEEN(1, 100)
=SQRT(A1)
=POWER(A1, 2)
```

## Text Functions

```excel
=CONCATENATE(A1, " ", B1)          ' legacy — prefer & or TEXTJOIN
=TEXTJOIN(", ", TRUE, A1:A10)          ' join with delimiter, skip empty cells

=LEFT(A1, 3) / =RIGHT(A1, 3) / =MID(A1, 2, 5)
=LEN(A1)
=UPPER(A1) / =LOWER(A1) / =PROPER(A1)
=TRIM(A1)                    ' remove extra spaces
=CLEAN(A1)                       ' remove non-printable characters
=SUBSTITUTE(A1, "old", "new")       ' replace occurrences of a substring
=REPLACE(A1, start, num_chars, new_text)   ' replace by position

=FIND("x", A1)          ' case-sensitive search, position of substring
=SEARCH("x", A1)            ' case-insensitive search

=TEXT(A1, "0.00")           ' number to formatted string
=TEXT(A1, "yyyy-mm-dd")
=VALUE(A1)                     ' text to number
=NUMBERVALUE(A1)

=TEXTSPLIT(A1, ",")         ' modern dynamic array text split
=TEXTBEFORE(A1, "@")            ' text before a delimiter
=TEXTAFTER(A1, "@")                ' text after a delimiter

=REPT("-", 10)          ' repeat a string
=EXACT(A1, B1)              ' case-sensitive equality check
=CHAR(65) / =CODE("A")         ' character <-> ASCII code
```

## Date & Time Functions

```excel
=TODAY() / =NOW()
=DATE(2026, 7, 17)
=YEAR(A1) / =MONTH(A1) / =DAY(A1)
=HOUR(A1) / =MINUTE(A1) / =SECOND(A1)
=WEEKDAY(A1, [type])
=WEEKNUM(A1)
=EDATE(A1, 3)              ' add 3 months
=EOMONTH(A1, 0)                ' last day of the month
=DATEDIF(start, end, "d")          ' difference in days/months/years ("y","m","d","ym","md")
=NETWORKDAYS(start, end, [holidays])   ' working days between two dates
=WORKDAY(start, days, [holidays])         ' date N working days from start
=DAYS(end, start)
=DATEVALUE("2026-07-17")
```

## Logical Functions

```excel
=IF(condition, value_if_true, value_if_false)
=IF(A1>100, "High", IF(A1>50, "Medium", "Low"))        ' nested IF

=IFS(cond1, val1, cond2, val2, ..., TRUE, default)      ' cleaner alternative to nested IF
=IFS(A1>100, "High", A1>50, "Medium", TRUE, "Low")

=AND(cond1, cond2, ...)
=OR(cond1, cond2, ...)
=NOT(condition)
=XOR(cond1, cond2)

=IFERROR(formula, value_if_error)
=IFNA(formula, value_if_na)
=ISERROR(A1) / =ISNA(A1) / =ISBLANK(A1) / =ISNUMBER(A1) / =ISTEXT(A1)

=SWITCH(expression, val1, result1, val2, result2, ..., default)
```

## Financial Functions

```excel
=PMT(rate, nper, pv, [fv], [type])          ' loan/mortgage payment
=FV(rate, nper, pmt, [pv], [type])              ' future value
=PV(rate, nper, pmt, [fv], [type])                 ' present value
=NPER(rate, pmt, pv, [fv], [type])                    ' number of periods
=RATE(nper, pmt, pv, [fv], [type])                       ' interest rate

=NPV(rate, value1, value2, ...)          ' net present value
=IRR(values, [guess])                       ' internal rate of return
=XIRR(values, dates, [guess])                  ' IRR for irregular cash flow dates
=XNPV(rate, values, dates)

=SLN(cost, salvage, life)          ' straight-line depreciation
=DB(cost, salvage, life, period)      ' declining balance depreciation
```

## Array & Dynamic Array Formulas

```excel
=SEQUENCE(rows, [columns], [start], [step])       ' generate a sequence of numbers
=RANDARRAY(rows, columns, min, max, integer)          ' array of random numbers

' Spill behavior — a formula in one cell can "spill" results into adjacent cells automatically
=SORT(FILTER(A2:C100, B2:B100="Active"))

' Reference an entire spill range
=A2#

' Legacy array formula (Ctrl+Shift+Enter, pre-dynamic-array Excel)
{=SUM(IF(A1:A10>5, A1:A10, 0))}
```

## Conditional Formatting

```text
Home > Conditional Formatting > New Rule
- Highlight Cells Rules (greater than, between, duplicate values, etc.)
- Top/Bottom Rules
- Data Bars / Color Scales / Icon Sets
- Custom formula: =$B2>AVERAGE($B$2:$B$100)      ' highlight above-average rows
```

## PivotTables

```text
Insert > PivotTable
- Drag fields into Rows / Columns / Values / Filters
- Value Field Settings: Sum, Count, Average, Max, Min, % of Total, Running Total, Rank
- Right-click > Group... to group dates (by month/quarter/year) or numbers (into bins)
- Right-click > Show Values As > % of Grand Total, % of Column Total, Difference From, etc.
- Insert > PivotChart for a linked visualization
- Refresh: right-click > Refresh, or Data > Refresh All
- Slicers: Insert > Slicer for interactive filter buttons
```

```excel
=GETPIVOTDATA("Sum of Amount", $A$3, "Category", "Electronics")    ' pull a value out of a PivotTable by criteria
```

## Data Tools

```text
Data > Text to Columns          Split one column into multiple (by delimiter or fixed width)
Data > Remove Duplicates           Remove duplicate rows based on selected columns
Data > Data Validation                Restrict allowed input (dropdown lists, number ranges, custom formulas)
Data > Consolidate                       Combine data from multiple ranges/sheets
Data > What-If Analysis > Goal Seek        Find an input that produces a target output
Data > What-If Analysis > Data Table          Sensitivity analysis across a range of inputs
Data > Get Data / Power Query               Import & transform data from files, databases, web
Data > Sort / Filter                           Standard sort and AutoFilter
```

## Named Ranges

```text
Formulas > Name Manager (Ctrl+F3)
Formulas > Define Name

=MyRange              ' use a named range directly in a formula
```

```excel
' Named ranges make formulas more readable
=SUM(SalesData)          ' instead of =SUM(A2:A500)
```

## Charts

```text
Insert > Charts — Column, Line, Pie, Bar, Area, Scatter, Combo, etc.
Right-click chart > Select Data to change series/range
Chart Design tab > Change Chart Type, Quick Layout, Chart Styles
Format > Add Chart Element > Trendline, Error Bars, Data Labels
Alt+F1                    Insert a default chart on the current sheet
F11                          Insert a default chart on a NEW sheet
```

## Macros / VBA Basics

```text
Alt+F11                Open VBA editor
Developer tab > Record Macro         Record actions as a macro
Alt+F8                                   Run Macro dialog
```

```vb
Sub HelloWorld()
    MsgBox "Hello, World!"
End Sub

Sub CopyRange()
    Sheets("Sheet1").Range("A1:A10").Copy
    Sheets("Sheet2").Range("A1").PasteSpecial xlPasteValues
End Sub

Function DoubleIt(x As Double) As Double
    DoubleIt = x * 2
End Function
```

## Common Cell Formatting Codes

```text
0.00                General number, 2 decimals
#,##0                  Thousands separator, no decimals
#,##0.00                  Thousands separator, 2 decimals
0%                          Percentage
$#,##0.00                      Currency
yyyy-mm-dd                        ISO date
mm/dd/yyyy                           US date
dd/mm/yyyy                              European date
hh:mm:ss                                   Time
[Red](#,##0);#,##0                            Negative numbers in red, parentheses
```

## Common Gotchas

- `VLOOKUP` only searches to the right of the lookup column and breaks silently if column order changes — `XLOOKUP` or `INDEX`/`MATCH` avoid this.
- Dates are stored as serial numbers (days since 1900-01-01 on Windows Excel) — formatting a number as a date doesn't change the underlying value, and comparing text-formatted "dates" numerically will fail.
- Circular references (a formula referencing its own cell, directly or indirectly) trigger a warning and return 0 unless iterative calculation is explicitly enabled.
- `SUM` silently ignores text and blank cells rather than erroring — useful, but can mask data quality issues.
- Copy-pasting formulas shifts relative references — use `$` to lock rows/columns you don't want to shift, especially in totals/lookup tables.
- Merged cells break sorting, filtering, and many formulas that expect one value per row — avoid merging cells in data ranges; use "Center Across Selection" formatting instead for visual centering.
