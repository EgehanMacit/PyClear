from core.analyzer import CodeAnalyzer

if __name__ == "__main__":
    file_path = input("Analiz edilecek .py dosyasını girin: ").strip()
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()

    analyzer = CodeAnalyzer(code)
    result = analyzer.analyze()

    print("\n=== PEP8 Hataları ===")
    for i in result["pep8_issues"]:
        print(" -", i)

    print("\n=== Güvenlik Uyarıları ===")
    for s in result["security_issues"]:
        print(" -", s)

    print("\n=== Metrikler ===")
    for k, v in result["metrics"].items():
        print(f"{k}: {v}")

    print("\n Toplam Puan:", result["final_score"])
