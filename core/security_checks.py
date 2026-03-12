# core/security_checks.py
import re

def security_scan(code_text: str) -> list:
    """
    Basit güvenlik kontrolleri yapar.
    Potansiyel riskli fonksiyon ve yapıların varlığını arar.
    """
    issues = []

    if re.search(r'\beval\(', code_text):
        issues.append("eval() kullanılmış — bu çok tehlikeli bir fonksiyondur.")
    if re.search(r'\bexec\(', code_text):
        issues.append("exec() kullanılmış — dış girdilerde büyük güvenlik riski oluşturur.")
    if re.search(r'\bos\.system\(', code_text):
        issues.append("os.system() çağrısı mevcut — komut enjeksiyonu riski.")
    if re.search(r'\bsubprocess\.Popen\(', code_text):
        issues.append("subprocess.Popen() kullanımı riskli olabilir.")
    if re.search(r'\bpickle\.load\(', code_text):
        issues.append("pickle.load() — güvenli olmayan deserialization işlemi.")
    if re.search(r'\binput\(', code_text):
        issues.append("input() doğrudan kullanılmış — kullanıcı girdisi doğrulanmalı.")
    if re.search(r'\bopen\(', code_text):
        issues.append("open() kullanılmış — dosya yolları güvenli biçimde doğrulanmalı.")

    return issues
