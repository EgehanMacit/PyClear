# core/metrics.py
import ast

def analyze_metrics(code_text: str) -> dict:
    """
    Kodun yapısını inceler:
    - Fonksiyon sayısı
    - Sınıf sayısı
    - Yorum oranı
    - Ortalama fonksiyon uzunluğu
    - Karmaşıklık
    - total_lines, total_chars (daha önce analyzer tarafından da eklenebilir)
    """
    # Güvenli AST parse
    try:
        tree = ast.parse(code_text)
    except SyntaxError:
        # Syntax hatası olsa bile bazı metrikleri döndürebilmek için devam et
        tree = None

    func_count = 0
    class_count = 0
    func_lengths = []
    comment_lines = 0
    total_lines = len(code_text.splitlines())
    total_chars = len(code_text)
    complexity = 0

    if tree is not None:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_count += 1
                # fonksiyon içi satır sayısını tahmini olarak al
                func_lengths.append(len(node.body))
                complexity += len(node.body)
            elif isinstance(node, ast.ClassDef):
                class_count += 1

    for line in code_text.splitlines():
        if line.strip().startswith('#'):
            comment_lines += 1

    avg_func_length = sum(func_lengths) / func_count if func_count > 0 else 0
    comment_ratio = (comment_lines / total_lines) * 100 if total_lines > 0 else 0

    return {
        "functions": func_count,
        "classes": class_count,
        "avg_func_length": round(avg_func_length, 2),
        "comment_ratio": round(comment_ratio, 2),
        "complexity": complexity,
        "total_lines": total_lines,
        "total_chars": total_chars
    }
