import subprocess
import sys
import tempfile
from pathlib import Path


TASK_BACKUP = "Controle Financeiro - Backup"
TASK_WEEKLY = "Controle Financeiro - Relatório Semanal"
TASK_MONTHLY = "Controle Financeiro - Relatório Mensal"


def get_executable_path() -> Path:
    """
    Retorna o executável usado para executar o sistema.
    """

    return Path(sys.executable).resolve()


def get_current_user() -> str:
    """
    Retorna o usuário atual do Windows.
    """

    result = subprocess.run(
        ["whoami"],
        capture_output=True,
        text=True,
        shell=False,
        check=True,
    )

    return result.stdout.strip()


def create_task_from_xml(
    task_name: str,
    xml_content: str,
) -> None:
    """
    Cria ou atualiza uma tarefa usando XML do Agendador de Tarefas.
    """

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-16",
        suffix=".xml",
        delete=False,
    ) as file:
        file.write(xml_content)
        xml_path = Path(file.name)

    try:
        result = subprocess.run(
            [
                "schtasks",
                "/Create",
                "/TN",
                task_name,
                "/XML",
                str(xml_path),
                "/F",
            ],
            capture_output=True,
            text=True,
            shell=False,
        )

        if result.returncode != 0:
            error = result.stderr.strip() or result.stdout.strip()

            raise RuntimeError(
                f"Não foi possível criar a tarefa '{task_name}'.\n"
                f"{error}"
            )

    finally:
        xml_path.unlink(missing_ok=True)


def build_task_xml(
    argument: str,
    trigger_xml: str,
) -> str:
    """
    Monta o XML de uma tarefa do Windows.
    """

    executable = get_executable_path()
    
    if getattr(sys, "frozen", False):
        working_directory = executable.parent
        script_argument = argument
    else:
        working_directory = Path(__file__).resolve().parents[2]
        script_argument = f'"{working_directory / "main.py"}" {argument}'
        
    user = get_current_user()

    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4"
      xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">

    <RegistrationInfo>
        <Author>{user}</Author>
        <Description>Controle Financeiro - tarefa automática.</Description>
    </RegistrationInfo>

    <Triggers>
        {trigger_xml}
    </Triggers>

    <Principals>
        <Principal id="Author">
            <UserId>{user}</UserId>
            <LogonType>InteractiveToken</LogonType>
            <RunLevel>LeastPrivilege</RunLevel>
        </Principal>
    </Principals>

    <Settings>
        <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>

        <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>

        <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>

        <AllowHardTerminate>true</AllowHardTerminate>

        <StartWhenAvailable>true</StartWhenAvailable>

        <Enabled>true</Enabled>

        <Hidden>false</Hidden>

        <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    </Settings>

    <Actions Context="Author">
        <Exec>
            <Command>{executable}</Command>
            <Arguments>{script_argument}</Arguments>
            <WorkingDirectory>{working_directory}</WorkingDirectory>
        </Exec>
    </Actions>

</Task>
"""


def create_backup_task() -> None:
    """
    Cria o backup automático a cada 6 horas.
    """

    trigger = """
    <CalendarTrigger>
        <StartBoundary>2026-01-01T00:00:00</StartBoundary>
        <Enabled>true</Enabled>

        <ScheduleByDay>
            <DaysInterval>1</DaysInterval>
        </ScheduleByDay>

        <Repetition>
            <Interval>PT6H</Interval>
            <StopAtDurationEnd>false</StopAtDurationEnd>
        </Repetition>
    </CalendarTrigger>
    """

    xml = build_task_xml(
        argument="--backup",
        trigger_xml=trigger,
    )

    create_task_from_xml(
        TASK_BACKUP,
        xml,
    )


def create_weekly_report_task() -> None:
    """
    Cria o relatório semanal todo domingo às 18:00.
    """

    trigger = """
    <CalendarTrigger>
        <StartBoundary>2026-01-04T18:00:00</StartBoundary>
        <Enabled>true</Enabled>

        <ScheduleByWeek>
            <DaysOfWeek>
                <Sunday />
            </DaysOfWeek>

            <WeeksInterval>1</WeeksInterval>
        </ScheduleByWeek>
    </CalendarTrigger>
    """

    xml = build_task_xml(
        argument="--weekly-report",
        trigger_xml=trigger,
    )

    create_task_from_xml(
        TASK_WEEKLY,
        xml,
    )


def create_monthly_report_task() -> None:
    """
    Cria o relatório mensal no dia 1 de cada mês às 18:00.
    """

    trigger = """
    <CalendarTrigger>
        <StartBoundary>2026-01-01T18:00:00</StartBoundary>
        <Enabled>true</Enabled>

        <ScheduleByMonth>
            <DaysOfMonth>
                <Day>1</Day>
            </DaysOfMonth>

            <Months>
                <January />
                <February />
                <March />
                <April />
                <May />
                <June />
                <July />
                <August />
                <September />
                <October />
                <November />
                <December />
            </Months>
        </ScheduleByMonth>
    </CalendarTrigger>
    """

    xml = build_task_xml(
        argument="--monthly-report",
        trigger_xml=trigger,
    )

    create_task_from_xml(
        TASK_MONTHLY,
        xml,
    )


def create_all_tasks() -> None:
    """
    Cria todas as tarefas automáticas do sistema.
    """

    create_backup_task()
    create_weekly_report_task()
    create_monthly_report_task()


def remove_task(task_name: str) -> None:
    """
    Remove uma tarefa do Agendador.
    """

    result = subprocess.run(
        [
            "schtasks",
            "/Delete",
            "/TN",
            task_name,
            "/F",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    if result.returncode != 0:
        error = result.stderr.strip().lower()

        if "não foi possível encontrar" not in error:
            raise RuntimeError(
                f"Erro ao remover a tarefa '{task_name}'.\n"
                f"{result.stderr.strip()}"
            )


def remove_all_tasks() -> None:
    """
    Remove todas as tarefas automáticas.
    """

    remove_task(TASK_BACKUP)
    remove_task(TASK_WEEKLY)
    remove_task(TASK_MONTHLY)