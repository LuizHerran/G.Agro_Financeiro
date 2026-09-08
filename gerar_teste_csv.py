from app.database.schema import initialize_database
from app.reports.csv_reports import generate_csv_report

initialize_database()

arquivo = generate_csv_report(
    start_date="2026-09-01",
    end_date="2026-09-08",
    output_path="relatorio_teste.csv",
)

print(f"Relatório criado em:")
print(arquivo.resolve())