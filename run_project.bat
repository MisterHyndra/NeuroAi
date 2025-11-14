@echo off
echo ==========================================
echo   Sistema de Diagnostico de Cancer - IA
echo ==========================================
echo.

:menu
echo Escolha uma opcao:
echo.
echo 1. Configurar projeto (primeira vez)
echo 2. Baixar datasets
echo 3. Treinar modelo
echo 4. Avaliar modelo
echo 5. Interface de predicoes
echo 6. Sair
echo.
set /p choice="Digite sua escolha (1-6): "

if "%choice%"=="1" goto setup
if "%choice%"=="2" goto download
if "%choice%"=="3" goto train
if "%choice%"=="4" goto evaluate
if "%choice%"=="5" goto predict
if "%choice%"=="6" goto exit
goto menu

:setup
echo.
echo Configurando projeto...
C:\Python313\python.exe setup.py
pause
goto menu

:download
echo.
echo Baixando datasets...
C:\Python313\python.exe src/data_downloader.py
pause
goto menu

:train
echo.
echo Treinando modelo...
C:\Python313\python.exe src/train_model.py
pause
goto menu

:evaluate
echo.
echo Avaliando modelo...
C:\Python313\python.exe src/evaluate_model.py
pause
goto menu

:predict
echo.
echo Abrindo interface de predicoes...
C:\Python313\python.exe src/predict.py
pause
goto menu

:exit
echo.
echo Saindo do sistema...
pause
exit