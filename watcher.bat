@echo off
title Auto Login Watcher

:: ����Ҫ���������Ľű�����
set SCRIPT_NAME="E:\LZU-auto_login-main\auto_login.bat"

:: ���ü�������룩
set CHECK_INTERVAL=300

:CHECK_LOOP
:: -----------------------------------------------------------------
:: ʹ�� set /a ��ȡ��ǰʱ�䣬����ʹ�� %DATE% %TIME% �������ʽ����
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set CurrentDate=%%a%%b%%c%%d
for /f "tokens=1-3 delims=:. " %%a in ('echo %time%') do set CurrentTime=%%a:%%b:%%c

echo -----------------------------------------------------------------
echo [%CurrentDate% %CurrentTime%] ���ڼ�� "%SCRIPT_NAME%" �Ƿ�������...

:: ʹ�� wmic ��ȡ��������Ϣ���������Ľű�����
:: ���� findstr /V /C:"wmic" ����ƥ�䵽 wmic �����������
wmic process where "name='cmd.exe'" get CommandLine | findstr /I /C:"%SCRIPT_NAME%" | findstr /V /C:"wmic"
IF %ERRORLEVEL% EQU 0 (
    echo [%CurrentDate% %CurrentTime%] "%SCRIPT_NAME%" �������С�
) ELSE (
    echo [%CurrentDate% %CurrentTime%] "%SCRIPT_NAME%" δ�����У�����������
    
    :: �������� auto_login.bat �ű�
    start "" %SCRIPT_NAME%
    
    echo [%CurrentDate% %CurrentTime%] "%SCRIPT_NAME%" ��������
)

echo [%CurrentDate% %CurrentTime%] �ȴ� %CHECK_INTERVAL% ����ٴμ��...

:: �ؼ��޸ģ�ֱ��ʹ�����֣�ȷ�� timeout ������һ������
timeout /T %CHECK_INTERVAL% /NOBREAK

goto CHECK_LOOP 