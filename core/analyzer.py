# core/analyzer.py
import ast
from core.metrics import analyze_metrics
from core.security_checks import security_scan
from utils.score_calculator import calculate_final_score
from core.auto_fix import AutoFix

class CodeAnalyzer:
    def __init__(self, code_text: str):
        self.code = code_text
        self.lines = code_text.split("\n")  # <-- BU GEREKLİ

        self.pep8_issues = []
        self.metrics = {}
        self.security_issues = []
        self.final_score = 0
        self.suggestions = []

        self.advanced_security = []

    def pep8_check(self):
        lines = self.lines
        total_lines = len(lines)
        total_chars = len(self.code)
        self.pep8_issues.clear()

        for i, line in enumerate(lines, 1):
            # Satır tamamen boş mu kontrol et
            if not line.strip():
                continue  # Boş satırsa skip

            # Trailing whitespace
            if line.rstrip() != line:
                self.pep8_issues.append(f"Line {i}: Trailing whitespace detected.")

            # Tab kontrolü
            if "\t" in line:
                self.pep8_issues.append(f"Line {i}: Tab used instead of spaces.")

            # Too long (100 karakterden uzun mu)
            if len(line.rstrip()) > 100:
                self.pep8_issues.append(f"Line {i}: Too long ({len(line.rstrip())} chars).")

        return {"total_lines": total_lines, "total_chars": total_chars}

    def analyze(self):
        """
        Run full code analysis:
        - PEP8 issues
        - Security issues
        - Metrics
        - Final score
        - AI suggestions
        """
        try:
            # PEP8 check
            pep8_meta = self.pep8_check()

            # Code metrics
            self.metrics = analyze_metrics(self.code)
            self.metrics["total_lines"] = pep8_meta["total_lines"]
            self.metrics["total_chars"] = pep8_meta["total_chars"]

            # Security scan
            self.security_issues = security_scan(self.code)

            # Calculate final score
            self.final_score = calculate_final_score(
                self.metrics, self.pep8_issues, self.security_issues
            )

            # AI suggestions (AutoFix)
            fixer = AutoFix(self.code)
            self.suggestions = fixer.analyze()

        except Exception as e:
            self.pep8_issues.append(f"Analysis error: {e}")

        # Return full analysis data
        return {
            "pep8_issues": self.pep8_issues,
            "security_issues": self.security_issues,
            "metrics": self.metrics,
            "final_score": self.final_score,
            "suggestions": self.suggestions
        }
