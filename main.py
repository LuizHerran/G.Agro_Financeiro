import sys

from app.database.backup import create_backup_and_cleanup
from app.database.schema import initialize_database
from app.reports.automatic_reports import ( generate_monthly_report, generate_weekly_report,)
from app.ui.app import run_app
from app.utils.scheduler import create_all_tasks

def main() -> None:
    initialize_database()

    if "--weekly-report" in sys.argv:
        report_path = generate_weekly_report()
        print(f"Relatório semanal criado: {report_path}")
        return

    if "--monthly-report" in sys.argv:
        report_path = generate_monthly_report()
        print(f"Relatório mensal criado: {report_path}")
        return

    if "--backup" in sys.argv:
        backup_path = create_backup_and_cleanup()
        print(f"Backup criado: {backup_path}")
        return

    if "--setup-scheduler" in sys.argv:
        create_all_tasks()
        print("Tarefas automáticas configuradas com sucesso.")
        return

    run_app()


if __name__ == "__main__":
    main()