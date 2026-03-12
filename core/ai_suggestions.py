# core/ai_suggestions.py
from core.analyzer import CodeAnalyzer


class AISuggestions:
    """Generates smart suggestions based on code analysis results."""

    def __init__(self, code: str, analysis_result: dict):
        self.code = code
        self.result = analysis_result
        self.suggestions = []

    def generate(self):
        self.suggestions.clear()

        # --- PEP8-based suggestions ---
        for issue in self.result.get("pep8_issues", []):
            if "Tab karakteri yerine 4 boşluk" in issue:
                self.suggestions.append("Replace tabs with 4 spaces for PEP8 compliance.")
            elif "Satır sonunda gereksiz boşluk" in issue:
                self.suggestions.append("Remove trailing whitespaces at the end of lines.")
            elif "Çok uzun satır" in issue:
                self.suggestions.append("Consider breaking long lines into multiple shorter lines.")

        # --- Security suggestions ---
        for sec_issue in self.result.get("security_issues", []):
            if "eval" in sec_issue or "exec" in sec_issue:
                self.suggestions.append("Avoid using eval()/exec() for security reasons.")
            elif "hardcoded password" in sec_issue.lower():
                self.suggestions.append("Do not hardcode passwords in the source code.")

        # --- Metric-based suggestions ---
        metrics = self.result.get("metrics", {})
        if metrics.get("total_lines", 0) > 500:
            self.suggestions.append("Consider splitting the code into smaller modules for better maintainability.")
        if metrics.get("average_line_length", 0) > 80:
            self.suggestions.append("Reduce average line length to improve readability.")

        # Default suggestion if nothing found
        if not self.suggestions:
            self.suggestions.append("No issues detected. Code looks clean!")

        return self.suggestions
