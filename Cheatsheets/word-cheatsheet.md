# Microsoft Word Cheatsheet

## Navigation Shortcuts

```text
Ctrl+Home / Ctrl+End         Go to start / end of document
Ctrl+↑ / Ctrl+↓                 Jump to previous/next paragraph
Ctrl+← / Ctrl+→                    Jump one word left/right
Ctrl+G                                 Go To dialog (page, section, line, bookmark, etc.)
Ctrl+F                                    Find (Navigation Pane)
Ctrl+H                                       Replace
Ctrl+Alt+Home                                   Browse object jump (with Select Browse Object)
Alt+Ctrl+P / O / N                                  Switch to Print / Outline / Normal (Draft) view
Shift+F5                                               Return to last edit location (cycles through recent edits)
Ctrl+PageUp / Ctrl+PageDown                               Previous / next page
```

## Selection Shortcuts

```text
Ctrl+A                    Select entire document
Shift+↑/↓/←/→                 Extend selection
Ctrl+Shift+←/→                   Extend selection one word at a time
Shift+Home / Shift+End               Select to start/end of line
Ctrl+Shift+Home / End                    Select to start/end of document
Shift+Click                                  Extend selection to click point
Ctrl+Click on a sentence                        Select the whole sentence
Triple-click a paragraph                           Select the whole paragraph
Alt+Click and drag                                     Select a rectangular (column) block of text
F8                                                        Extend selection mode (press again to extend by word, sentence, etc.)
```

## Editing Shortcuts

```text
Ctrl+C / Ctrl+X / Ctrl+V        Copy / Cut / Paste
Ctrl+Shift+V                        Paste Special
Ctrl+Alt+V                             Paste Special dialog (choose format)
Ctrl+Z / Ctrl+Y                           Undo / Redo
Ctrl+B / Ctrl+I / Ctrl+U                     Bold / Italic / Underline
Ctrl+Shift+W                                    Underline words only, not spaces
Ctrl+D                                             Font dialog
Ctrl+Shift+F                                          Change font (opens font name box)
Ctrl+Shift+P                                             Change font size (opens size box)
Ctrl+] / Ctrl+[                                             Increase / decrease font size by 1pt
Ctrl+Shift+> / <                                                Increase / decrease font size to next preset
Ctrl+Space                                                         Clear manual character formatting
Ctrl+Q                                                                Clear manual paragraph formatting
Ctrl+= / Ctrl+Shift+=                                                    Subscript / Superscript
Shift+F3                                                                    Cycle text case (UPPER/lower/Title)
```

## Paragraph & Alignment

```text
Ctrl+E / Ctrl+L / Ctrl+R / Ctrl+J        Center / Left / Right / Justify alignment
Ctrl+1 / Ctrl+2 / Ctrl+5                    Single / Double / 1.5 line spacing
Ctrl+0 (zero)                                  Toggle 12pt spacing before paragraph
Ctrl+M / Ctrl+Shift+M                             Increase / decrease indent
Ctrl+T / Ctrl+Shift+T                                Hanging indent / remove hanging indent
Ctrl+Enter                                              Insert a page break
Ctrl+Shift+Enter                                           Insert a column break
Shift+Enter                                                    Line break (no new paragraph)
Ctrl+Hyphen                                                        Optional (soft) hyphen
Ctrl+Shift+Hyphen                                                     Non-breaking hyphen
Ctrl+Shift+Space                                                        Non-breaking space
```

## Styles & Formatting

```text
Ctrl+Alt+1 / 2 / 3        Apply Heading 1 / 2 / 3 style
Ctrl+Shift+N                  Apply Normal (body text) style
Ctrl+Shift+S                     Apply Styles pane / Apply Style box
Alt+Ctrl+K                          Start AutoFormat

Home tab > Styles gallery — click to apply a built-in style
Home tab > Styles pane launcher (bottom-right of Styles group) — full list + Modify options
Right-click a style > Modify — change font, spacing, and set "Update automatically"
Format Painter (Ctrl+Shift+C to copy, Ctrl+Shift+V to apply) — copy formatting between selections
```

## Working with Long Documents

```text
References tab > Table of Contents — auto-generate from Heading styles
References > Update Table — refresh page numbers/entries after edits
View > Navigation Pane (Ctrl+F) — outline view of all headings, drag to reorder sections
View > Outline — dedicated outline editing mode, promote/demote headings

Insert > Header & Footer
Insert > Page Number
Design tab (in Header/Footer edit mode) > Different First Page / Different Odd & Even Pages
Layout > Breaks > Section Break (Next Page / Continuous) — needed to vary headers/footers or page numbering per section

Insert > Cross-reference — link to a heading, figure, table, bookmark; updates automatically if the target moves
Insert > Bookmark — name a location for cross-referencing or hyperlinking
Insert > Caption — auto-numbered captions for figures/tables, feeds a "Table of Figures"
References > Insert Table of Figures
References > Insert Index / Mark Entry — build a back-of-book index
References > Insert Footnote (Alt+Ctrl+F) / Insert Endnote (Alt+Ctrl+D)
```

## Citations & Bibliography

```text
References > Insert Citation > Add New Source          Add a reference with structured fields (author, title, year...)
References > Style dropdown                                 Choose citation style (APA, MLA, Chicago, IEEE, etc.)
References > Bibliography                                      Insert an auto-generated, style-formatted bibliography
References > Manage Sources                                       Edit/reuse sources across documents
```

## Tables

