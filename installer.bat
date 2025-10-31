@echo off
REM Instala o Clap Assistant Pro para inicializar com o Windows
set APPDIR=%APPDATA%\ClapAssistantPro
mkdir "%APPDIR%" >nul 2>&1
copy "%~dp0\dist\clap_assistant_pro.exe" "%APPDIR%\clap_assistant_pro.exe" /Y

REM Cria atalho na pasta de inicialização
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ClapAssistantPro.lnk');$s.TargetPath='%APPDATA%\ClapAssistantPro\clap_assistant_pro.exe';$s.Save()"

echo.
echo ✅ Clap Assistant Pro instalado com sucesso!
echo Ele será iniciado automaticamente quando o Windows iniciar.
echo Logs em: %TEMP%\clap_assistant\clap_assistant.log
echo.
pause
