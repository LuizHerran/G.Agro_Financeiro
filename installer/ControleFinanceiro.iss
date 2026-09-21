#define MyAppName "Controle Financeiro"
#define MyAppVersion "1.0.3"
#define MyAppPublisher "G.Agro"
#define MyAppExeName "ControleFinanceiro.exe"

[Setup]
AppId={{8A6D5E9B-7B5E-4A4E-9B31-7E3C4A1F2D10}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={autopf}\Controle Financeiro
DefaultGroupName={#MyAppName}

OutputDir=..\dist
OutputBaseFilename=ControleFinanceiro-Setup-{#MyAppVersion}

Compression=lzma
SolidCompression=yes

PrivilegesRequired=admin

ArchitecturesInstallIn64BitMode=x64compatible

CloseApplications=no

UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "..\dist\ControleFinanceiro\*"; \
    DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs

Source: "..\dist\Updater.exe"; \
    DestDir: "{app}"; \
    Flags: ignoreversion onlyifdoesntexist

Source: "..\app\ui\assets\logo.ico"; \
    DestDir: "{app}"; \
    Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Controle Financeiro"; \
    Filename: "{app}\ControleFinanceiro.exe"; \
    IconFilename: "{app}\logo.ico"

Name: "{autodesktop}\Controle Financeiro"; \
    Filename: "{app}\ControleFinanceiro.exe"; \
    IconFilename: "{app}\logo.ico"

[Run]
Filename: "{app}\{#MyAppExeName}"; \
    Description: "Executar Controle Financeiro"; \
    Flags: nowait postinstall skipifsilent