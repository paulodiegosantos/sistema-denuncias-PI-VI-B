@echo off
title Sistema de Denuncias

if not exist ".env" (
    echo ERRO: Arquivo .env nao encontrado.
    echo Execute configurar.bat primeiro.
    pause
    exit /b 1
)

if not exist "venv\Scripts\python.exe" (
    echo ERRO: Ambiente virtual nao encontrado.
    echo Execute configurar.bat primeiro.
    pause
    exit /b 1
)

echo Iniciando o sistema...
echo.
echo Acesse: http://127.0.0.1:8000/
echo.

venv\Scripts\python.exe manage.py runserver

pause
