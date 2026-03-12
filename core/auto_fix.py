# core/auto_fix.py
import re

class AutoFix:
    """Provides suggestions and automatic fixes for analyzed code."""

    def __init__(self, code: str):
        self.code = code
        self.suggestions = []

    def analyze(self):
        """Generate suggestions for improvements."""
        self.suggestions.clear()
        lines = self.code.splitlines()

        for i, line in enumerate(lines, start=1):
            stripped = line.strip()

            if re.match(r"import .*", stripped) and "os" in stripped and "os." not in self.code:
                self.suggestions.append(f"Line {i}: Unused import 'os' can be removed.")
            if len(line) > 79:
                self.suggestions.append(f"Line {i}: Line too long ({len(line)} chars).")
            if stripped == "" and (i > 1 and lines[i-2].strip() == ""):
                self.suggestions.append(f"Line {i}: Multiple consecutive empty lines.")
            if re.match(r"def \w+\(.*\):", stripped):
                next_line = lines[i] if i < len(lines) else ""
                if '"""' not in next_line and "'''" not in next_line:
                    self.suggestions.append(f"Line {i}: Function missing docstring.")

        return self.suggestions

    def auto_fix(self):
        """Apply simple automatic fixes without breaking the code."""
        fixed_lines = []
        prev_empty = False

        for line in self.code.splitlines():
            # Remove trailing whitespace
            line = line.rstrip()
            # Skip multiple empty lines
            if line == "":
                if prev_empty:
                    continue
                prev_empty = True
            else:
                prev_empty = False
            fixed_lines.append(line)

        # Remove unused import os if safe
        if "import os" in fixed_lines and "os." not in self.code:
            fixed_lines = [l for l in fixed_lines if l != "import os"]

        return "\n".join(fixed_lines)