```text
Insert > Table — draw, insert grid, or Insert Table dialog
Tab / Shift+Tab              Move to next / previous cell (Tab in the last cell adds a new row)
Alt+Home / Alt+End              Jump to first / last cell in a row
Alt+PageUp / Alt+PageDown          Jump to first / last cell in a column

Table Design tab > Table Styles — quick formatting presets
Table Design > Borders and Shading
Layout tab (table tools) > Insert Above/Below/Left/Right, Merge Cells, Split Cells
Layout > Sort — sort table rows by a column
Layout > Formula — basic spreadsheet-like formulas in table cells: =SUM(ABOVE), =SUM(LEFT)
Layout > Convert Text to Table / Convert Table to Text
Layout > Repeat Header Rows — keep header visible across page breaks
```

## Mail Merge

```text
Mailings tab > Start Mail Merge > Letters/Emails/Envelopes/Labels
Mailings > Select Recipients > Use an Existing List (Excel/CSV/Access source)
Mailings > Insert Merge Field — placeholders like «FirstName», «Amount»
Mailings > Rules > If...Then...Else — conditional content per recipient
Mailings > Preview Results — cycle through merged records before finishing
Mailings > Finish & Merge > Edit Individual Documents / Print / Send Email Messages
```

## Review, Comments & Track Changes

```text
Ctrl+Shift+E                Toggle Track Changes
Alt+Ctrl+M                     Insert a comment
Review tab > Accept / Reject                   Step through and resolve tracked changes
Review tab > Compare                              Compare two versions of a document
Review > Restrict Editing                            Lock formatting/editing, optionally with a password
Review > Spelling & Grammar (F7)
Review > Word Count (Ctrl+Shift+C in some builds; also status bar shows live count)
Review > Read Aloud
```

## Insert Menu Highlights

```text
Insert > Picture / Online Pictures / Screenshot / Icons / SmartArt / Chart
Insert > Shapes / Text Box / WordArt
Insert > Symbol / Equation (Alt+=)
Insert > Hyperlink (Ctrl+K)
Insert > Object — embed another file type (Excel sheet, PDF page, etc.)
Insert > Date & Time
Insert > Quick Parts > AutoText / Field — reusable content blocks and dynamic fields
Insert > Header/Footer/Page Number
```

## Fields (dynamic content)

```text
{ PAGE }                  Current page number
{ NUMPAGES }                  Total pages
{ DATE \@ "yyyy-MM-dd" }          Current date, formatted
{ FILENAME }                        Current file name
{ TOC \o "1-3" \h \z \u }              Table of Contents field (levels 1-3, hyperlinked)
{ REF Bookmark1 }                         Reference to a bookmark's content
{ SEQ Figure \* ARABIC }                     Auto-incrementing sequence (used by captions)

Alt+F9              Toggle field code visibility (see the raw field vs its rendered result)
F9                      Update the selected field
Ctrl+A, F9                Update all fields in the document
Ctrl+Shift+F9                 Unlink a field (convert to static text/value)
```

## Templates & Building Blocks

```text
File > New > search or browse templates
File > Save As > Word Template (.dotx)
Insert > Quick Parts > Building Blocks Organizer          reusable content (cover pages, headers, boilerplate text)
Developer tab > Content Controls (Rich Text, Plain Text, Dropdown, Date Picker, Checkbox)     for structured/fillable templates
```

## Macros / VBA Basics

```vb
Sub InsertDateStamp()
    Selection.InsertDateTime DateTimeFormat:="MMMM d, yyyy", InsertAsField:=False
End Sub

Sub ReplaceAllOccurrences()
    Selection.Find.Execute FindText:="old", ReplaceWith:="new", Replace:=wdReplaceAll
End Sub
```

```text
Alt+F11               Open the VBA editor
Developer tab > Macros / Record Macro / Visual Basic
Alt+F8                    Run Macro dialog
```

## Exporting & File Formats

```text
File > Export > Create PDF/XPS          Export as PDF (also: File > Save As > choose PDF)
File > Save As > Save as Type          .docx, .doc, .rtf, .txt, .odt, .html, .pdf, .dotx (template)

File > Options > Save > "Embed fonts in the file"      important when sharing .docx with unusual fonts, to preserve appearance
```

## Compare & Combine Documents

```text
Review > Compare > Compare (two versions of one doc, shows differences as tracked changes)
Review > Compare > Combine (merge tracked changes from multiple reviewers into one document)
```

## Useful Status Bar Toggles

```text
Right-click the status bar to enable/disable:
- Word Count, Page Number, Section, Line/Column, Track Changes indicator,
  Overtype/Insert mode, Selection Mode, Macro Recording indicator
```

## Common Gotchas

- Direct/manual formatting (selecting text and clicking Bold/font size) overrides style-based formatting and makes documents inconsistent and harder to maintain — prefer applying/modifying Styles for anything beyond a one-off emphasis.
- Section breaks (not page breaks) are required to have different headers/footers, margins, or page orientation in different parts of the same document — a plain page break won't allow this.
- Track Changes can hide content that still exists in the file (deleted text, comments) even after it looks "accepted" visually — use Review > Accept All / Reject All and check for personal/hidden metadata (File > Info > Check for Issues > Inspect Document) before sharing externally.
- Tables of Contents and captions/cross-references don't auto-update on their own — press F9 or use References > Update Table before finalizing/printing/exporting.
- Pasting content from the web or another Word doc can bring along unwanted styles — use Paste Special > Keep Text Only (or Ctrl+Shift+V then choose "Merge Formatting"/"Keep Text Only") to avoid style pollution.
- Embedded objects (Excel tables, etc.) inflate file size significantly and can behave inconsistently across Word versions — consider linking or pasting as an image/table when live editing isn't required.
