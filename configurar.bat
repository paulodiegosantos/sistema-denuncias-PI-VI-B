@echo off
title Configuracao - Sistema de Denuncias

echo ==========================================
echo   CONFIGURACAO DO SISTEMA DE DENUNCIAS
echo ==========================================
echo.

REM Verifica se o Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado.
    echo Instale o Python antes de continuar.
    pause
    exit /b 1
)

REM Cria o ambiente virtual, caso nao exista
if not exist "venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo ERRO ao criar o ambiente virtual.
        pause
        exit /b 1
    )
)

REM Instala as dependencias
echo.
echo Instalando dependencias...
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERRO ao instalar as dependencias.
    pause
    exit /b 1
)

REM Gera a chave somente se o .env ainda nao existir
if not exist ".env" (
    echo.
    echo Gerando chave de criptografia...
    venv\Scripts\python.exe -c "from cryptography.fernet import Fernet; open('.env', 'w', encoding='ascii').write('FERNET_KEY=' + Fernet.generate_key().decode() + '\n')"
    if errorlevel 1 (
        echo ERRO ao gerar a chave.
        pause
        exit /b 1
    )
    echo Chave gerada e salva no arquivo .env.
) else (
    echo.
    echo Arquivo .env encontrado. Chave existente preservada.
)

REM Executa as migracoes
echo.
echo Preparando banco de dados...
venv\Scripts\python.exe manage.py migrate
if errorlevel 1 (
    echo ERRO ao executar as migracoes.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   CONFIGURACAO CONCLUIDA!
echo ==========================================
echo.
echo Para iniciar o sistema, execute iniciar.bat.
pause
