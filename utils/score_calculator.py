# utils/score_calculator.py
def calculate_final_score(metrics: dict, pep8_issues: list, security_issues: list) -> int:
    """
    100 üzerinden puan hesaplar.
    metrics artık total_lines ve total_chars içerir.
    """
    score = 100

    # PEP8 hataları
    score -= len(pep8_issues) * 0.8

    # Güvenlik açıkları (kritik)
    score -= len(security_issues) * 5

    # Az yorum varsa
    if metrics.get("comment_ratio", 0) < 5:
        score -= 10

    # Çok karmaşıksa
    if metrics.get("complexity", 0) > 50:
        score -= 15

    # Fonksiyonlar çok uzunsa
    if metrics.get("avg_func_length", 0) > 20:
        score -= 10

    # Büyük dosyaysa (ör: >5000 karakter) ekstra inceleme penalty'si (opsiyonel)
    if metrics.get("total_chars", 0) > 5000:
        # büyük dosyalar daha fazla modülerleştirme ister — küçük ceza
        score -= 2

    if score < 0:
        score = 0

    return round(score)
