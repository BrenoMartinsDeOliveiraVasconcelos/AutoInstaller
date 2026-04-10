@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Instalando dependencias
echo ============================================
echo.

:: Checar adm
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Necessário execução como administrador
    echo [!] Pedindo permissão.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo [*] Instalando Python usando winget.
echo.

:: Instalar python silenciosamente shhhhhhh
winget install --id Python.Python.3.12 -e --scope machine --silent --accept-source-agreements --accept-package-agreements

:: Verificar instalação
if %errorlevel% equ 0 (
    echo.
    echo [+] Python 3.12 instalado com sucesso.
    echo.
    echo [*] Instalando dependencias
    call "C:\Program Files\Python312\python.exe" -m pip install -r requirements.txt
) else (
    echo.
    echo [!] Falha na instalação: %errorlevel%
)

echo.
pause