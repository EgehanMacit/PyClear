PyClear - Python Code Analysis Tool 🐍
PyClear is a professional Python utility designed to analyze the code quality, readability, and security of .py files.
It highlights the strengths and weaknesses of your script and provides actionable suggestions for improvement.

Features
PEP 8 Compliance Check
Detects common styling issues, including:

Excessively long lines

Use of tabs instead of spaces

Redundant trailing whitespace

Security Analysis
Identifies potential security risks in your code:

Usage of eval() or exec() functions

Hardcoded passwords or sensitive information

Code Metrics
Measurements for maintainability and readability:

Total number of lines

Total character count

Average line length

AI-Based Recommendations
Provides smart suggestions based on detected errors and metrics:

Style improvements

Security enhancements

Readability and modularity tips

PDF Report Generation
Produces professional, Unicode-supported PDF reports featuring:

Analyzed file path

PEP 8 violations

Security alerts

Code metrics

AI-driven suggestions

Final Score (0–100)

User-Friendly GUI
An interface designed with Kivy offering:

Easy file selection

Interactive results screen

"Back" and "Export as PDF" buttons

How to Use
Launch the Application
Double-click the .exe file or run it via Python: python gui/main_gui.py.

Select a File
Locate and select the .py file you wish to analyze.

Start Analysis
Click the Start Analysis button.

View Results
Once the analysis is complete, the following will be displayed:

File Path: Full path of the analyzed file.

PEP 8 Errors: Issues regarding coding style.

Security Warnings: Potential security risks found in the code.

Code Metrics: Total lines, total characters, etc.

AI Suggestions: Tips to optimize your code.

Final Score: An overall grade (0–100).

Generate PDF Report
Click Export as PDF to save the results as a document.

Analyze a New File
Click the Back button to return to the selection screen and choose another file.

Usage Example
Run main_gui.py.

Select example.py → Click Start Analysis.

View analysis results on the screen.

Click Export as PDF → report_example.pdf will be created.

Click Back → Select a new file and repeat the process.