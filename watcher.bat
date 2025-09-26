@echo off
title Auto Login Watcher

:: 设置要检查和启动的脚本名称
set SCRIPT_NAME="E:\LZU-auto_login-main\auto_login.bat"

:: 设置检查间隔（秒）
set CHECK_INTERVAL=300

:CHECK_LOOP
:: -----------------------------------------------------------------
:: 使用 set /a 获取当前时间，避免使用 %DATE% %TIME% 的区域格式问题
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set CurrentDate=%%a%%b%%c%%d
for /f "tokens=1-3 delims=:. " %%a in ('echo %time%') do set CurrentTime=%%a:%%b:%%c

echo -----------------------------------------------------------------
echo [%CurrentDate% %CurrentTime%] 正在检查 "%SCRIPT_NAME%" 是否在运行...

:: 使用 wmic 获取命令行信息并查找您的脚本名称
:: 增加 findstr /V /C:"wmic" 避免匹配到 wmic 本身的命令行
wmic process where "name='cmd.exe'" get CommandLine | findstr /I /C:"%SCRIPT_NAME%" | findstr /V /C:"wmic"
IF %ERRORLEVEL% EQU 0 (
    echo [%CurrentDate% %CurrentTime%] "%SCRIPT_NAME%" 正在运行。
) ELSE (
    echo [%CurrentDate% %CurrentTime%] "%SCRIPT_NAME%" 未在运行，现在启动。
    
    :: 启动您的 auto_login.bat 脚本
    start "" %SCRIPT_NAME%
    
    echo [%CurrentDate% %CurrentTime%] "%SCRIPT_NAME%" 已启动。
)

echo [%CurrentDate% %CurrentTime%] 等待 %CHECK_INTERVAL% 秒后再次检查...

:: 关键修改：直接使用数字，确保 timeout 仅接收一个参数
timeout /T %CHECK_INTERVAL% /NOBREAK

goto CHECK_LOOP 