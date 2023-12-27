; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define appName "Second"
#define appVer "3.0"
#define appPublisher "Infinite, Inc."
#define appURL "cpythonist.github.io/second.html"
#define appOutName "second3.exe"

[Code]
function GetEnvKey(Param: string): string;
begin
  if IsAdminInstallMode then
    Result := 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
  else
    Result := 'Environment';
end;

function CheckAdmin(Param: string): string;
begin
  if IsAdminInstallMode then
  begin
    Result := ExpandConstant('{commonpf64}/Infinite/{#appName}3');
  end
  else
  begin
    Result := ExpandConstant('{localappdata}/Infinite/{#appName}3');
  end
end;

procedure RemovePath(Path: string);
var
  Paths: string;
  P: Integer;
begin
  if not RegQueryStringValue(HKLM, GetEnvKey('None'), 'Path', Paths) then
  begin
    Log('PATH not found');
  end
    else
  begin
    Log(Format('PATH is [%s]', [Paths]));

    P := Pos(';' + Uppercase(Path) + ';', ';' + Uppercase(Paths) + ';');
    if P = 0 then
    begin
      Log(Format('Path [%s] not found in PATH', [Path]));
    end
      else
    begin
      if P > 1 then P := P - 1;
      Delete(Paths, P, Length(Path) + 1);
      Log(Format('Path [%s] removed from PATH => [%s]', [Path, Paths]));
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    RemovePath(ExpandConstant('{app}'));
  end;
end;

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{6A1D0E79-85F2-4350-9CBF-17D52D110BA2}
AppName={#appName}
AppVersion={#appVer}
;AppVerName={#appName} {#appVer}
AppPublisher={#appPublisher}
AppPublisherURL={#appURL}
AppSupportURL={#appURL}
AppUpdatesURL={#appURL}
DefaultDirName={code:CheckAdmin}
DefaultGroupName={#appName}
DisableProgramGroupPage=yes
LicenseFile=E:\Second3.0\second3\LICENSE.txt
InfoBeforeFile=infoBefore.txt
InfoAfterFile=infoAfter.txt
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
Compression=lzma2/ultra64
InternalCompressLevel=ultra
SolidCompression=yes
OutputDir=E:\Second3.0\output
OutputBaseFilename=SecondSetup-3.0
SetupIconFile=E:\Second3.0\second3Install.ico
WizardStyle=modern
UninstallDisplayIcon={app}\{#appOutName}
ChangesEnvironment=yes

[Registry]
Root: HKA; Subkey: {code:GetEnvKey}; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}";  

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: envPath; Description: "Add to PATH variable" 

[Files]
Source: "E:\Second3.0\second3\{#appOutName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\_bz2.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\_ctypes.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\_lzma.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\_socket.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\crashReports.dat"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\libffi-8.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\python311.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\second3.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\select.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\unicodedata.pyd"; DestDir: "{app}"; Flags: ignoreversion
Source: "E:\Second3.0\second3\vcruntime140.dll"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#appName} 3"; Filename: "{app}\{#appOutName}"
Name: "{autodesktop}\{#appName} 3"; Filename: "{app}\{#appOutName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#appOutName}"; Description: "{cm:LaunchProgram,{#StringChange(appName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent


